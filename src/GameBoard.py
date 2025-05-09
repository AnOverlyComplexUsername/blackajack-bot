import discord
import UrlUtil
from blackjackGUI import GameUI
from jsonFormatter import formatEmbed 

class GameBoard:
    
    sesID = None
    '''class for interacting with and containing game and game data'''
    def __init__(self, gameData : dict = None, boardMsg : discord.Message = None, client : discord.Client = None):
        ''' Parameters
        -----------
        gameData: :class:`dict`
            dictionary of json game data
            
        boardMsg: :class:`Message`
            game board message that's being used to display current game
        
        client: :class:`Client`
            client being used to interact with discord
        '''
        self.gameData = gameData
        self.boardMsg = boardMsg 
        self.client = client
        if gameData:
            self.sesID = gameData.get("sessionId")
    
    def getBalance(self) -> str:
        '''returns the balance in json schema'''
        return str(self.gameData.get("balance"))
    
    def getPhase(self) -> str:
        ''' returns current state of game'''
        return self.gameData.get("phase")
    
    def getBoard(self) -> discord.Message:
        return self.boardMsg
        
    
    async def startNewGame(self, i : discord.Interaction):
        ''' intializes a new game '''
        response = UrlUtil.startGame()
        self.gameData : dict = response.json()
        self.sesID = self.gameData.get("sessionId")
        print(self.sesID)
        UrlUtil.setGameID(self.sesID)
        UrlUtil.resetGame()
        await i.response.send_message(content="Starting/Resuming game...",ephemeral=True)
        await self.newRound(i=i)
        
    async def newRound(self, i : discord.Interaction):
        ''' sets up a new round of blackjack'''
        try:
            if self.getPhase() == "BETTING":
                await i.channel.send(content=f"Current Balance: {self.getBalance()} \n Enter bet in increments of 10, under 1000: ")
                input : discord.Message = await self.client.wait_for("message", check=lambda message : message.author == i.user)
                result = int(input.content)
                print(result)
                if result > 1000 or result <= 0 or result % 10 != 0:
                    raise Exception("Not valid number")
                self.gameData = UrlUtil.bet(result).json() 
            self.boardMsg = await (i.channel.send(embed=formatEmbed(gameData=self.gameData)))
            await i.followup.send(view=GameUI(),ephemeral=True)
        except:
            await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
        
            