import os
from typing import Final
import discord 
from discord import Intents, Client 
from discord.ext import commands

from dotenv import load_dotenv

#get api token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
SRVRID: Final = discord.Object(id=os.getenv('SERVER_ID'))
USERNAME : Final[str] = os.getenv('USERNAME')
PASSWORD : Final[str] = os.getenv('PASSWORD')
ID = None
API_URL = f"http://euclid.knox.edu:8080/api/blackjack/{id}/hit?username={username}&password={password}"


#bot setup
intents: Intents = Intents.all()
intents.message_content = True
client : Client = commands.Bot("",intents=intents, )


    
    #commands
@client.tree.command(name="start_game", guild=SRVRID)
async def set_channel(i:discord.Interaction):
    '''channel in which the bot will post the interface messages'''
    
    await i.response.send_message("channel selected!")
    
#entry point
def startDiscord() -> None:
    client.run(token=TOKEN)
    client.clear()
    
startDiscord()