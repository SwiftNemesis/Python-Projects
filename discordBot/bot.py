from __future__ import print_function
from email.errors import StartBoundaryNotFoundDefect
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

HOURS_BEFORE = 5
#Checks the time of the next event check if it's 5 hours before
def check_time(time):
    from datetime import datetime
    import pytz
    time_int = int(time[11:13])
    time_int -= HOURS_BEFORE
    if time_int < 0:
        return False
    #Builds the string for time to compare it to the current time
    time_string = f'{time_int}:{time[14:16]}'
    time_zone = pytz.timezone('America/Los_Angeles')
    current_time = datetime.now(time_zone)
    #converts current time to be Hours and Minutes In military time
    current_time = current_time.strftime("%H:%M")
    if time_string == current_time:
        return True
    else:
        return False
    
#Section for Discord Bot Code
load_dotenv()

intents = discord.Intents.all()
token = os.getenv('TOKEN')

bot = discord.Client (intents=intents)

#Predeclariations for Discord Bot Function Call
channel_ID = 996591747226411018
creds = validate_google_API_credentials()
service = build('calendar', 'v3', credentials=creds)
now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        
@tasks.loop(minutes=1)
async def test():
    channel = bot.get_channel(channel_ID)
    items = googleCalendarAPI.get_event_items(service, now)
    event_startTime = googleCalendarAPI.get_event_startTime(items)
    time_bool = check_time(event_startTime)
    if not time_bool:
        event_attendee = googleCalendarAPI.get_attendee_ids(items)
        event_attendee = (', '.join(str(a) for a in event_attendee))
        event_summary = googleCalendarAPI.get_event_summary(items)
        event_description = googleCalendarAPI.get_event_description(items)
        event_date = googleCalendarAPI.day_month_year(event_startTime)
        event_startTime = googleCalendarAPI.convert_time(event_startTime)
        event_endTime = googleCalendarAPI.get_event_endTime(items)
        event_endTime = googleCalendarAPI.convert_time(event_endTime)
        await channel.send(f'Attendees: **{event_attendee}**\nSummary:\n**{event_summary}**\n\nDescription: \n{event_description}\n\nDate: **{event_date}**\nStart Time: **{event_startTime}**\nEnd Time: **{event_endTime}**')

@bot.event
async def on_ready():
    test.start()

bot.run(token)


    


