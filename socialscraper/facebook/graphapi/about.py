import logging, json
from ...base import ScrapingError
from ..models import FacebookUser

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

    employer = json.dumps(profile.get('work')) if profile.get('work') else None
    data = json.dumps(profile) if profile else None
    hometown = json.dumps(profile.get('hometown')) if profile.get('hometown') else None
    currentcity = json.dumps(profile.get('currentcity')) if profile.get('currentcity') else None

    user = FacebookUser(
        uid=int(profile.get('id')), 
        username=username, 
        email=profile.get('email'), 
        birthday=profile.get('birthday'), 
        sex=profile.get('gender'), 
        college=None, 
        employer=employer,
        highschool=None,
        currentcity=currentcity,
        hometown=hometown,
        locale=profile.get('locale'),
        data=data
    )

    return user