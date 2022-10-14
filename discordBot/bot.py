from __future__ import print_function
from email.errors import StartBoundaryNotFoundDefect
#HEADERS FOR DISCORD API
import discord, os, googleCalendarAPI
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

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

def change_to_UTC(time):
    time = time[:-6]
    time += 'Z'
    return time
#Section for Discord Bot Code
load_dotenv()

intents = discord.Intents.all()
token = os.getenv('TOKEN')

bot = discord.Client (intents=intents)

#Predeclariations for Discord Bot Function Call
channel_ID = 996591747226411018
creds = validate_google_API_credentials()
service = build('calendar', 'v3', credentials=creds)

@tasks.loop(minutes=1)
async def reminder():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    channel = bot.get_channel(channel_ID)
    items = googleCalendarAPI.get_event_items(service, now)
    event_startTime = googleCalendarAPI.get_event_startTime_zero(items)
    time_bool = googleCalendarAPI.check_time(event_startTime)
    if time_bool:
        event_attendee = googleCalendarAPI.get_attendee_ids(items) 
        event_attendee = (', '.join(str(a) for a in event_attendee))
        event_summary = googleCalendarAPI.get_event_summary(items)
        event_description = googleCalendarAPI.get_event_description(items)
        event_date = googleCalendarAPI.day_month_year(event_startTime)
        event_startTime = googleCalendarAPI.convert_time(event_startTime)
        event_endTime = googleCalendarAPI.get_event_endTime_zero(items)
        event_endTime = googleCalendarAPI.convert_time(event_endTime)
        await channel.send(f'**Attendees:** {event_attendee}\n**Summary:**\n{event_summary}\n\n**Description:** \n{event_description}\n\n**Date:** {event_date}**\nStart Time:** {event_startTime}\n**End Time:** {event_endTime}')

@bot.event
async def on_ready():
    reminder.start()

bot.run(token)


    


