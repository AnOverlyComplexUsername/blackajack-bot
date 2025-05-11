import os
from typing import Final
import discord 
from discord import Button, Intents, Client 
from discord.ext import commands
from dotenv import load_dotenv

import UrlUtil 
import blackjackGUI as gui
#from jsonFormatter import formatEmbed
from GameBoard import GameBoard

#get api token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
SRVRID: Final = discord.Object(id=os.getenv('SERVER_ID'))

# TODO: add normal resuming of gameplay via drop down menu + left right; maybe add seperate data base for storing discord user side stuff (?) 
    
#bot setup
intents: Intents = Intents.all()
intents.message_content = True
client : Client = commands.Bot(command_prefix="gaf9403i",intents=intents, )

gameBoard : GameBoard = GameBoard(client=client)
    
    #commands
@client.tree.command(name="start_new_game", guild=SRVRID)
async def start_game(i:discord.Interaction):
    '''Starts a new game or resumes most recent game'''
    global gameBoard
    response = UrlUtil.startGame()
    gameData : dict = response.json()
    sessionID = gameData.get("sessionId")
    print(sessionID)
    UrlUtil.setGameID(sessionID)
    await i.response.send_message(content="Starting game...",ephemeral=True)
    try:
        await gameBoard.startNewGame(i=i,gameData=gameData)  
        await i.followup.send(view=gui.GameUI(),ephemeral=True)
    except:
        await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   
   
@client.tree.command(name="resume_session", guild=SRVRID)
async def resume_session(i:discord.Interaction):
    UrlUtil.resumeGame("ca32e56c-455b-45e0-aaf6-0910929b0ffb")
    response = UrlUtil.resetGame()
    gameData : dict = response.json()
    await i.response.send_message(content="Resuming game...",ephemeral=True)
    await gameBoard.continueGame(i=i, gameData=gameData)


  
@client.tree.command(name="list_sessions", guild=SRVRID)
async def list_sessions(i:discord.Interaction):
    '''Returns list of ongoing sessions'''
    response = UrlUtil.getGameSessions()
    sessions = response.json() # a list of dictionaries
    embedVar = discord.Embed(title="Active Sessions", color=0x00ff00)
    for c in range(25):
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