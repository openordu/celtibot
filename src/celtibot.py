#!/usr/bin/env python3

# Feature requests
# * Post images that are celtic language related
# * boost followers celtic posts based on tags
# * links with images / posts the image
# * celtic word of the day freakout / celbration post
# * prefixes entity strings with tag '#'

from pprint import pprint
import sys, datetime
from os import environ as env
import random
import math
import textwrap
import requests
import argparse
from dateutil.easter import *

allModes = ['holiday', 'quote', 'topic', 'follow']
tootModes =  ['holiday', 'topic', 'quote']

parser = argparse.ArgumentParser()
parser.add_argument("--dryrun", help="on/off/True/False",default="0",metavar='DRYRUN')
parser.add_argument("--date", help="set now date in %m-%d / mm-dd format.",default="%s-%s" % (datetime.datetime.now().strftime('%m'), datetime.datetime.now().strftime('%d')),metavar='DATE')
parser.add_argument("--pod", help="part of day",default=None,metavar='PARTOFDAY')
parser.add_argument("--mode", help="must be one of %s" % " ".join(allModes),default=str('holiday'),metavar='INFO')

args = parser.parse_args()
current_year = int(datetime.datetime.now().strftime('%Y'))
day = int(str(args.date).split('-')[1])
month = int(str(args.date).split('-')[0])

partOfDay = int(args.pod) if args.pod != None else None

if partOfDay == None: partOfDay = 1 if datetime.date(current_year, month, day).strftime('%j') == 'am' else 2
    

doy = (int(datetime.date(current_year, month, day).strftime('%j')))-1 if partOfDay == 1 else int(datetime.date(current_year, month, day).strftime('%j'))+364

def usage():
  print("Run with -h for usage")

def switchHandler(flick):
    if flick in ['no','on', '1', 1, 'true', 'True', True]: return 1
    if flick in ['yes','off', '0', 0, 'false', 'False', False]: return 0

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
    words = dateString.split(' ')
    if words[0] not in ['first', 'second', 'third', 'fourth', 'last'] and words[-1] not in ['easter']:
        return False
    else:
        if words[-1] == 'easter':
            if words[-2] == '-':
                newDate = calcEasterDate(datetime.datetime.now().strftime('%Y')) - datetime.timedelta(days=int(words[0]))
                newDateString = newDate.strftime('%m-%d')
                return newDateString
            if words[-2] == '+':
                return (calcEasterDate(datetime.datetime.now().strftime('%Y')) + datetime.timedelta(days=int(words[0]))).strftime('%m-%d')
        elif words[0] in ['first', 'second', 'third', 'fourth', 'last']:
            date = words[-1]
            verb = words[-2]
            dayOfTheWeek = words[1]
            returnDate = findDatetimeFromWords(date, verb, dayOfTheWeek, words)
            return returnDate.strftime('%m-%d')
        else:
            return False
    
def isDateToday(dateString):
    if args.date:
        try:
            current_time = datetime.datetime(current_year, month, day)
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

def dateStringFromTextOrWords(item):
    dateString = item['date'] if 'date' in item.keys() else item['day']
    return dateString

def getHolidayObjectsForToday(yamlListOfHolidays):
    holidays = list()
    for item in yamlListOfHolidays['holidays']:
       
        dateString = dateStringFromTextOrWords(item)

        if isDateToday(dateString):
            holidays.append(item)
    return holidays

def getQuoteObjectsForToday(yamlListOfQuotes):
    quotes = list()
    for item in [x for x in yamlListOfQuotes if set(x.keys()).intersection(['day','date'])]:
        dateString = dateStringFromTextOrWords(item)
        
        if isDateToday(dateString):
            quotes.append(item)
    return quotes

def getInfoObjectsForToday(yamlListOfTopics):
    topics = list()
    for item in [x for x in yamlListOfTopics if set(x.keys()).intersection(['day','date'])]:
        
        dateString = dateStringFromTextOrWords(item)

        if isDateToday(dateString):
            topics.append(item)
    return topics

def calcEasterDate(year):
    #return datetime.datetime(easter(int(year)).strptime('%Y'),easter(int(year)).strptime('%m'),easter(int(year)).strptime('%d'))
    #date = datetime.datetime.strptime("%s-%s" % (dateString, current_year), '%m-%d-%Y')
    return easter(int(year))

def matchDateFormat(dateString):
    import re
    if re.match(r'\d{2}-\d{2}', dateString):
        return True
    return False

def shorten_url(long_url):
    api_url = "http://tinyurl.com/api-create.php"
    params = { "url": long_url }
    response = requests.get(api_url, params=params)
    return response.text

    if response.status_code == 200:
        shortened_url = response.json()["results"][long_url]["shortUrl"]
        return shortened_url
    else:
        return None

def formatHolidayToots(holiday):
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
    string += "#celtic #CelticCalendar"
    if reconstructed == True:
            string += "\n\n\nnote: contains some reconstructed elements"
    return string

def formatTopicToot(topic):
    tags = ''
    toots = []
    breakPoint = 400

    toot = "`%s' - %s\n\n%s\n" % (topic['name'], topic['summary'], shorten_url(topic['link']))
    toots = textwrap.wrap(toot, breakPoint, break_long_words=False)

    hashTags = set(topic['tags']) if 'tags' in topic.keys() else []

    tags += "\n#celtic"
    while len(hashTags):
        tag = list(hashTags)[0]
        tags += "\n#%s " % hashTags.pop()

    for toot in toots:
        toots[toots.index(toot)] = "%s%s%s" % (toot, '...' if (toots.index(toot) != len(toots)-1) else '',tags)

    if len(toots): toots[len(toots)-1] = "%s %s" % (toots[len(toots)-1], "\nnote: edit this info: https://dub.sh/FcTpgFK")
    return toots

