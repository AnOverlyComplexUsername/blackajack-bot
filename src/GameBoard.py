import discord
import UrlUtil
from jsonFormatter import formatEmbed 


class GameBoard:
    
    sesID : str = None
    board : discord.Message = None
    gameData : dict = None
    client : discord.Client= None
    
    '''wrapper class for interacting with and recieving blackjack game data'''
    def __init__(self, gameData : dict = None, boardMsg : discord.Message = None, client : discord.client = None):
        ''' Parameters
        -----------
        gameData: :class:`dict`
            dictionary of json game data
        board: :class:`Message`
            gmaeBoard message that's being used for current game
        '''
        self.gameData = gameData
        self.board = boardMsg 
        self.client = client
        if gameData:
            self.sesID = gameData.get("sessionId")

    
    def setBoardMessage(self,msg : discord.Message):
        self.board = msg
    
    def getBalance(self) -> str:
        '''returns the current player balance'''
        return str(self.gameData.get("balance"))
    
    def getPlayerValue(self) -> str:
        '''returns current player card value'''
        return str(self.gameData.get("playerValue"))
    
    def getDealerValue(self) -> str:
        '''returns current dealer card value'''
        return str(self.gameData.get("dealerValue"))
    
    def getPhase(self) -> str:
        ''' returns current state of game'''
        return self.gameData.get("phase")
            
    async def startNewGame(self, i : discord.Interaction, gameData : dict):
        '''starts new game or resumes most recent unsaved game'''
        if gameData.get("phase") == "RESOLVED":
            UrlUtil.resetGame()
        if gameData.get("phase") == "BETTING":
            self.recieveNewBet(i=i)
        self.board = await i.channel.send(embed=formatEmbed(gameData=gameData, i=i))
        
    async def continueGame(self, i : discord.Interaction, gameData : dict):
        ''' continues current game and starts a new round'''
        while True:
            try:
                if gameData.get("phase") == "RESOLVED":
                    UrlUtil.resetGame()
                    print("here")
                    self.recieveNewBet(i=i)
                    await self.board.edit(embed=formatEmbed(gameData=gameData, i=i))
                break
            except:
                await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
    
    async def recieveNewBet(self, i : discord.Interaction):
        msg = await i.channel.send(content=f"Current Balance: {self.getBalance()} \n Enter bet in increments of 10, under 1000: ")
        input : discord.Message = await self.client.wait_for("message", check=lambda message : message.author == i.user)
        result = int(input.content)
        await msg.delete()
        await input.delete()
        if result > 1000 or result <= 0 or result % 10 != 0:
            raise Exception("Not valid number")
        self.gameData = UrlUtil.bet(result)
    


    
        