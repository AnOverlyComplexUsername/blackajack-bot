import discord 
from discord import Button
import UrlUtil
from GameBoard import GameBoard
from jsonFormatter import formatEmbed, formatSessionsEmbed

class SessionList(discord.ui.View):
    ''' Parameters
        -----------
    sesList: :class:`list`
        dictionary of list of all sessions in a dictionary format   
    curStartIndex: :class:`int`
        first index that's at the top of the page 
    entryRange: :class:`int`
        how many entries should be in each page
            
        '''
    sesList : list[dict] = None
    listSize : int = 0
    curStartIndex : int = 0
    entryRange : int = 5
    
    def __init__(self, sesList : list[dict], curStartIndex : int = 0, entryRange : int = 5, timeout = 300):
        super().__init__(timeout=timeout)
        self.listSize = sesList.__len__()
        self.sesList = sesList
        self.entryRange = entryRange
        self.curStartIndex = curStartIndex
        if self.listSize < entryRange or self.curStartIndex + entryRange > self.listSize:
            nextButton : discord.Button= [x for x in self.children if x.custom_id == "next"][0]
            nextButton.disabled = True
        if self.curStartIndex == 0:
            prevButton : discord.Button= [x for x in self.children if x.custom_id == "prev"][0]
            prevButton.disabled = True
            
    @discord.ui.button(label="First Page", row=0, style=discord.ButtonStyle.primary)
    async def firstpg_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=SessionList(sesList=self.sesList,entryRange=self.entryRange,curStartIndex=0),embed=formatSessionsEmbed(sessions=self.sesList, startIndex=0, entryRange=self.entryRange))   
        
    @discord.ui.button(label="Previous", row=0, style=discord.ButtonStyle.primary, custom_id="prev")
    async def prev_callback(self, interaction: discord.Interaction, button: Button):
        self.curStartIndex -= self.entryRange
        await interaction.response.edit_message(view=SessionList(sesList=self.sesList,entryRange=self.entryRange,curStartIndex=self.curStartIndex),embed=formatSessionsEmbed(sessions=self.sesList, startIndex=self.curStartIndex, entryRange=self.entryRange))

    @discord.ui.button(label="Next", row=0, style=discord.ButtonStyle.primary,custom_id="next")
    async def next_callback(self, interaction: discord.Interaction, button: Button):
        self.curStartIndex += self.entryRange
        await interaction.response.edit_message(view=SessionList(sesList=self.sesList,entryRange=self.entryRange,curStartIndex=self.curStartIndex),embed=formatSessionsEmbed(sessions=self.sesList, startIndex=self.curStartIndex, entryRange=self.entryRange))
        
    @discord.ui.button(label="Last Page", row=0, style=discord.ButtonStyle.primary)
    async def lastpg_callback(self, interaction: discord.Interaction, button: Button):
        lastIndex =  self.listSize - (self.listSize % self.entryRange)
        await interaction.response.edit_message(view=SessionList(sesList=self.sesList,entryRange=self.entryRange,curStartIndex=lastIndex),embed=formatSessionsEmbed(sessions=self.sesList, startIndex=lastIndex, entryRange=self.entryRange))   
        
        

class GameUI(discord.ui.View):
    board : GameBoard = None
    
    def __init__(self, board : GameBoard, timeout = 180):
        super().__init__(timeout=timeout)
        self.board = board
        
 #UI for when the game starts (hit/stand)       
class StartGameUI(GameUI):
    @discord.ui.button(label="Hit", row=0, style=discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: Button):
        '''handles interactions when you draw a card; automatically ends game when dealer or player has 21 and updates game board'''
        result = UrlUtil.hit()
        await interaction.response.defer()
        if self.board.getPlayerValue() == 21 or self.board.getDealerValue() == 21:
            UrlUtil.stand()
        if self.board.getPhase() == "RESOLVED":
            msg = await interaction.original_response()
            await msg.edit(view=EndGameUI(self.board))
        await self.board.getBoardMessage().edit(embed=formatEmbed(result, i=interaction)), 
   
    @discord.ui.button(label="Stand", row=0, style=discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: Button):
        '''ends players turn and the game when pressed'''
        result = UrlUtil.stand()
        await interaction.response.edit_message(view=EndGameUI(board=self.board))
        await self.board.getBoardMessage().edit(embed=formatEmbed(result,i=interaction))

# UI for game ending (ending/start new game)
class EndGameUI(GameUI):
    @discord.ui.button(label="New Game", row=0, style=discord.ButtonStyle.green)
    async def new_game_callback(self, interaction: discord.Interaction, button: Button):
        '''when pressed, disables buttons and waits for player's input for new bet amount for new game '''
        result = UrlUtil.getGameState()
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        await self.board.continueGame(i=interaction,gameData=result)
        msg = await interaction.original_response()
        await msg.edit(view=StartGameUI(self.board))
    @discord.ui.button(label="End Game", row=0, style=discord.ButtonStyle.red)
    async def end_game_callback(self, interaction: discord.Interaction, button: Button):
        '''ends current game and archives results to database after finishing'''
        UrlUtil.finishGame()
        await interaction.response.edit_message(delete_after=0.01)
        

    
