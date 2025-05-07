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

#bot setup
intents: Intents = Intents.all()
intents.message_content = True
client : Client = commands.Bot("",intents=intents, )


    
    #commands
@client.tree.command(name="hello", guild=SRVRID)
async def sayHello(i:discord.Interaction):
    await i.response.send_message("kys")
    
#entry point
def startDiscord() -> None:
    client.run(token=TOKEN)
    client.clear()