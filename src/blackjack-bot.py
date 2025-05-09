import os
from typing import Final
import discord 
from discord import Button, Intents, Client 
from discord.ext import commands
from dotenv import load_dotenv

import UrlUtil 
import blackjackGUI as gui
from jsonFormatter import formatEmbed
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

#used for hit / stand
class GameUI(discord.ui.View):
    @discord.ui.button(label="Hit", row=0, style=discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.hit()
        await interaction.response.edit_message(view=GameUI())
        await gameBoard.boardMsg.edit(embed=formatEmbed(response.json()))
        #await gameBoard.reply(view=GameUI())
    @discord.ui.button(label="Stand", row=0, style=discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.stand()
        await interaction.response.edit_message(view=EndGameUI())
        await gameBoard.getBoard().edit(embed=formatEmbed(response.json()))

# UI for game ending 
class EndGameUI(discord.ui.View):
    @discord.ui.button(label="New Game", row=0, style=discord.ButtonStyle.green)
    async def new_game_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.resetGame()
        await gameBoard.newRound()
        await gameBoard.getBoard().edit(embed=formatEmbed(response.json()))
        
    @discord.ui.button(label="End Game", row=0, style=discord.ButtonStyle.red)
    async def end_game_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.finishGame()
        await interaction.response.edit_message(delete_after=0.01)
        await gameBoard.getBoard().edit(embed=formatEmbed(response.json()))
    
    #commands


@client.tree.command(name="start_new_game", guild=SRVRID)
async def start_game(i:discord.Interaction):
    '''Starts a new game or resumes most recent game'''
    await gameBoard.startNewGame(i=i)  
   
  
  
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