import discord
import UrlUtil
from blackjackGUI import GameUI
from jsonFormatter import formatEmbed 

class GameBoard:
    
    sesID = None
    '''class for interacting with and containing game and game data'''
    def __init__(self, gameData : dict = None, boardMsg : discord.Message = None):
        ''' Parameters
        -----------
        gameData: :class:`dict`
            dictionary of json game data
        boardMsg: :class:`Message`
            gmaeBoard message that's being used for current game
        '''
        self.gameData = gameData
        self.boardMsg = boardMsg 
        self.sesID = gameData.get("sessionId")
    
    def setBoardMessage(self,msg : discord.Message):
        self.boardMsg = msg
    
    def getBalance(self) -> str:
        '''returns the balance in json schema'''
        return str(self.gameData.get("balance"))
    
    def getPhase(self) -> str:
        ''' returns current state of game'''
        return self.gameData.get("phase")
    
    async def startNewGame(self, i : discord.Interaction, client : discord.Client):
        ''' intializes a new game '''
        response = UrlUtil.startGame()
        gameData : dict = response.json()
        sessionID = gameData.get("sessionId")
        print(sessionID)
        UrlUtil.setGameID(sessionID)
        UrlUtil.resetGame()
        await i.response.send_message(content="Starting/Resuming game...",ephemeral=True)
        try:
            if gameData.get("phase") == "BETTING":
                await i.channel.send(content=f"Current Balance: {str(gameData.get("balance"))} \n Enter bet in increments of 10, under 1000: ")
                input : discord.Message = await client.wait_for("message", check=lambda message : message.author == i.user)
                result = int(input.content)
                print(result)
                if result > 1000 or result <= 0 or result % 10 != 0:
                    raise Exception("Not valid number")
                gameData = UrlUtil.bet(result).json() 
            self.boardMsg = i.channel.send(embed=formatEmbed(gameData=gameData))
            await i.followup.send(view=GameUI(),ephemeral=True)
        except:
            await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
        
    async def setUpGame(self):
        ''' sets up a new round of blackjack'''
         try:
            if self.gameData.get("phase") == "BETTING":
                await i.channel.send(content=f"Current Balance: {str(gameData.get("balance"))} \n Enter bet in increments of 10, under 1000: ")
                input : discord.Message = await client.wait_for("message", check=lambda message : message.author == i.user)
                result = int(input.content)
                print(result)
                if result > 1000 or result <= 0 or result % 10 != 0:
                    raise Exception("Not valid number")
                gameData = UrlUtil.bet(result).json() 
            self.boardMsg = i.channel.send(embed=formatEmbed(gameData=gameData))
            await i.followup.send(view=GameUI(),ephemeral=True)
        except:
            await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
        
            