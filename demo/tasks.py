import os, sys; sys.path.append(os.path.abspath('../'))

from models import Session, FacebookUser
from socialscraper.facebook import FacebookScraper
from celery import Celery
from celery.signals import worker_init

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

def manual_init(scraper_type='nograph'):
    global facebook_scraper
    # hostname = socket.gethostname()

    if not os.path.isfile('facebook_scraper.pickle'):
        facebook_scraper = FacebookScraper(scraper_type=scraper_type)
        facebook_scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_PASSWORD'), id=os.getenv('FACEBOOK_USERID'), username=os.getenv('FACEBOOK_USERNAME'))
        facebook_scraper.pick_random_user()
        facebook_scraper.login()
        facebook_scraper.init_api()
        pickle.dump(facebook_scraper, open('facebook_scraper_.pickle', 'wb'))
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

@app.task(bind=True)
def get_friends(self, username):
    result = facebook_scraper.get_friends_nograph(username)
    save_user(result)

@app.task()
def dmap(it, callback):
    callback = subtask(callback)
    return group(callback.clone([arg,]) for arg in it)()

# celery -A tasks worker --loglevel=info

# process_list = (scrape.get_usernames.s() | scrape.dmap.s(scrape.get_friends.s()))
# res = process_list()

# python -i tasks.py
# get_friends.delay("divirgupta")
