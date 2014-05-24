from ..base import BaseModel, Column

class TwitterTweet(BaseModel):
    __tablename__ = 'twitter_tweets'
    __attrs__ = ['id', 'timestamp', 'user', 'content']
    id = Column('id', 'BigInteger', primary_key=True)
    timestamp = Column('timestamp', 'BigInteger')
    user = Column('user', 'String', foreign_key=True, foreign_key_reference="twitter_users.screen_name")
    content = Column('content', 'Text')

class TwitterUser(BaseModel):
    __tablename__ = 'twitter_users'
    __attrs__ = ['id', 'screen_name']
    id = Column('id', 'BigInteger', primary_key=True)
    screen_name = Column('screen_name', 'String', unique=True)