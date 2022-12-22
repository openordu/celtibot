#!/usr/bin/python3
from pprint import pprint

def yamlRead(yamlFileByName):
    import yaml, sys
    with open(yamlFileByName, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)


def tooter(toot):
    from mastodon import Mastodon
    mastodon = Mastodon(access_token = 'thetoken')
    # mastodon.toot(toot)

def flatten(item):
    if len(item) == 0:
        return item 
    if isinstance(item[0], list):
        return flatten(item[0]) + flatten(item[1:])
    return item[:1] + flatten(item[1:])

def formatName(name):
    if type(name) == type([]): return name[0]
    if type(name) == type(''): return name

def isDateToday(dateString):
    from datetime import datetime
    current_time = datetime.now()
    if current_time.strftime('%m-%d') != dateString: return False
    return True

def getStuffAboutToday(yamlListOfHolidays):
    # pprint(yamlListOfHolidays['holidays'])
    holidays = list()
    for item in yamlListOfHolidays['holidays']:
       
        date = item['date'] if 'date' in item.keys() else None

        if isDateToday(date):
            holidays.append(item)
    return holidays

def makeHolidayToots(holiday):
    holidayName     = holiday['name']
    scottishName    = formatName(holiday['scottishname']) if 'scottishname' in holiday.keys() else None
    irishName       = formatName(holiday['irishname']) if 'irishname' in holiday.keys() else None
    cornishName     = formatName(holiday['cornishname']) if 'cornishname' in holiday.keys() else None
    bretonName      = formatName(holiday['bretonname']) if 'bretonname' in holiday.keys() else None
    welshName       = formatName(holiday['welshname']) if 'welshname' in holiday.keys() else None

    holidayGreeting = "Happy day."

    string = "Today is %s! %s" % (holidayName, holidayGreeting)
    return string

def init():
    toots = dict()
    yamlObjectFromFile = yamlRead('../data/cal/holidays.yaml')
    relevantHolidaysFromFile = getStuffAboutToday(yamlObjectFromFile)
    for i in range(len(relevantHolidaysFromFile)):
        holiday = relevantHolidaysFromFile[i]
        toots[i] = makeHolidayToots(holiday)
    pprint(toots)

init()