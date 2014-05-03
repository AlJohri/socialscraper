import logging
from facebook import GraphAPIError

from ...base import ScrapingError

logger = logging.getLogger(__name__)

def get_object(api, username):
    try:
        profile = api.get_object(username)
    except GraphAPIError:
        raise ScrapingError("Can't get object %s" % username)

    return profile

def get_connections(api, username, connection):
    try:
        profile = api.get_connections(username, connection)
    except GraphAPIError:
        raise ScrapingError("Can't get connection %s, %s" % username, connection)

    return profile

from .about import get_about
from .feed import get_feed
from .likes import get_likes