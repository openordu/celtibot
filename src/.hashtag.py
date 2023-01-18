# This file is retired and was used to get an initial group of followers before the searchbot controversey of mid-January 2023
from mastodon import Mastodon
from os import environ as env
from pprint import pprint
from time import sleep

from pprint import pprint
import sys, datetime
from os import environ as env
import random
import math
import textwrap
import requests
import argparse

allModes = ['holiday', 'quote', 'topic', 'follow']
tootModes =  ['holiday', 'topic', 'quote']

parser = argparse.ArgumentParser()
parser.add_argument("--dryrun", help="on/off/True/False",default="1",metavar='DRYRUN')
args = parser.parse_args()

def scriptDirectory(file = __file__):
    import os
    return str(os.path.dirname(os.path.realpath(file)))


def yamlRead(yamlFileByName):
    import yaml, sys
    with open(yamlFileByName, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

# Authenticate with Mastodon
mastodon = Mastodon(
        access_token = env['ACCESS_TOKEN'],
        api_base_url = env['SERVER']
)
# Replace HASHTAG with the desired hashtag
hashtagObjectsFromYamlFile = yamlRead('%s/../data/follow/tags.yaml' % str(scriptDirectory()))

tags = [ 'celtic', 'MastoDaoine', 'StandingStoneSunday', 'Scottish', 'Shetland', 'Welsh', 'Irish', 'Ireland', 'Scotland', 'Wales' ]
accounts = set()
for tag in hashtagObjectsFromYamlFile:
    # Search for posts containing the hashtag
    posts = mastodon.timeline(timeline='tag/%s' % tag['name'], limit=500)
    results = mastodon.search_v2(q="%s" % tag['name'], resolve=True, result_type="statuses")
    #pprint(results['statuses'])
    # Print the content of each post

    accounts = accounts.union(set([x['account']['acct'] for x in posts if x['account']['acct'] != 'celtibot']))
    accounts = accounts.union([x['acct'] for x in results["accounts"] if x['account']['acct'] != 'celtibot'])

following = mastodon.account_following(id=env['BOT_ACCOUNT_ID'])
following_ids = [f['id'] for f in following]

for account in accounts:
    user_info = mastodon.account_search(q=account, limit=1)

    if user_info[0]['id'] not in following_ids:
        if int(args.dryrun) == 0:
            result = mastodon.account_follow(id=user_info[0]['id'])
            sleep(30)
            pprint(result)
        pprint("%s: followed user %s:%s" % (args.dryrun,account,user_info[0]['id']))
    #pprint(mastodon.search(q="celtic"))

## take seed tag and search posts with those tags
## add tags to tagslist / print them so they can be added to seed tags
## 
