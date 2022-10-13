import discord
import os
import googleCalendarAPI
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
token = os.getenv('TOKEN')

discord_bot = discord.Client(intents=intents)

@discord_bot.event
async def on_message(message):
    if message.content == "hello":
        await message.reply("hey dirtbag")
    elif message.content == "calendar":
        list = googleCalendarAPI.main()
        await message.reply(list)

    
discord_bot.run(token) # type: ignore


    


