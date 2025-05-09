import os
from typing import Final
import discord 
from discord import Button, Intents, Client 
from discord.ext import commands
from dotenv import load_dotenv

import UrlUtil 
import blackjackGUI as gui
from jsonFormatter import formatEmbed
#import GameBoard

#get api token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
SRVRID: Final = discord.Object(id=os.getenv('SERVER_ID'))


#bot setup
intents: Intents = Intents.all()
intents.message_content = True
client : Client = commands.Bot("fianwedcushi",intents=intents, )

gameBoard : discord.Message = None

#used for hit / stand
class GameUI(discord.ui.View):
    @discord.ui.button(label="Hit", row=0, style=discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.hit()
        await interaction.response.edit_message(view=GameUI())
        await gameBoard.edit(embed=formatEmbed(response.json()))
        #await gameBoard.reply(view=GameUI())
    @discord.ui.button(label="Stand", row=0, style=discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.stand()
        await interaction.response.edit_message(view=EndGameUI())
        await gameBoard.edit(embed=formatEmbed(response.json()))


class EndGameUI(discord.ui.View):
    @discord.ui.button(label="New Game", row=0, style=discord.ButtonStyle.green)
    async def new_game_callback(self, interaction: discord.Interaction, button: Button):
        global gameBoard
        response = UrlUtil.resetGame()
        await interaction.response.edit_message(delete_after=0.01)
        await gameBoard.edit(embed=formatEmbed(response.json()))
        gameBoard = await interaction.channel.send(view=GameUI())
        start_game(interaction)
    @discord.ui.button(label="End Game", row=0, style=discord.ButtonStyle.red)
    async def end_game_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.finishGame()
        await interaction.response.edit_message(delete_after=0.01)
        await gameBoard.edit(embed=formatEmbed(response.json()))
    
    #commands


@client.tree.command(name="start_new_game", guild=SRVRID)
async def start_game(i:discord.Interaction):
    global gameBoard
    '''Starts a new game or resumes most recent game'''
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
   # except:
    #   await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   
   
    
    
@client.tree.command(name="test_ui", guild=SRVRID)
async def test_ui(i:discord.Interaction):
    '''Starts a game using the most recent session'''
    # response = requests.get(util.startGame())
    # sessions : dict = response.json()
    # for s in sessions:
    #     sessions
    await i.response.send_message("AAAA", view=gui.MyView())
    await i.channel.send("pick a session: ")
    # def check(m):
    #     return m.content == 'hello' and m.channel == i.channel
    # await client.wait_for('message', check=check)
    # await i.channel.send("no")
    
@client.tree.command(name="list_sessions", guild=SRVRID)
async def list_sessions(i:discord.Interaction):
    '''Returns list of ongoing sessions'''
    response = UrlUtil.getGameSessions()
    sessions = response.json() # a list of dictionaries
    embedVar = discord.Embed(title="Active Sessions", color=0x00ff00)
    for c in range(sessions.__len__()):
        embedVar.add_field(name=f"Session {c}, ID:", value=sessions[c].get("sessionId") + f"\n Balance: " + str(sessions[c].get("currentBet")), inline=False)
        
    await i.response.send_message(embed=embedVar)
    

#handling startup
@client.event
async def on_ready() -> None:
     print(f'{client.user} is now running!')
     try:
         synced = await client.tree.sync(guild=SRVRID)
         print(f"Synced {len(synced)} commands")
     except Exception as e:
         print(e)
             
#entry point
def startDiscord() -> None:
    client.run(token=TOKEN)
    client.clear()
    
startDiscord()