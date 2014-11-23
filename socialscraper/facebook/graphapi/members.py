import logging, requests
from time import time
from datetime import datetime
from ...base import ScrapingError
from ..models import FacebookUser

from . import get_object
from . import get_connections

logger = logging.getLogger(__name__)

def get_members(api, graph_name):
    # after = ''
    # while True:
    #     profile = api.get_object(str(username) + "/members", after=after, fields="id,username,name")
    #     if profile['data'] == []: break
    #     after = profile['paging'].get('cursors', {}).get('after', "shit")
    #     for item in profile['data']:
    #         

    members = api.get_connections(str(graph_name), "members")
    while members['data']:
        for item in members['data']:
        	yield FacebookUser(uid=int(item.get('id')), username=item.get('username'), name=item.get('name'))
        members = requests.get(members['paging']['next']).json()