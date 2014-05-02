from ...base import ScrapingError

from . import get_connections

def get_likes(api, username):
    profile = get_connections(api, username, 'likes')
    return profile