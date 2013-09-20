import pdb

from py2neo import neo4j


graph=neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
foo_nodes = graph.get_or_create_index(neo4j.Node,"foo_nodes")
foos=graph.get_or_create_index(neo4j.Relationship, "foos")


foos_val = foos.query("name:Bob344*")
for i in foos_val:
	node =i.start_node.get_properties(),i.end_node.get_properties()
	print node 
