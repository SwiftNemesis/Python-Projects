from __future__ import print_function
from calendar import calendar

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']



def convert_discord_ids(id_list):
    
    discordIdList = []
    for item in id_list:
        temp = item.get('email')
        if temp == 'abid@unlv.nevada.edu':
            print("Mehdi Abid")
            discordIdList.append('<@669691111693877291>')
        elif temp == 'sowerb1@unlv.nevada.edu':
            print("Bryce Sowers")
            discordIdList.append('<@215953716522516480>')
        elif temp == 'rodric36@unlv.nevada.edu':
            print("Christian Rodriguez")
            discordIdList.append('<@106906513460756480>')
        elif temp == 'anderj12@unlv.nevada.edu':
            print("Jorge Anderson")
            discordIdList.append('<@412681290761109507>')
        elif temp == 'salcem2@unlv.nevada.edu':
            print("Mathew Salcedo")
            discordIdList.append('<@155098435324739585>')
        else:
            print("No valid Emails")
    
    return discordIdList



def get_attendee_ids(service, now):
    
    print('Getting the next upcoming event')
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])
    #Pulls event id using the 'id' identifier in the array
    event_id = events[0].get('id')
    str(event_id)
    
    attendee_id_list = service.events().get(calendarId='primary', eventId=event_id).execute()

    id_list = attendee_id_list.get('attendees', [])
    
    if not events:
        print('No upcoming events found.')
        return
    
    
    for id in id_list:
            list = id.get('email', [])
            print(list)
    
    discord_ids = convert_discord_ids(id_list)
    return discord_ids
    # Prints the start and name of the next 10 events
    #for event in events:
        #start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start, event['summary'])
    
    


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        email_list = get_attendee_ids(service, now)

    except HttpError as error:
        print('An error occurred: %s' % error)

    return email_list

if __name__ == '__main__':
    main()