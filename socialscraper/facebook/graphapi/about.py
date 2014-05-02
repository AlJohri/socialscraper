from ...base import ScrapingError

from . import get_object

"""
Ignoring the idea of tiered permissions, we consider any user for whom 
we find "non-public" data to be a public user.

Non-public data is defined as any key not defined in PUBLIC_KEYS.
"""

PUBLIC_KEYS = [
    'id', 
    'first_name', 
    'gender', 
    'last_name', 
    'link', 
    'locale', 
    'name', 
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