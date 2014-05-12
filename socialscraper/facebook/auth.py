# -*- coding: utf-8 -*-

import logging, lxml.html, re
from ..base import ScrapingError

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FACEBOOK_MOBILE_URL = 'https://m.facebook.com'
MOBILE_LOGIN_URL = FACEBOOK_MOBILE_URL + '/login.php'
MOBILE_PROFILE_URL = FACEBOOK_MOBILE_URL + '/profile.php'
MOBILE_CHECKPOINT_URL = FACEBOOK_MOBILE_URL + '/login/checkpoint/'

FACEBOOK_DESKTOP_URL = 'https://www.facebook.com'
DESKTOP_PROFILE_URL = FACEBOOK_DESKTOP_URL + '/profile.php'

INPUT_ERROR = ["We didn't recognize your email address or phone number."]

REVIEW_RECENT_LOGIN_CONTINUE = [
    "Review Recent Login", 
    "Someone recently tried to log into your account from an unknown browser. " + 
    "Please review this login."
]

REVIEW_RECENT_LOGIN_OKAY = [
    "Review Recent Login", 
    "Login near", 
    "from", 
    "This is Okay", 
    "I don&#039;t recognize"
]

REMEMBER_BROWSER = [
    "Remember Browser", 
    "You have already saved the maximum number of computers for your account. " + 
    "To remove existing computers, please visit your Account Settings after you login.  " + 
    "For now, please save this browser."
]

LOGGED_IN = [
    "Home", 
    "Messages", 
    "Notifications", 
    "Chat", 
    "Friends", 
    "logout.php"
]

LOCKED = [
    "Your Account is Temporarily Locked",
    "detected suspicious activity coming from your IP address"
]

SECURITY_CHECK = [
    "Security Check",
    "Please enter the text below"
]

def state(response_text, test_strings):
    return all(s in response_text for s in test_strings)

def login(browser, email, password, username=None):
    """

    Facebook Login

    browser: non-authenticated requests session
    email: email used to log in to Facebook
    password: password used to log into Facebook
    username: (optional) if not supplied, it will be found from the PROFILE_URL

    Given a requests session, email, and password, authenticate the session.
    Returns authenticated user's username if not given.

    Because logging into Facebook can be relatively non-deterministic based on
    how often the account has been used, how many friends it has, how recently 
    it was created, etc. I created a simple state machine and listed the states
    above. 

    It's very easy to add new states, they are based on strings that are found 
    on the resulting page.

    """

    logger.info("Begin Facebook Authentication")
    response = browser.get(FACEBOOK_MOBILE_URL, timeout=1)
    logger.debug('Loaded Facebook Mobile Browser')
    payload = {'email': email, 'pass': password}
    response = browser.post(MOBILE_LOGIN_URL , data=payload)
    logger.debug('Initial Login')

    def get_base_payload(response_content):
        doc = lxml.html.fromstring(response_content)
        return {
            'lsd': doc.cssselect("input[name=lsd]")[0].get('value'),
            'charset_test': doc.cssselect("input[name=charset_test]")[0].get('value'),
            'nh': doc.cssselect("input[name=nh]")[0].get('value')
        }

    if not state(response.text, LOGGED_IN):
        base_payload = get_base_payload(response.content)

    while not state(response.text, LOGGED_IN):

        if state(response.text, INPUT_ERROR):
            raise ScrapingError("We didn't recognize your email address or phone number.")
        elif state(response.text, REVIEW_RECENT_LOGIN_CONTINUE):
            payload = { 'submit[Continue]': 'Continue' }
            payload.update(base_payload)
            response = browser.post(MOBILE_CHECKPOINT_URL, data=payload)
            logger.debug('Review Recent Login -- Click Continue')
        elif state(response.text, REVIEW_RECENT_LOGIN_OKAY):
            payload = { 'submit[This is Okay]': 'This is Okay' }
            payload.update(base_payload)
            response = browser.post(MOBILE_CHECKPOINT_URL, data=payload)
            logger.debug('Review Recent Login -- Click Okay')
        elif state(response.text, REMEMBER_BROWSER):
            payload = {
                'submit[Continue]': 'Continue',
                'name_action_selected': 'dont_save'
            }
            payload.update(base_payload)
            response = browser.post(MOBILE_CHECKPOINT_URL, data=payload)
            logger.debug('Remember Browser -- Click Don\'t Save')
        elif state(response.text, LOCKED):
            raise ScrapingError("Account is locked.")

    logger.info("Facebook Authentication Complete")

    def get_auth_username():
        """Get username of logged in user."""
        response = browser.get(DESKTOP_PROFILE_URL)
        doc = lxml.html.fromstring(response.content)
        username = doc.cssselect('noscript meta')[0].get('content').replace('0; URL=/', '').replace('?_fb_noscript=1', '')
        logger.debug('Retrieve username from profile')
        return username

    if not username: username = get_auth_username()

    if username == "profile.php": 
        raise ScrapingError("You need to pass in the id as the username to the auth method because this user only has an id.")
    
    return username

def logout(browser):
    browser.post('http://www.facebook.com/logout.php')
