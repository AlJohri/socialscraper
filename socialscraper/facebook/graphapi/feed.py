import logging, requests
from time import time
from datetime import datetime
from urlparse import urlparse, parse_qs
from facebook import GraphAPIError

from . import get_object

logger = logging.getLogger(__name__)

def get_feed(api, graph_name, start="", end=datetime.now()):
    """

    Returns:

        feed from start date to end date.

    If dates not specified starts from present and continues
    reverse chronologically.

    Input:
        api: GraphAPI
        graph_name: string
        start: datetime
        end: datetime

    Caveats:
        The Facebook GraphAPI ['paging']['next'] and ['paging']['previous'] url 
        ignores end limits.

        For example, if I search for posts between Date X to Y. The first result
        will be between these dates. 

        If I blindly go to the next url, it will 
        keep until=Y and traverse reverse chronologically indefinitely.

        Similarly, if I blindly go to the previous url, it will keep since=X and
        traverse forward chronologically indefinitely.

        For this reason, I re-append the since parameter parameter to the next url
        and reappend the until parameter to the previous url.

    """

    # if start, end ar passed in as None
    if start == None: start = ""
    if end == None: end = datetime.now()

    logger.info("Getting feed since %s until %s" % 
        (
            start.strftime('%Y-%m-%d %H:%M:%S') if isinstance(start, datetime) else "indefinite", 
            end.strftime('%Y-%m-%d %H:%M:%S')
        )
    )

    feed = api.get_connections(graph_name, "feed", 
        since=int((start-datetime(1970,1,1)).total_seconds()) if isinstance(start, datetime) else "",
        until=int((end-datetime(1970,1,1)).total_seconds())
    )

    
    while feed['data']:
        for item in feed['data']: yield item

        # Hacky fix for Facebook GraphAPI. See method doctstring.
        feed['paging']['next'] += "&since=%d" % int((start-datetime(1970,1,1)).total_seconds()) if isinstance(start, datetime) else ""
        feed['paging']['previous'] += "&until=%d" % int((end-datetime(1970,1,1)).total_seconds())

        feed = requests.get(feed['paging']['next']).json()
