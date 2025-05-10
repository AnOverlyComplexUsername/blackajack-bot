import os
from typing import Final
import discord 
from discord import Button, Intents, Client 
from discord.ext import commands
from dotenv import load_dotenv

import UrlUtil 
import blackjackGUI as gui
import discord.ext
from jsonFormatter import formatEmbed
#import GameBoard, i=i

#get api token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
SRVRID: Final = discord.Object(id=os.getenv('SERVER_ID'))


#bot setup
intents: Intents = Intents.all()
intents.message_content = True
client : commands.Bot = commands.Bot(command_prefix="gaf9403i",intents=intents, )

gameBoard : discord.Message = None

#used for hit / stand
class GameUI(discord.ui.View):
    @discord.ui.button(label="Hit", row=0, style=discord.ButtonStyle.primary)
    async def hit_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.hit()
        await interaction.response.defer()
        if response.json().get("phase") == "RESOLVED":
            msg = await interaction.original_response()
            await msg.edit(view=EndGameUI())
        await gameBoard.edit(embed=formatEmbed(response.json(), i=interaction)), 
    @discord.ui.button(label="Stand", row=0, style=discord.ButtonStyle.primary)
    async def stand_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.stand()
        await interaction.response.edit_message(view=EndGameUI())
        await gameBoard.edit(embed=formatEmbed(response.json(),i=interaction))

# UI for game ending 
class EndGameUI(discord.ui.View):
    @discord.ui.button(label="New Game", row=0, style=discord.ButtonStyle.green)
    async def new_game_callback(self, interaction: discord.Interaction, button: Button):
        response = UrlUtil.getGameState().json()
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        await test2(i=interaction,gameData=response)
        msg = await interaction.original_response()
        await msg.edit(view=GameUI())
    @discord.ui.button(label="End Game", row=0, style=discord.ButtonStyle.red)
    async def end_game_callback(self, interaction: discord.Interaction, button: Button):
        UrlUtil.finishGame()
        await interaction.response.edit_message(delete_after=0.01)
    
#helper funciton 
async def test(i : discord.Interaction, gameData : dict):
    global gameBoard
    try:
        if gameData.get("phase") == "RESOLVED":
            UrlUtil.resetGame()
        if gameData.get("phase") == "BETTING":
            msg = await i.channel.send(content=f"Current Balance: {str(gameData.get("balance"))} \n Enter bet in increments of 10, under 1000: ")
            input : discord.Message = await client.wait_for("message", check=lambda message : message.author == i.user)
            result = int(input.content)
            await msg.delete()
            await input.delete()
            if result > 1000 or result <= 0 or result % 10 != 0:
                raise Exception("Not valid number")
            gameData = UrlUtil.bet(result).json() 
        gameBoard = await i.channel.send(embed=formatEmbed(gameData=gameData, i=i))
        await i.followup.send(view=GameUI(),ephemeral=True)
        
    except:
         await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   

async def test2(i : discord.Interaction, gameData : dict):
    global gameBoard
    try:
        if gameData.get("phase") == "RESOLVED":
            UrlUtil.resetGame()
            print("here")
            msg = await i.channel.send(content=f"Current Balance: {str(gameData.get("balance"))} \n Enter bet in increments of 10, under 1000: ")
            input : discord.Message = await client.wait_for("message", check=lambda message : message.author == i.user) 
            result = int(input.content)
            if result > 1000 or result <= 0 or result % 10 != 0:
                raise Exception("Not valid number")
            await input.delete()
            await msg.delete()
            gameData = UrlUtil.bet(result).json() 
            await gameBoard.edit(embed=formatEmbed(gameData=gameData, i=i))
    except:
         await i.followup.send(content="Error: Enter an acceptable bet", ephemeral=True)   

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
    #UrlUtil.resetGame()
    await i.response.send_message(content="Starting game...",ephemeral=True)
    await test(i=i,gameData=gameData)  
   
@client.tree.command(name="resume_session", guild=SRVRID)
async def resume_session(i:discord.Interaction):
    UrlUtil.resumeGame("ca32e56c-455b-45e0-aaf6-0910929b0ffb")
    response = UrlUtil.resetGame()
    gameData : dict = response.json()
    await i.response.send_message(content="Resuming game...",ephemeral=True)
    await test(i=i, gameData=gameData)


  
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