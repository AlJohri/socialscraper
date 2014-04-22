from ..base import ScrapingError


class Base(object):
    """
    Usage: 

    Base(uid=10, username="test")
    """

    @classmethod
    def get_columns(cls):
        column_names = filter(lambda x: x[0:2] != '__' and x[-1: -2] != '__', cls.__dict__.keys())
        columns = map(lambda x: getattr(cls, x), column_names)
        return columns

    def __init__(self,**kwargs):

        columns = self.get_columns()
        print columns

        for column in columns:
            setattr(self,column.name,kwargs.get(column.name,None))

class Column(Base):
    """
    Usage:

    Column('uid', 'BigInteger', primary_key=True, foreign_key=True, foreign_key_reference="user.uid")

    If no type is specified, it is assumed to be "String".
    """

    def __init__(self, name, column_type=None, **options):
        self.name = name
        self.type = column_type if column_type else "String"
        self.primary_key = options.get('primary_key', False)
        self.foreign_key = options.get('foreign_key', False)
        
        if self.foreign_key:
            try:
                self.foreign_key_reference = options['foreign_key_reference']
            except IndexError:
                raise ScrapingError("Foreign Key Reference must be defined if foreign_key=True")

class User(Base):
    __table__ = "user"

    uid = Column("uid", "BigInteger", primary_key=True)
    username = Column("username")
    email = Column("email")
    birthday = Column("birthday", "Date")
    name = Column("name")
    locale = Column("locale")
    profile_url = Column("profile_url")
    sex = Column("sex")

class Family(Base):
    __table__ = "family"

    profile_id = Column("profile_id", "BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="user.uid")
    relationship = Column("relationship","String")
    uid = Column("uid","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="user.uid") # foreign key
    name = Column("name","String")

class Friend(Base):
    __table__ = "friend"

    uid1 = Column("uid1","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="user.uid")
    uid2 = Column("uid2","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="user.uid")

class Page(Base):
    __table__ = "page"

    about = Column("about","Text")
    username = Column("username","String")
    page_id = Column("page_id","BigInteger", primary_key=True) # primary key
    is_verified = Column("is_verified","Boolean")
    keywords = Column("keywords","String")
    location = Column("location","BigInteger", foreign_key=True, foreign_key_reference="location.loc_id") # foreign key
    name = Column("name","String")
    url = Column("url","String")
    type = Column("type","String")
    num_likes = Column("num_likes","BigInteger")

class CategoriesPages(Base):
    __table__ = "categories_pages"

    page_id = Column("page_id","BigInteger",primary_key=True)
    category = Column("category","String",primary_key=True)

class Status(Base):
    __table__ = "status"

    like_count = Column("like_count","Integer")
    message = Column("message","Text")
    status_id = Column("status_id","BigInteger",primary_key=True)
    uid = Column("uid","BigInteger")
    time = Column("time","Date")

class PagesUsers(Base):
    __table__ = "pages_users"

    uid = Column("uid","BigInteger",primary_key=True)
    page_id = Column("page_id","BigInteger",primary_key=True)
    type = Column("type","String")
    created_time = Column("created_time","Date")

class Location(Base):
    __table__ = "location"

    gid = Column("gid","BigInteger")
    loc_id = Column("loc_id","BigInteger",primary_key=True)
    street = Column("street","String")
    city = Column("city","String")
    state = Column("state","String")
    country = Column("country","String")
    zip = Column("zip","String")
    address = Column("address","String")
    latitude = Column("latitude","Float")
    longitude = Column("longitude","Float")
    name = Column("name","String")

