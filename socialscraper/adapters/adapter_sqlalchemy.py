# -*- coding: utf-8 -*-

import json
from datetime import datetime
from .. import facebook, twitter

import sqlalchemy

# try:
#     import sqlalchemy
# except ImportError:
#     raise Exception("You can't use the sqlalchemy adapter without installing sqlalchemy!")

from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, BigInteger, Date, Text, Boolean, Float
from sqlalchemy.orm import relationship, backref

class BaseSQLModel(object):

    def to_json(self):
        d = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            d[column.name] = val
        return d

def make_models(db, base_classes):

    """
    base_classes = (db.Model, BaseModel)
    make_models(base_classes)
    """

    def get_model_properties(model):    
        properties = {}
        pkeys = []
        for col in model.get_columns():
            if col.foreign_key:
                properties[col.name] = Column(col.name, eval(col.type), ForeignKey(col.foreign_key_reference), primary_key=col.primary_key, unique=col.unique)
            else:
                properties[col.name] = Column(col.name, eval(col.type), primary_key=col.primary_key, unique=col.unique)
            if col.primary_key:
                pkeys.append(col.name)
        properties['__tablename__'] = model.__tablename__

        return properties

    base_classes = base_classes + (BaseSQLModel,)

    FacebookUser = type('FacebookUser', base_classes, get_model_properties(facebook.models.FacebookUser))
    FacebookFamily = type('FacebookFamily', base_classes, get_model_properties(facebook.models.FacebookFamily))
    FacebookLocation = type('FacebookLocation', base_classes, get_model_properties(facebook.models.FacebookLocation))
    FacebookFriend = type('FacebookFriend', base_classes, get_model_properties(facebook.models.FacebookFriend))
    FacebookPage = type('FacebookPage', base_classes, get_model_properties(facebook.models.FacebookPage))
    FacebookStatus = type('FacebookStatus', base_classes, get_model_properties(facebook.models.FacebookStatus))
    FacebookPagesUsers = type('FacebookPagesUsers', base_classes, get_model_properties(facebook.models.FacebookPagesUsers))

    TwitterUser = type('TwitterUser', base_classes, get_model_properties(twitter.models.TwitterUser))
    TwitterTweet = type('TwitterTweet', base_classes, get_model_properties(twitter.models.TwitterTweet))

    FacebookUser.pages = relationship('FacebookPage', secondary=FacebookPagesUsers.__table__)
    FacebookPage.users = relationship('FacebookUser', secondary=FacebookPagesUsers.__table__)

    # http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends
    FacebookUser.friends = relationship('FacebookUser', 
      secondary = FacebookFriend.__table__, 
      primaryjoin = (FacebookFriend.__table__.c.uid1 == FacebookUser.uid),
      secondaryjoin = (FacebookFriend.__table__.c.uid2 == FacebookUser.uid),
      backref = backref('facebook_friends', lazy = 'dynamic'), 
      lazy = 'dynamic'
    )

    # FacebookUser.locations = relationship('FacebookLocation') uid -> gid
    # FacebookPage.locations = relationship('FacebookLocation') page_id -> gid

    def to_json(self):
        dic = super(FacebookUser,self).to_json()
        dic['pages'] = [pg.to_json() for pg in self.pages]
        dic['locations'] = [loc.to_json() for loc in self.locations]
        return dic

    FacebookUser.to_json = to_json

    return {
        'FacebookUser': FacebookUser,
        'FacebookFamily': FacebookFamily,
        'FacebookLocation': FacebookLocation,
        'FacebookFriend': FacebookFriend,
        'FacebookPage': FacebookPage,
        'FacebookStatus': FacebookStatus,
        'FacebookPagesUsers': FacebookPagesUsers,
        'TwitterUser': TwitterUser,
        'TwitterTweet': TwitterTweet
    }

def convert_result(sqlalchemymodel, socialscrapermodel):
    for col in socialscrapermodel.get_columns():
        if not getattr(sqlalchemymodel, col.name):
            setattr(sqlalchemymodel, col.name, getattr(socialscrapermodel, col.name))

