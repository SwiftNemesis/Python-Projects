from os import times


def get_event_items(service,now):
    event = service.events().list(calendarId='primary', maxResults=1, timeMin=now, singleEvents=True, orderBy='startTime').execute()
    events_items = event.get('items',[])
    return events_items

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



def get_attendee_ids(items):
    
    print('Getting the attendee ids')
    #Pulls event id using the 'id' identifier in the array
    event_id = items[0].get('id')
    str(event_id)

    id_list = items[0].get('attendees', [])
    
    if not items:
        print('No upcoming events found.')
        return
    
    discord_ids = convert_discord_ids(id_list)
    return discord_ids

def get_event_summary(events_result):
    print('Getting event details')
    events_summary = events_result[0].get('summary', [])
    return events_summary

def get_event_description(events_result):
    print('Getting event summary')
    events_description = events_result[0].get('description', [])
    return events_description
    

def convert_time(timeString):
    import datetime
    newTime = datetime.datetime.strptime(timeString[11:16], '%H:%M').strftime('%I:%M %p')
    return newTime

def get_event_startTime(events_result):
    print('Getting event start time')
    events_start = events_result[0].get('start', [])
    events_start_time = events_start.get('dateTime', [])
    #events_start_time = convert_time(events_start_time)
    return events_start_time

def get_event_endTime(events_result):
    print('Getting event end time')
    events_end = events_result[0].get('end', [])
    events_end_time = events_end.get('dateTime')
    #events_end_time = convert_time(events_end_time)
    return events_end_time


    

