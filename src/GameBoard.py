import discord
import UrlUtil
from jsonFormatter import formatEmbed 
from UrlUtil import UrlUtil


class GameBoard:
    
    session : UrlUtil  = UrlUtil()
    board : discord.Message = None
    data : dict = None
    client : discord.Client= None
    
    '''wrapper class for interacting with and recieving blackjack game data'''
    def __init__(self, gameData : dict = None, boardMsg : discord.Message = None, client : discord.client = None):
        ''' Parameters
        -----------
        gameData: :class:`dict`
            dictionary of JSON game data  
        board: :class:`Message`
            gameBoard message that's being used for current game  
        client: :class`client`
            current discord bot client being used
        '''
        self.data = gameData
        self.board = boardMsg 
        self.client = client
        if gameData:
            self.session.setGameID(id=self.data.get("sessionId"))

    def setSessionID(self, id : str):
        '''sets session ID'''
        self.session.setGameID(id=id)

    def getSessionID(self) -> str:
        '''returns current session ID'''
        return self.session.getGameID()

    def setBoardMessage(self,msg : discord.Message):
        ''' sets current board being used'''
        self.board = msg
    
    def getBoardMessage(self):
        ''' returns current board being used'''
        return self.board 
        
    def setGameData(self, data : dict):
        '''updates and sets game data'''
        self.data = data
    
    def getGameData(self) -> dict:
        return self.data
    
    def getBalance(self) -> str:
        '''returns the current player balance'''
        return str(self.data.get("balance"))

    def getPlayerValue(self) -> int:
        '''returns current player card value'''
        return self.session.getGameState().get("playerValue")
    
    def getDealerValue(self) -> int:
        '''returns current dealer card value'''
        return self.session.getGameState().get("dealerValue")
    
    def getPhase(self) -> str:
        ''' returns current state of game'''
        return self.data.get("phase")
    
    def getSession(self) -> UrlUtil:
        '''returns current url utility used for interacting w/ game'''
        return self.session
            
    async def startNewGame(self, i : discord.Interaction, gameData : dict = None):
        '''starts new game or resumes most recent unsaved game'''
        if gameData: self.setGameData(gameData)
        else: self.setGameData(self.session.startGame().json())
        self.setSessionID(self.data.get("sessionId"))
        if self.getPhase() == "RESOLVED":
            self.session.resetGame()
        if self.getPhase() == "BETTING":
            while True:
                try:
                    await self.recieveNewBet(i=i)
                    break
                except:
                    await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
                
        self.setBoardMessage(await i.channel.send(embed=formatEmbed(gameData=self.data, i=i)))
        
    async def resumeGame(self, i : discord.Interaction, id : str):
        '''resumes a game given a game ID'''
        self.setSessionID(id=id)
        self.session.resumeGame()
        self.setGameData(self.session.getGameState())
        if self.getPhase() == "RESOLVED":
            self.session.resetGame()
        if self.getPhase() == "BETTING":
            while True:
                try:
                    await self.recieveNewBet(i=i)
                    break
                except:
                    await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
                
        self.setBoardMessage(await i.channel.send(embed=formatEmbed(gameData=self.data, i=i)))
    
    async def continueGame(self, i : discord.Interaction, gameData : dict):
        ''' continues current game and starts a new round'''
        self.setGameData(gameData)
        while True:
            try:
                if gameData.get("phase") == "RESOLVED":
                    self.session.resetGame()
                    await self.recieveNewBet(i=i)
                    await self.board.edit(embed=formatEmbed(gameData=self.data, i=i))
                break
            except:
                await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)
    
    async def recieveNewBet(self, i : discord.Interaction) -> dict:
        '''recieves new bet by awaiting user's new bet in Discord, sends new bet and returns game state result'''
        msg = await i.channel.send(content=f"Current Balance: {self.getBalance()} \n Enter bet in increments of 10, under 1000: ")
        input : discord.Message = await self.client.wait_for("message", check=lambda message : message.author == i.user)
        result = int(input.content)
        await input.delete()
        await msg.delete()
        if result > 1000 or result <= 0 or result % 10 != 0:
            raise Exception("Not valid number")
        self.data = self.session.bet(result)

    


    
        