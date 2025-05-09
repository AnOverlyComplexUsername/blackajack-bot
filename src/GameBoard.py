import discord
from jsonFormatter import format, formatEmbed
import UrlUtil

class GameBoard:

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
    
    def setBoardMessage(self,msg : discord.Message):
        self.boardMsg = msg
    
    def getBalance(self) -> str:
        '''returns the balance in json schema'''
        return str(self.gameData.get("balance"))
    
    async def startNewGame(self, i : discord.Interaction):
        response = UrlUtil.startGame()
        gameData : dict = response.json()
        sessionID = gameData.get("sessionId")
        print(sessionID)
        UrlUtil.setGameID(sessionID)
        UrlUtil.resetGame()
        await i.response.send_message(content="Starting/Resuming game...",ephemeral=True)
    #  try:
        if gameData.get("phase") == "BETTING":
            await i.channel.send(content=f"Current Balance: {str(gameData.get("balance"))} \n Enter bet in increments of 10, under 1000: ")
            # input : discord.Message = await client.wait_for("message", check=lambda message : message.author == i.user)
            # result = int(input.content)
            # if result > 1000 and result < 0 and result % 10 != 0:
            #     raise Exception("Bet under 0, over 1000, or not in 10s")
            gameData = UrlUtil.bet(30).json() 
        gameBoard = await i.channel.send(embed=formatEmbed(gameData=gameData))
        await i.followup.send(view=GameUI(),ephemeral=True)
            
            