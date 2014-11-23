import logging
from time import time
from datetime import datetime
from ...base import ScrapingError
from ..models import FacebookGroup

from . import get_object
from . import get_connections

logger = logging.getLogger(__name__)

def get_groups(api, username):
    after = ''
    while True:
        profile = api.get_object(str(username) + "/groups", after=after, fields="id,name")
        if profile['data'] == []: break
        after = profile['paging']['cursors']['after']
        for item in profile['data']:
            yield FacebookGroup(group_id=int(item.get('id')), username=int(item.get('id')), name=item.get('name'))