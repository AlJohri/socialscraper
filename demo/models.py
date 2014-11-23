import os, sys; sys.path.append(os.path.abspath('../'))

# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from pprint import pprint as pp

LOCAL_DATABASE_URL = 'postgresql:///nusocialgraph'
REMOTE_DATABASE_URL = 'postgres://nusocialgraph:nucracker@nusocialgraph-production.cpc7uj1yh3bv.us-east-1.rds.amazonaws.com:5432/nusocialgraph'

engine = create_engine(LOCAL_DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

from socialscraper.adapters import adapter_sqlalchemy

class BaseModel(object):
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    def __init__(self,created_at,updated_at):
        self.created_at = created_at
        self.updated_at = updated_at

base_classes = (Base, BaseModel,)
fbmodels = adapter_sqlalchemy.make_models(Base, base_classes)

FacebookUser = fbmodels['FacebookUser']
FacebookPage = fbmodels['FacebookPage']
FacebookPagesUsers = fbmodels['FacebookPagesUsers']
FacebookFriend = fbmodels['FacebookFriend']
FacebookGroup = fbmodels['FacebookGroup']

__all__ = ['Session', 'FacebookPage', 'FacebookUser', 'FacebookPagesUsers', 'FacebookFriend', 'FacebookGroup']

# create sqllite db
# python -c "from models import Base, engine; Base.metadata.create_all(engine)"

# to query db
# python -i models.py
# [user.name for user in session.query(FacebookUser).all()]

if __name__ == '__main__':
	session = Session()
	scraping = lambda : session.query(FacebookUser).filter(FacebookUser.data=="scraping").all()
	complete = lambda : session.query(FacebookUser).filter(FacebookUser.data=="complete").all()
	
	print "complete", session.query(FacebookUser).filter(FacebookUser.data=="complete").count()
	pp(sorted([(user.name, user.uid, user.friends.count()) for user in complete()], key=lambda x: x[2], reverse=True))

	print "scraping", session.query(FacebookUser).filter(FacebookUser.data=="scraping").count()
	pp(sorted([(user.name, user.uid, user.friends.count()) for user in scraping()], key=lambda x: x[2], reverse=True))
	

