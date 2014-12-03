import logging
from time import time
from datetime import datetime
from ...base import ScrapingError
from ..models import FacebookGroup

from . import get_object
from . import get_connections

logger = logging.getLogger(__name__)

def get_group(api, username):
	item = api.get_object(str(username))
	return FacebookGroup(group_id=int(item.get('id')), username=int(item.get('id')), name=item.get('name'), icon=item.get('icon'), privacy=item.get('privacy'), description=item.get('description'))

def get_groups(api, username):
    after = ''
    while True:
        profile = api.get_object(str(username) + "/groups", after=after, fields="id,name")
        if profile['data'] == []: break
        after = profile['paging']['cursors']['after']
        for result in profile['data']:
            item = api.get_object(result.get('id'))
            yield FacebookGroup(group_id=int(item.get('id')), username=int(item.get('id')), name=item.get('name'), icon=item.get('icon'), privacy=item.get('privacy'), description=item.get('description'))