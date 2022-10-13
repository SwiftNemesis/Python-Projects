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



def get_attendee_ids(service, now):
    
    print('Getting the next upcoming event')
    events = get_event_items(service,now)
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
    
    

def get_event_summary(service, now):
    print('Getting event details')
    events_result = get_event_items(service, now)
    events_summary = events_result[0].get('summary', [])
    return events_summary

def get_event_startTime(service, now):
    print('Getting event start time')
    events_result = get_event_items(service,now)
    

def get_event_endTime(service,now):
    print('Getting event end time')
    events_result = get_event_items(service,now)
    

