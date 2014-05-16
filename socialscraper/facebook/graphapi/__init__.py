import logging
from facebook import GraphAPIError

from ...base import ScrapingError

logger = logging.getLogger(__name__)

def get_object(api, username):
    try:
        profile = api.get_object(username)
    except GraphAPIError:
        raise ValueError("Can't get object %s" % username)

    return profile

def get_connections(api, username, connection):
    try:
        profile = api.get_connections(username, connection)
    except GraphAPIError:
        raise ValueError("Can't get connection %s, %s" % username, connection)

    return profile

def get_attributes(api,graph_obj,attributes):
    """Get multiple attributes of a given a graph_name or graph_id."""
    ret_attributes = []
    data = get_object(api,graph_obj)
    for attribute in attributes:
        ret_attributes.append(data.get(attribute, None))
    return ret_attributes

from .about import get_about
from .feed import get_feed
from .likes import get_likes