from time import time
from datetime import datetime
from urlparse import urlparse, parse_qs
from facebook import GraphAPIError

from . import get_object

def get_feed(api, username):

    def get_previous(previous_url):
        previous_url_parameters = parse_qs(urlparse(previous_url).query)
        return int(previous_url_parameters['since'][0])

    def get_next(next_url):
        next_url_parameters = parse_qs(urlparse(next_url).query)
        return int(next_url_parameters['until'][0])

    profile = get_object(api, username)

    until = int(time())
    while True:

        print "Getting Feed Until: " + datetime.utcfromtimestamp(until).strftime('%Y-%m-%d %H:%M:%S')
        profile = api.get_object(username + "/feed", until=str(until))
        if profile['data'] == []:
            print "End of Results"
            break
        since = get_previous(profile['paging']['previous'])
        until = get_next(profile['paging']['next'])

        print profile['data']

        for item in profile['data']:
            print item.get('type') + ": " + item.get('story', '') + item.get('message', '')