import discord
import UrlUtil
from jsonFormatter import formatEmbed 



class GameBoard:
    
    sesID : str = None
    board : discord.Message = None
    data : dict = None
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
        self.data = gameData
        self.board = boardMsg 
        self.client = client
        if gameData:
            self.sesID = gameData.get("sessionId")

        self.data = gameData
        self.board = boardMsg 
        self.client = client
        if gameData:
            self.sesID = gameData.get("sessionId")

    def setBoardMessage(self,msg : discord.Message):
        ''' sets current board being used'''
        self.board = msg
    
    def getBoardMessage(self):
        ''' returns current board being used'''
        return self.board 
        
    def setGameData(self, data : dict):
        '''updates and sets game data'''
        self.data = data
    
    def getBalance(self) -> str:
        '''returns the current player balance'''
        return str(self.data.get("balance"))

    def getPlayerValue(self) -> int:
        '''returns current player card value'''
        return UrlUtil.getGameState().get("playerValue")
    
    def getDealerValue(self) -> int:
        '''returns current dealer card value'''
        return UrlUtil.getGameState().get("dealerValue")
    
    def getPhase(self) -> str:
        ''' returns current state of game'''
        return UrlUtil.getGameState().get("phase")
            
    async def startNewGame(self, i : discord.Interaction, gameData : dict):
        '''starts new game or resumes most recent unsaved game'''
        self.setGameData(gameData)
        if gameData.get("phase") == "RESOLVED":
            UrlUtil.resetGame()
        if gameData.get("phase") == "BETTING":
            await self.recieveNewBet(i=i)
        self.board = await i.channel.send(embed=formatEmbed(gameData=self.data, i=i))
        
    async def continueGame(self, i : discord.Interaction, gameData : dict):
        ''' continues current game and starts a new round'''
        self.setGameData(gameData)
        
        while True:
            try:
                if gameData.get("phase") == "RESOLVED":
                    UrlUtil.resetGame()
                    await self.recieveNewBet(i=i)
                    await self.board.edit(embed=formatEmbed(gameData=self.data, i=i))
                break
            except:
                await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
    
    async def recieveNewBet(self, i : discord.Interaction) -> dict:
        '''recieves and sends the new bet, returning game state result'''
        msg = await i.channel.send(content=f"Current Balance: {self.getBalance()} \n Enter bet in increments of 10, under 1000: ")
        input : discord.Message = await self.client.wait_for("message", check=lambda message : message.author == i.user)
        result = int(input.content)
        await msg.delete()
        await input.delete()
        if result > 1000 or result <= 0 or result % 10 != 0:
            raise Exception("Not valid number")
        self.data = UrlUtil.bet(result)

    


    
        