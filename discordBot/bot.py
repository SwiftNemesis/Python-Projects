from __future__ import print_function
#HEADERS FOR DISCORD API
import discord, asyncio, os, googleCalendarAPI
from discord.ext import commands, tasks
from dotenv import load_dotenv

#HEADERS FOR GOOGLE CALENDAR API
from calendar import calendar

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#Validates the google_API credentials
#Provided by the Google Calendar API Code Snippet at <https://developers.google.com/calendar/api/quickstart/python>
def validate_google_API_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

#Section for Discord Bot Code
load_dotenv()

intents = discord.Intents.all()
token = os.getenv('TOKEN')

discord_bot = discord.Client(intents=intents)
bot = commands.Bot('!', intents=intents)

# @discord_bot.event
# async def on_message(message):
#     creds = validate_google_API_credentials()
#     if message.content == "hello":
#         await message.reply("hey dirtbag")
#     elif message.content == "calendar":      
#         service = build('calendar', 'v3', credentials=creds)
#         now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#         list = googleCalendarAPI.get_attendee_ids(service, now)
#         for item in list:
#             await message.reply(f'{item}')

        
channel_ID = 1027272274027499573
@tasks.loop(minutes=1)
async def called_once_a_minute():
    #Validates google credentials
    creds = validate_google_API_credentials()
    #Pulls ID for channel
    message_channel = bot.get_channel(channel_ID)
    #Prints the channel ID
    print(f"Got channel {message_channel}")
    #Builds calendar service object
    service = build('calendar', 'v3', credentials=creds)
    #Grabs current time
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    #Grabs list of attendee's
    list = googleCalendarAPI.get_attendee_ids(service, now)
    for item in list:
            await message_channel.send(f'{item}')

@called_once_a_minute.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished Waiting")

called_once_a_minute.start()
bot.run(token)
discord_bot.run(token) # type: ignore


    


