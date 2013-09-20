from py2neo import *

def connect_to_neo4j():
	return neo4j.GraphDatabaseService("http://localhost:7474/db/data")

graph = connect_to_neo4j()
batch=neo4j.WriteBatch(graph)
foo_nodes = graph.get_or_create_index(neo4j.Node,"foo_nodes")
foos=graph.get_or_create_index(neo4j.Relationship, "foos")
batch.get_or_create_indexed_node("foo_nodes", "name1", "Bob0", {"name": "Bob344"})
batch.get_or_create_indexed_node("foo_nodes", "name1", "Bob1", {"name": "Bob1"})
batch.get_or_create_indexed_node("foo_nodes", "name1", "Bob2", {"name": "Bob2"})
batch.get_or_create_indexed_node("foo_nodes", "name1", "Bob3", {"name": "Bob3"})
batch.get_or_create_indexed_node("foo_nodes", "name1", "Bob4", {"name": "Bob4"})
nodes = batch.submit() 
batch.clear()
for n in nodes:
	linkstring = nodes[0].get_properties()['name']+":"+n.get_properties()['name'];
	print linkstring	
	batch.get_or_create_indexed_relationship("foos", "name", linkstring, nodes[0], "KNOWS", n)
t = batch.submit()
print t
