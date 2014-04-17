import logging, requests, lxml.html

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = 'https://m.facebook.com'
LOGIN_URL = BASE_URL + '/login.php'
CHECKPOINT_URL = BASE_URL + '/login/checkpoint/'

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
    "Profile", 
    "Groups", 
    "Messages", 
    "Notifications", 
    "Chat", 
    "Friends", 
    "logout.php"
]

def login(browser, email, password):

    logger.info("Begin Facebook Authentication")
    response = browser.get(BASE_URL, timeout=1)
    logger.debug('Loaded Facebook Mobile Browser')
    payload = {'email': email, 'pass': password}
    response = browser.post(LOGIN_URL , data=payload)
    logger.debug('Initial Login')

    def get_base_payload(response_content):
        doc = lxml.html.fromstring(response_content)
        return {
            'lsd': doc.cssselect("input[name=lsd]")[0].get('value'),
            'charset_test': doc.cssselect("input[name=charset_test]")[0].get('value'),
            'nh': doc.cssselect("input[name=nh]")[0].get('value')
        }

    def state(response_text, test_strings):
        return all(s in response_text for s in test_strings)

    while not state(response.text, LOGGED_IN):

        base_payload = get_base_payload(response.content)

        if state(response.text, INPUT_ERROR):
            raise UsageError("We didn't recognize your email address or phone number.")
        elif state(response.text, REVIEW_RECENT_LOGIN_CONTINUE):
            payload = { 'submit[Continue]': 'Continue' }
            payload.update(base_payload)
            response = browser.post(CHECKPOINT_URL, data=payload)
            logger.debug('Review Recent Login -- Click Continue')
        elif state(response.text, REVIEW_RECENT_LOGIN_OKAY):
            payload = { 'submit[This is Okay]': 'This is Okay' }
            payload.update(base_payload)
            response = browser.post(CHECKPOINT_URL, data=payload)
            logger.debug('Review Recent Login -- Click Okay')
        elif state(response.text, REMEMBER_BROWSER):
            payload = {
                'submit[Continue]': 'Continue',
                'name_action_selected': 'dont_save'
            }
            payload.update(base_payload)
            response = browser.post(CHECKPOINT_URL, data=payload)
            logger.debug('Remember Browser -- Click Don\'t Save')

    logger.info("Facebook Authentication Complete")