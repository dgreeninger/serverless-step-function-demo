# importing the requests library
import requests
from pprint import pprint
import json
import time
import datetime
import os

def main(event, context):
    # defining global variables
    today = datetime.datetime.now()
    runtime = float(str(today.hour)+'.'+str(today.minute))

    ts = time.time()
    three_hours_ago = ts - 3*3600

    # defining the api-endpoint
    channel_endpoint = "https://slack.com/api/conversations.history?token="
    user_endpoint = "https://slack.com/api/users.info?token="
    channel = '&channel=C8UBSDL23'
    # your API key here
    api_key = os.environ['slackApiKey']
    now = "&latest="+str(ts)
    b_bots = ['anelavelly',
              'etrpchevska',
              'dnguyen',
              'dgreeninger',
              'hrychlik',
              'fbidanjiri',
              'jmcmillan',
              'slackbot',
              'tfruzza']
    # sending post request and saving response as response object
    r = requests.get(url=channel_endpoint+api_key+channel+now+"&limit=10")

    # extracting response text
    response = r.text
    # print("The slack return is:%s" % response)
    channel_json = json.loads(response)
    user_array = []
    for message in channel_json['messages']:
        try:
            user = "&user="+message['user']
            u = requests.get(url=user_endpoint+api_key+user)
            user_json = json.loads(u.text)
            updated_time = message['ts']
            print(updated_time)
            print(three_hours_ago)

            if float(three_hours_ago) < float(updated_time):
                print('posted today')
                if (user_json['user']['name'] in user_array):
                    print('already exists')
                else:
                    user_array.append(user_json['user']['name'])
            else:
                print('posted yesterday')
        except KeyError:
            # pprint(message)
            print('no user')

    user_count = len(user_array)
    lazy_bots = len(b_bots) - user_count
    pprint(user_array)
    site_values = {}
    site_values['result'] = [runtime, user_count, lazy_bots]
    site_values['state'] = 'success'
    if int(today.hour) >= 20:
        site_values['state'] = 'complete'
    return site_values
