import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.messages = True
bot = discord.Client(intents=intents)


token = os.getenv('TOKEN')

@bot.event
async def on_ready():
    guild_count = 0
    
    for guild in bot.guilds:
            print(f" - {guild.id} (name: {guild.name})")

            guild_count += 1
            
    print("FCC Reminder Bot is in " + str(guild_count) + " guilds.")

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

bot.run(token)

