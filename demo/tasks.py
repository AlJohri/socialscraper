import os, sys; sys.path.append(os.path.abspath('../'))

import pickle, logging, datetime
from models import Session, FacebookUser
from socialscraper.facebook import FacebookScraper
from celery import Celery
from celery.signals import worker_init
from celery import group, chord, subtask

from lib import save_user

logging.basicConfig(level=logging.DEBUG)

LOCAL_BROKER_URL = 'amqp://guest@localhost//'
REMOTE_BROKER_URL = 'amqp://guest:guest@nusocialgraph.com:5672//'

app = Celery('tasks', backend='amqp', broker=REMOTE_BROKER_URL)

def manual_init(scraper_type='nograph'):
    global facebook_scraper
    # hostname = socket.gethostname()

    if not os.path.isfile('facebook_scraper.pickle'):
        facebook_scraper = FacebookScraper(scraper_type=scraper_type)
        facebook_scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_PASSWORD'), id=os.getenv('FACEBOOK_USERID'), username=os.getenv('FACEBOOK_USERNAME'))
        facebook_scraper.pick_random_user()
        facebook_scraper.login()
        facebook_scraper.init_api()
        pickle.dump(facebook_scraper, open('facebook_scraper.pickle', 'wb'))
    else:
        facebook_scraper = pickle.load(open('facebook_scraper.pickle', "rb" ))
        facebook_scraper.scraper_type = scraper_type

@worker_init.connect
def worker_init(*args, **kwargs):
    manual_init()

@app.task
def get_usernames():
	session = Session()
	return filter(lambda username: username, map(lambda user: user.username, session.query(FacebookUser).all()))

@app.task()
def get_friends(username): # add self if bind=True
    session = Session()
    start_user = session.query(FacebookUser).filter_by(username=username).first()
    
    start_user.data = "scraping"
    session.commit()

    for result in facebook_scraper.get_friends_nograph(username):
        print result
        current_user = save_user(result, session)
        start_user.friend(current_user)

    start_user.data = "complete"
    session.commit()

@app.task()
def dmap(it, callback):
    callback = subtask(callback)
    return group(callback.clone([arg,]) for arg in it)()

# celery -A tasks worker --loglevel=info

# python -i tasks.py
# get_friends.delay("divirgupta")

if __name__ == "__main__":
    session = Session()
    manual_init()
    process_list = (get_usernames.s() | dmap.s(get_friends.s()))
    print "res = process_list()"