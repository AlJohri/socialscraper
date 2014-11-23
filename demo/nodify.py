import os, sys; sys.path.append(os.path.abspath('../'))

from itertools import combinations
from models import Session, FacebookGroup, FacebookUser

session = Session()

groups = session.query(FacebookGroup).all()

class Node:
	def __init__(self, group, name, id, size=0):
		self.name = name
		self.id = id
		self.size = size
		self.group = group

class Link:
	def __init__(self, source, target, value=0):
		self.source = source
		self.target = target
		self.value = value

	@classmethod
	def create_links(cls, tuples):
		return [Link(item[0], item[1]) for item in tuples]

nodes = [Node(group, group.name, group.group_id, len(group.users)) for group in groups]
links = Link.create_links(combinations(nodes, 2))

for link in links:
	source_members = set(link.source.group.users)
	target_members = set(link.target.group.users)
	link.value=len(source_members.intersection(target_members))