import os, pickle, logging, datetime
from socialscraper.facebook import FacebookScraper
from socialscraper.adapters.adapter_sqlalchemy import convert_result

from models import Session, FacebookUser
session = Session()

logging.basicConfig(level=logging.DEBUG)

scraper_type = "nograph"

if not os.path.isfile('facebook_scraper.pickle'):
   scraper = FacebookScraper(scraper_type=scraper_type)
   scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_PASSWORD'))
   scraper.login()
   pickle.dump(scraper, open('facebook_scraper.pickle', 'wb'))
else:
   scraper = pickle.load(open('facebook_scraper.pickle', 'rb'))
   scraper.scraper_type = scraper_type

for i,result in enumerate(scraper.get_friends_nograph("andybayer")):

    user = session.query(FacebookUser).filter_by(uid=result.uid).first()

    if not user:
        user = FacebookUser()
        convert_result(user, result)
        user.created_at = datetime.datetime.now()
        session.add(user)
        print user, "created"
    else:
        convert_result(user, result)
        print user, "updated"

    user.updated_at = datetime.datetime.now()
    session.commit()