from mastodon import Mastodon
from os import environ as env
from pprint import pprint


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

# Search for posts containing the hashtag
results = mastodon.search_v2(q="%s" % 'celtic')
#pprint(posts)
# Print the content of each post

sys.exit(1)
for account in results["accounts"]:
    user_info = mastodon.account_search(q=account['acct'], limit=1)

    following = mastodon.account_following(id=env['BOT_ACCOUNT_ID'])
    following_ids = [f['id'] for f in following]

    if user_info[0]['id'] not in following_ids:
        if int(args.dryrun) == 0:
            result = mastodon.account_follow(id=user_info[0]['id'])
            pprint(result)
        pprint("%s: followed user %s:%s" % (args.dryrun,account['acct'],user_info[0]['id']))
    #pprint(mastodon.search(q="celtic"))
