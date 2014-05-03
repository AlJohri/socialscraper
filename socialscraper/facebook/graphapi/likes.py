from time import time
from datetime import datetime
from ...base import ScrapingError

from . import get_object
from . import get_connections

def get_likes(api, username):
    profile = get_connections(api, username, 'likes')
    return profile


def get_likes(api, username):
    after = ''
    while True:
        profile = api.get_object(username + "/likes", after=after)

        if profile['data'] == []:
            print "End of Results"
            break
        after = profile['paging']['cursors']['after']

        for item in profile['data']:
        	print item.get('name'), item.get('category'), item.get('id')
            # print item.get('type') + ": " + item.get('story', '') + item.get('message', '')