def formatQuoteToot(quote):
    toots = []
    tags = ''
    breakPoint = 400
    toot = "`%s' - %s, %s " % (quote['text'], quote['author'], quote['source'])
    toots = textwrap.wrap(toot, breakPoint, break_long_words=False)

    
    hashTags = set(quote['tags']) if 'tags' in quote.keys() else []

    while len(hashTags):
        tag = list(hashTags)[0]
        tags += "\n#%s " % hashTags.pop()
    tags += "\n#celtic"

    tags = textwrap.wrap(tags, 100, break_long_words=False)

    for toot in toots:
        toots[toots.index(toot)] = "%s%s%s" % (toot, '...' if (toots.index(toot) != len(toots)-1) else '', tags[0])
    
    return toots

def followToots(toots):
    from mastodon import Mastodon
    mastodon = Mastodon(
        access_token = env['ACCESS_TOKEN'],
        api_base_url = env['SERVER']
    )
    # Get a list of accounts the bot is already following
    acctsTheBotFollows = mastodon.account_following(id=env['BOT_ACCOUNT_ID'], min_id=0)
    acctsTheBotFollowsIDs = [f['id'] for f in acctsTheBotFollows]
    last_followed_user = acctsTheBotFollowsIDs[-1]

    # Get a list of the bot's new followers
    acctsFollowingTheBot = mastodon.account_followers(id=env['BOT_ACCOUNT_ID'], min_id=0)


    # Get a list of the bot's new followers
    newAcctsFollowingTheBot = mastodon.account_followers(id=env['BOT_ACCOUNT_ID'], since_id=last_followed_user)
    sorted(acctsTheBotFollowsIDs)

    # Follow each new follower
    for acct in newAcctsFollowingTheBot:
        if acct['id'] not in acctsTheBotFollowsIDs:
            try:
                if int(args.dryrun) == 0: mastodon.account_follow(id=acct['id'])
                print("Followed %s." % acct['acct'])
            except:
                # User has blocked us from following them
                if int(args.dryrun) == 0: mastodon.account_remove_from_followers(acct['id'])
                print("User: %s has blocked us from following them." % acct['id'])

    # Get a list of the users you follow but do not follow you back
    non_followers = [user for user in acctsTheBotFollows if user not in acctsFollowingTheBot]

    # Unfollow the non-followers
    for user in non_followers:
        print("Unfollowing user: %s" % user['acct'])
        if int(args.dryrun) == 0:
            mastodon.account_unfollow(user["id"])

    # Roadmap for this function:
    # 1. DM new users with a link to the bot's terms of use and license

def quoteToots(toots):
    # quotes
    quoteObjectsFromYamlFile = yamlRead('%s/../data/quotes/quotes.yaml' % str(scriptDirectory()))
    todayQuotes = getQuoteObjectsForToday(quoteObjectsFromYamlFile)
    if not len(todayQuotes) or int(partOfDay) == 2:
        undatedQuotesObjects = [x for x in quoteObjectsFromYamlFile if not set(['date','day']).intersection(x.keys())]
        try:
            toots = formatQuoteToot(undatedQuotesObjects[doy])
        except IndexError:
            sys.exit()
        return toots

    for quote in todayQuotes:
        toots = formatQuoteToot(quote)
    return toots

def topicToots(toots):
    infoObjectsFromYamlFile = yamlRead('%s/../data/info/topics.yaml' % str(scriptDirectory()))
    todayTopics = getInfoObjectsForToday(infoObjectsFromYamlFile)
    if not len(todayTopics) or int(partOfDay) == 2:
        undatedInfoObjects = [x for x in infoObjectsFromYamlFile if not set(['date','day']).intersection(x.keys())]
        try:
            toots = formatTopicToot(undatedInfoObjects[doy])
        except IndexError:
            sys.exit()
        return toots
    for topic in todayTopics:
        toots = formatTopicToot(topic)
    return toots

def holidayToots(toots):
    # holidays
    holidayObjectsFromYamlFile = yamlRead('%s/../data/cal/holidays.yaml' % str(scriptDirectory()))
    relevantHolidaysFromFile = getHolidayObjectsForToday(holidayObjectsFromYamlFile)
    for i in range(len(relevantHolidaysFromFile)):
        holiday = relevantHolidaysFromFile[i]
        toots[i] = formatHolidayToots(holiday)
    return toots

def tooter(toot, replyid=0):
    from mastodon import Mastodon
    mastodon = Mastodon(
        access_token = env['ACCESS_TOKEN'],
        api_base_url = env['SERVER']
    )
    if replyid>0: return mastodon.status_post(toot, in_reply_to_id=replyid)
    else: return mastodon.status_post(toot)

def makeToots(toots):
    if len(toots) == 1: status = tooter(toots[0])
    else:
        first_toot = tooter(toots[0])
    for toot in toots:
        if toots.index(toot) == 0:
            continue
        tooter(toot, first_toot['id'])

def init():
    import os, datetime
    toots = dict()

    if args.mode in allModes:
        toots = eval("%sToots(toots)" % args.mode)
    else:
        usage()
        sys.exit(5)
    if args.mode not in tootModes: sys.exit()
    if switchHandler(args.dryrun) == 1: print(toots)
    else: makeToots(toots)
init()