from ..base import ScrapingError



class User(object):
	__attrs__ = [
		("uid","BigInteger"), #primary key
		("username","String"),
		("email","String"),
		("birthday","Date"),
		("name","String"),
		("locale","String"),
		("profile_url","String"),
		("sex","String")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class Family(object):
	__attrs__ = [
		# (profile_id,uid) is primary key
		("profile_id","BigInteger"),
		("relationship","String"),
		("uid","BigInteger"), # foreign key
		("name","String")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class Friend(object):
	__attrs__ = [
		# (uid1,uid2) is primary key 
		("uid1","BigInteger"), 
		("uid2","BigInteger")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class Page(object):
	__attrs__ = [
		("about","Text"),
		("username","String")
		("page_id","BigInteger"), # primary key
		("is_verified","Boolean"),
		("keywords","String"),
		("location","Integer"), # foreign key
		("name","String"),
		("url","String"),
		("type","String"),
		("num_likes","BigInteger")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class CategoriesPages(object):
	__attrs__ = [
		# (page_id,category) is primary key 
		("page_id","BigInteger"),
		("category","String")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class Status(object):
	__attrs__ = [
		("like_count","Integer"),
		("message","Text"),
		("status_id","BigInteger"), #primary key
		("uid","BigInteger"),
		("time","Date")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class PagesUsers(object):
	__attrs__ = [
	# (uid,page_id) is primary key
		("uid","BigInteger"),
		("page_id","BigInteger"),
		("type","String"),
		("created_time","Date")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))

class Location(object):
	__attrs__ = [
	# (gid,loc_id) is primary key
		("gid","BigInteger"),
		("loc_id","BigInteger"),
		("street","String"),
		("city","String"),
		("state","String"),
		("country","String"),
		("zip","String"),
		("address","String"),
		("latitude","Float"),
		("longitude","Float"),
		("name","String")
	]
	def __init__(self,**kwargs):
		for k in User.__attrs__:
			setattr(self,k[0],kwargs.get(k[0],None))