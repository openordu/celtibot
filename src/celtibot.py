#!/usr/bin/python3
from pprint import pprint
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--date", help="set now date in %m-%d / mm-dd format.")
args = parser.parse_args()

def scriptDirectory(file = __file__):
    import os
    return str(os.path.dirname(os.path.realpath(file)))

def currentDirectory():
    import os
    return os.getcwd()

def yamlRead(yamlFileByName):
    import yaml, sys
    with open(yamlFileByName, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

def flatten(item):
    if len(item) == 0:
        return item 
    if isinstance(item[0], list):
        return flatten(item[0]) + flatten(item[1:])
    return item[:1] + flatten(item[1:])

def formatName(name):
    if type(name) == type([]): return name[0]
    if type(name) == type(''): return name

def findDatetimeFromWords(dateString, verb, dayOfTheWeek, words):
    import datetime
    current_time = datetime.datetime.now()
    current_year = current_time.strftime('%Y')
    current_month = current_time.strftime('%m')
    current_day = current_time.strftime('%d')

    day = dateString.split('-')[1]
    month = dateString.split('-')[0]

    date = datetime.datetime.strptime("%s-%s" % (dateString, current_year), '%m-%d-%Y')

    temporalWords = {
        'first': 1,
        'second': 2,
        'third': 3,
        'fourth': 4,
        'last': -1
    }

    daysOfTheWeek = {
        'sunday': 6,
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5
    }
    tally = 0
    while True:
        try:
            if tally == temporalWords[words[0]]:
                break
            if verb == 'after':
                date += datetime.timedelta(days=1)
                if date.weekday() == daysOfTheWeek[dayOfTheWeek]:
                    tally += 1
            elif verb == 'before':
                date -= datetime.timedelta(days=1)
                if date.weekday() == daysOfTheWeek[dayOfTheWeek]:
                    tally -= 1
        except OverflowError:
            print("OverflowError on day:`%s', try 'last'" % " ".join(words))
            return False
    return date

def dateFromWords(dateString):
    import datetime
    words = dateString.split(' ')
    if words[0] not in ['first', 'second', 'third', 'fourth','easter', 'last']:
        return False
    else:
        if words[0] == 'easter':
            if words[-2] == '-':
                newDate = calcEasterDate(datetime.datetime.now().strftime('%Y')) - datetime.timedelta(days=int(words[-1]))
                newDateString = newDate.strftime('%m-%d')
                return newDateString
            if words[-2] == '+':
                return (calcEasterDate(datetime.datetime.now().strftime('%Y')) + datetime.timedelta(days=int(words[-1])))
        elif words[0] in ['first', 'second', 'third', 'fourth', 'last']:
            date = words[-1]
            verb = words[-2]
            dayOfTheWeek = words[1]
            returnDate = findDatetimeFromWords(date, verb, dayOfTheWeek, words)
            return returnDate.strftime('%m-%d')
        else:
            return False
    
def isDateToday(dateString):
    from datetime import datetime
    if args.date:
        try:
            current_time = datetime(int(datetime.now().strftime('%Y')),int(args.date.split("-")[0]),int(args.date.split("-")[1]))
        except ValueError:
            print('That date doesn\'t exist')
            sys.exit(1)
    else:
        current_time = datetime.now()
    
    if not matchDateFormat(dateString):
            newDateString = dateFromWords(dateString)
    else: newDateString = None
    if current_time.strftime('%m-%d') in [dateString, newDateString]:
        return True
    return False

def getStuffAboutToday(yamlListOfHolidays):
    holidays = list()
    for item in yamlListOfHolidays['holidays']:
       
        dateString = item['date'] if 'date' in item.keys() else item['day']

        if isDateToday(dateString):
            holidays.append(item)
    return holidays

def calcEasterDate(year):
    import datetime
    """returns the date of Easter Sunday of the given yyyy year"""
    y = int(year)
    # golden year - 1
    g = y % 19
    # offset
    e = 0
    # century
    c = y/100
    # h is (23 - Epact) mod 30
    h = (c-c/4-(8*c+13)/25+19*g+15)%30
    # number of days from March 21 to Paschal Full Moon
    i = h-(h/28)*(1-(h/28)*(29/(h+1))*((21-g)/11))
    # weekday for Paschal Full Moon (0=Sunday)
    j = (y+y/4+i+2-c+c/4)%7
    # number of days from March 21 to Sunday on or before Paschal Full Moon
    # p can be from -6 to 28
    p = i-j+e
    d = int(1+(p+27+(p+6)/40)%31)
    m = int(3+(p+26)/30)
    return datetime.date(y,m,d)
  
    if year in special_years:
        dateofeaster = (22 + d + e) - specyr_sub
    else:
        dateofeaster = 22 + d + e
    return dateofeaster

def matchDateFormat(dateString):
    import re
    if re.match(r'\d{2}-\d{2}', dateString):
        return True
    return False

def tooter(toot):
    from mastodon import Mastodon
    mastodon = Mastodon(access_token = 'thetoken')
    # mastodon.toot(toot)

def makeHolidayToots(holiday):
    holidayName     = holiday['name']
    blessName       = holiday['blessname'] if 'blessname' in holiday.keys() else holidayName
    scottishName    = formatName(holiday['scottishname']) if 'scottishname' in holiday.keys() else None
    gaulishName     = formatName(holiday['gaulishname']) if 'gaulishname' in holiday.keys() else None
    irishName       = formatName(holiday['irishname']) if 'irishname' in holiday.keys() else None
    cornishName     = formatName(holiday['cornishname']) if 'cornishname' in holiday.keys() else None
    bretonName      = formatName(holiday['bretonname']) if 'bretonname' in holiday.keys() else None
    welshName       = formatName(holiday['welshname']) if 'welshname' in holiday.keys() else None
    hashTags        = set(holiday['tags']) if 'tags' in holiday.keys() else []
    reconstructed   = holiday['reconstructed'] if 'reconstructed' in holiday.keys() else False
    
    celticNames     = {'gaulish':gaulishName,'scottish':scottishName, 'irish': irishName, 'cornish': cornishName, 'breton': bretonName, 'welsh': welshName}
    celticNames     = {key:val for key, val in celticNames.items() if val != None}

    string = "Today is %s!\n" % (holidayName)

    if len(celticNames):
        string += "\nNames for today in Celtic languages:\n"

    for key, name in celticNames.items():
        string += "#%s `%s'\n" % (key.capitalize(),name)

    string += "\nCeltibot wishes blessings on %s to all those who keep it.\n" % blessName
    while len(hashTags):
        tag = list(hashTags)[0]
        string += "#%s " % hashTags.pop()
    string += "#celtic #celtibot #CelticCalendar"
    if reconstructed == True:
            string += "\n\n\nnote: contains some reconstructed elements"
    return string

def init():
    import os, datetime
    toots = dict()

    # holidays
    holidayObjectsFromYamlFile = yamlRead('%s/../data/cal/holidays.yaml' % str(scriptDirectory()))
    relevantHolidaysFromFile = getStuffAboutToday(holidayObjectsFromYamlFile)
    for i in range(len(relevantHolidaysFromFile)):
        holiday = relevantHolidaysFromFile[i]
        toots[i] = makeHolidayToots(holiday)

    # moons
    # no moons yet

    # quotes

    quoteObjectsFromYamlFile = yamlRead('%s/../data/quotes/quotes.yaml' % str(scriptDirectory()))
    try:
        todaysquote = quoteObjectsFromYamlFile[datetime.datetime.now().strftime('%j')-1]
        quote = "`%s' - %s, %s " % (todaysquote['text'], todaysquote['author'], todaysquote['source'])
        hashTags = set(todaysquote['tags']) if 'tags' in todaysquote.keys() else []

        if len(hashTags): quote += "\n"
        while len(hashTags):
            tag = list(hashTags)[0]
            quote += "#%s " % hashTags.pop()
        quote += "#celtic #celtibot #CelticQuotes"
        toots[len(toots)] = quote
    except TypeError:
        # No quotes for today
        pass

    try:
        print(toots)
    except:
        pass
init()