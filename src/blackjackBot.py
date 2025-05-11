import os
from typing import Final
import discord 
from discord import Intents, Client 
from discord.ext import commands
from dotenv import load_dotenv

import UrlUtil 
from blackjackGUI import StartGameUI, SessionList
from jsonFormatter import formatSessionsEmbed
from GameBoard import GameBoard

#get api token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
SRVRID: Final = discord.Object(id=os.getenv('SERVER_ID'))

    
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
        await i.followup.send(view=StartGameUI(gameBoard),ephemeral=True)
    except:
        await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   
   
@client.tree.command(name="resume_session", guild=SRVRID)
async def resume_session(i:discord.Interaction, id : str):
    ''' resumes a game given a session ID'''
    UrlUtil.setGameID(id=id.strip())
    response = UrlUtil.resumeGame()
    gameData : dict = response.json()
    await i.response.send_message(content="Resuming game...",ephemeral=True)
    try:
        await gameBoard.startNewGame(i=i,gameData=gameData)  
        await i.followup.send(view=StartGameUI(gameBoard),ephemeral=True)
    except:
        await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   


  
@client.tree.command(name="list_sessions", guild=SRVRID)
async def list_sessions(i:discord.Interaction):
    '''Returns list of ongoing sessions from newest to oldest'''
    entryRange = 5
    sessions = UrlUtil.getGameSessions()        
    await i.response.send_message(embed=formatSessionsEmbed(sessions=sessions, startIndex= 0, entryRange=entryRange),view=SessionList(sesList=sessions,entryRange=entryRange))
    

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
    