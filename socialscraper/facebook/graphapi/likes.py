import logging
from time import time
from datetime import datetime
from ...base import ScrapingError
from ..models import FacebookPage

from . import get_object
from . import get_connections

logger = logging.getLogger(__name__)

def get_likes(api, username):
    profile = get_connections(api, username, 'likes')
    return profile


def get_likes(api, username):
    after = ''
    while True:
        profile = api.get_object(username + "/likes", after=after, fields="category,id,name,username")
        if profile['data'] == []: break
        after = profile['paging']['cursors']['after']
        for item in profile['data']:
            yield FacebookPage(page_id=int(item.get('id')), username=item.get('username') ,type=item.get('category'), name=item.get('name'))
            # print item.get('type') + ": " + item.get('story', '') + item.get('message', '')