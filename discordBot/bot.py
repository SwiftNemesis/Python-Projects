import discord
import os
import googleCalendar
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
token = os.getenv('TOKEN')

discord_bot = discord.Client(intents=intents)

@discord_bot.event
async def on_message(message):
    if message.content == "hello":
        await message.reply("hey dirtbag")

    
discord_bot.run(token) # type: ignore


    

googleCalendar.main()
