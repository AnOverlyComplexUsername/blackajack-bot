import discord
import UrlUtil
from blackjackGUI import GameUI
from jsonFormatter import formatEmbed 


class GameBoard:
    
<<<<<<< Updated upstream
    sesID = None
    '''class for interacting with and containing game and game data'''
    def __init__(self, gameData : dict = None, boardMsg : discord.Message = None, client : discord.Client = None):
=======
    sesID : str = None
    board : discord.Message = None
    gameData : dict = None
    client : discord.Client= None
    
    '''wrapper class for interacting with and recieving blackjack game data'''
    def __init__(self, gameData : dict = None, boardMsg : discord.Message = None, client : discord.client = None):
>>>>>>> Stashed changes
        ''' Parameters
        -----------
        gameData: :class:`dict`
            dictionary of json game data
<<<<<<< Updated upstream
            
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
=======
        board: :class:`Message`
            gmaeBoard message that's being used for current game
        '''
        self.gameData = gameData
        self.board = boardMsg 
        self.sesID = gameData.get("sessionId")
        self.client = client
    
    def setBoardMessage(self,msg : discord.Message):
        self.board = msg
>>>>>>> Stashed changes
    
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
<<<<<<< Updated upstream
    
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
=======
            
    async def startNewGame(self, i : discord.Interaction, gameData : dict):
        '''starts new game or resumes most recent unsaved game'''
        try:
            if gameData.get("phase") == "RESOLVED":
                UrlUtil.resetGame()
            if gameData.get("phase") == "BETTING":
                self.recieveNewBet(i=i)
            self.board = await i.channel.send(embed=formatEmbed(gameData=gameData, i=i))
            await i.followup.send(view=GameUI(),ephemeral=True)
        except:
            await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   

    async def continueGame(self, i : discord.Interaction, gameData : dict):
        ''' continues current game and starts a new round'''
        try:
            if gameData.get("phase") == "RESOLVED":
                UrlUtil.resetGame()
                print("here")
                self.recieveNewBet(i=i)
                await self.board.edit(embed=formatEmbed(gameData=gameData, i=i))
>>>>>>> Stashed changes
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

    
        