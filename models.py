# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
engine = create_engine('sqlite:///test.db', echo=True)
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

__all__ = ['FacebookPage', 'FacebookUser', 'FacebookPagesUsers', 'FacebookFriend']

Base.metadata.create_all(engine)