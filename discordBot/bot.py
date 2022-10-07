import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()

bot = discord.Client(intents = discord.Intents.default())
token = os.getenv('TOKEN')

@bot.event
async def on_ready():
    guild_count = 0
    
    for guild in bot.guilds:
            print(f" - {guild.id} (name: {guild.name})")

            guild_count += 1
            
    print("FCC Reminder Bot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
    if message.content == "hello":
        
        await message.channel.send("hey dirtbag")

bot.run(token)

