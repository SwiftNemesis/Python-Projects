from os import times
from unittest import case


def get_event_items(service,now):
    event = service.events().list(calendarId='primary', maxResults=1, timeMin=now, singleEvents=True, orderBy='startTime').execute()
    events_items = event.get('items',[])
    return events_items

def convert_discord_ids(id_list):
    discordIdList = []
    for item in id_list:
        email = item.get('email')
        match email:
            case 'abid@unlv.nevada.edu':
                discordIdList.append('<@669691111693877291>')
            case 'sowerb1@unlv.nevada.edu':
                discordIdList.append('<@215953716522516480>')
            case 'rodric36@unlv.nevada.edu':
                discordIdList.append('<@106906513460756480>')
            case 'anderj12@unlv.nevada.edu':
                discordIdList.append('<@412681290761109507>')
            case 'salcem2@unlv.nevada.edu':
                discordIdList.append('<@155098435324739585>')
    return discordIdList



def get_attendee_ids(items):
    event_id = items[0].get('id')
    str(event_id)
    id_list = items[0].get('attendees', [])
    if not items:
        return
    discord_ids = convert_discord_ids(id_list)
    return discord_ids

def get_event_summary(events_result):
    events_summary = events_result[0].get('summary', [])
    return events_summary

def get_event_description(events_result):
    events_description = events_result[0].get('description', [])
    return events_description
    

def convert_time(timeString):
    import datetime
    newTime = datetime.datetime.strptime(timeString[11:16], '%H:%M').strftime('%I:%M %p')
    return newTime

def day_month_year(string):
    import calendar
    year = string[0:4]
    day = string[8:10]
    month = string[5:7]
    match month:
        case '01':
            month = calendar.month_name[1]
        case '02':
            month = calendar.month_name[2]
        case '03':
            month = calendar.month_name[3]
        case '04':
            month = calendar.month_name[4]
        case '05':
            month = calendar.month_name[5]
        case '06':
            month = calendar.month_name[6]
        case '07':
            month = calendar.month_name[7]
        case '08':
            month = calendar.month_name[8]
        case '09':
            month = calendar.month_name[9]
        case '10':
            month = calendar.month_name[10]
        case '11':
            month = calendar.month_name[11]
        case '12':
            month = calendar.month_name[12]
    
    date = f'{month} {day}, {year}'
    return date

def get_event_startTime(events_result):
    events_start = events_result[0].get('start', [])
    events_start_time = events_start.get('dateTime', [])
    return events_start_time

def get_event_endTime(events_result):
    events_end = events_result[0].get('end', [])
    events_end_time = events_end.get('dateTime')
    return events_end_time



    

