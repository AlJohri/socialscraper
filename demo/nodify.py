import os, sys; sys.path.append(os.path.abspath('../'))

import json
from json import JSONEncoder
from itertools import combinations
from models import Session, FacebookGroup, FacebookUser, SuperGroup

session = Session()

# leaves only
groups = filter(lambda group: len(group.children.all()) == 0,session.query(SuperGroup).all())

class Node:
	def __init__(self, group):
		self.group = group
		self.name = group.name
		self.id = group.id
		self.size = len(set(reduce(lambda x, y: x + y, [fbgroup.users for fbgroup in group.facebook_groups], [])))
		self.description = "\n".join([fbgroup.description or "" for fbgroup in group.facebook_groups])
		self.icon = group.facebook_groups[0].icon
		self.category = group.parents[0].name

class Link:
	def __init__(self, source, target, value=0):
		self.source = source
		self.target = target
		self.value = value

	@classmethod
	def create_links(cls, tuples):
		return [Link(item[0], item[1]) for item in tuples]

print "making nodes"
nodes = [Node(group) for group in groups]

print "filter nodes"
nodes = filter(lambda node: node.size > 0, nodes)

print "making linkes"
links = Link.create_links(combinations(nodes, 2))

print "calculating link values"
for link in links:

	source_members = set(reduce(lambda x, y: x + y, [fbgroup1.users for fbgroup1 in link.source.group.facebook_groups], []))
	target_members = set(reduce(lambda x, y: x + y, [fbgroup2.users for fbgroup2 in link.target.group.facebook_groups], []))
	link.value=len(source_members.intersection(target_members))

	print "source length", len(source_members), "target length", len(target_members), "link value", link.value

print "filter links by value"
links = filter(lambda link: link.value > 5, links)

source_node_ids = [link.source.id for link in links]
target_node_ids = [link.target.id for link in links]

print "filter links for missing nodes"
links = filter(lambda link: 
	link.source.id not in target_node_ids or 
	link.target.id not in source_node_ids, links)

print "writing to file", len(nodes), "nodes", len(links), "links"

results = {
	"nodes": nodes,
	"links": links
}

class MyEncoder(JSONEncoder):
	def default(self, o):
		if o.__class__.__name__ == 'Link':
			return { "source": o.source.id, "target": o.target.id, "value": o.value }
		elif o.__class__.__name__ == 'Node':
			return { "id": o.id, "name": o.name, "size": o.size, "description": o.description, "icon": o.icon, "category": o.category }

json.dump(results, open("data.json", "w"), cls=MyEncoder)