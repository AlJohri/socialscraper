import logging
from ...base import ScrapingError

from . import get_object

logger = logging.getLogger(__name__)

"""
Ignoring the idea of tiered permissions, we consider any user for whom 
we find "non-public" data to be a public user.

Non-public data is defined as any key not defined in PUBLIC_KEYS.
"""

PUBLIC_KEYS = [
    'id', 
    'name',     
    'first_name', 
    'middle_name',
    'last_name',
    'gender',  
    'link', 
    'locale', 
    'updated_time', 
    'username'
]

def get_about(api, username):

    def check_public_profile(profile):
        for key in profile.keys(): 
            if key not in PUBLIC_KEYS:
                return True
                break
        return False

    profile = get_object(api, username)

    return profile, check_public_profile(profile)