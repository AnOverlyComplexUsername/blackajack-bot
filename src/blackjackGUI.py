import discord 
from discord import Button
import UrlUtil
from GameBoard import GameBoard
from jsonFormatter import formatEmbed





class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction : discord.Interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

class GameStartUI(discord.ui.View):
    @discord.ui.button(label="Button 1", row=0, style=discord.ButtonStyle.primary)
    async def click_me_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You clicked the button!")
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")
        button.disabled = True
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callbacks(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callbackss(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")
    @discord.ui.button(label="Button 2", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callbacksss(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You pressed me!")        



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
        if self.board.getPhase() == "RESOLVED":
            if self.board.getPlayerValue() == 21 or self.board.getDealerValue() == 21:
                UrlUtil.stand()
            msg = await interaction.original_response()
            await msg.edit(view=EndGameUI())
        await self.board.edit(embed=formatEmbed(result, i=interaction)), 
   
    @discord.ui.button(label="Stand", row=0, style=discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: Button):
        '''ends players turn and the game when pressed'''
        result = UrlUtil.stand()
        await interaction.response.edit_message(view=EndGameUI())
        await self.board.edit(embed=formatEmbed(result,i=interaction))

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
        await msg.edit(view=GameUI())
    @discord.ui.button(label="End Game", row=0, style=discord.ButtonStyle.red)
    async def end_game_callback(self, interaction: discord.Interaction, button: Button):
        UrlUtil.finishGame()
        await interaction.response.edit_message(delete_after=0.01)
        

    
