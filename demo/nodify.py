import os, sys; sys.path.append(os.path.abspath('../'))

import json
from json import JSONEncoder
from itertools import combinations
from models import Session, FacebookGroup, FacebookUser

session = Session()

groups = session.query(FacebookGroup).all()

class Node:
	def __init__(self, group):
		self.group = group
		self.name = group.name
		self.id = group.group_id
		self.size = len(group.users)
		self.description = group.description
		self.icon = group.icon

class NodeEncoder(JSONEncoder):
	def default(self, o):
		return { "id": o.id, "name": o.name, "size": o.size, "description": o.description, "icon": o.icon }

class Link:
	def __init__(self, source, target, value=0):
		self.source = source
		self.target = target
		self.value = value

	@classmethod
	def create_links(cls, tuples):
		return [Link(item[0], item[1]) for item in tuples]

class LinkEncoder(JSONEncoder):
	def default(self, o):
		return { "source": o.source.id, "target": o.target.id, "value": o.value }

print "making nodes"
nodes = [Node(group) for group in groups]

print "filter nodes"
nodes = filter(lambda node: node.size > 0, nodes)

print "making linkes"
links = Link.create_links(combinations(nodes, 2))

print "calculating link values"
for link in links:
	source_members = set(link.source.group.users)
	target_members = set(link.target.group.users)
	link.value=len(source_members.intersection(target_members))

print "filter links by value"
links = filter(lambda link: link.value > 5, links)

source_node_ids = [link.source.id for link in links]
target_node_ids = [link.target.id for link in links]

print "filter links for missing nodes"
links = filter(lambda link: 
	link.source.id not in target_node_ids or 
	link.target.id not in source_node_ids, links)

print "writing to file"
json.dump(nodes, open("nodes.json", "w"), cls=NodeEncoder)
json.dump(links, open("links.json", "w"), cls=LinkEncoder)