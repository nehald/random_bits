from py2neo import *

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data") 
batch=neo4j.WriteBatch(graph)
graph.clear()
val=()
old_sub=""
wikinodes = graph.get_or_create_index(neo4j.Node,"wikinodes")
wikirels=graph.get_or_create_index(neo4j.Relationship, "wikirels")
for i in  open("/tmp/output.dat"):
	try:
		fsplit = i.split(" ")
		val=([fsplit[i].split("/")[4][:-1] for i in range(0,3)]) 
		sub,pred,obj = val
		## new sub.  flush the old data 
		## by 1. Submitting the nodes batch
		##    2. Creating the rel batch
		##    3. Submitting rel batch
		if sub != old_sub:
			try:
				if len(batch) >0:
					nodes = batch.submit()
					batch.clear()
					for n in nodes:
						linkstring = nodes[0].get_properties()['name']+":"+n.get_properties()['name']; 
						batch.get_or_create_indexed_relationship("wikirels","link",linkstring,nodes[0], "links", n)
					batch.submit()
					batch.clear()
			except:
				print 'Batch submit error'
			print "Changing node from ",old_sub+" to "+ sub 
			batch.get_or_create_indexed_node("wikinodes", "name", sub, {"name": sub})
		batch.get_or_create_indexed_node("wikinodes", "name", obj, {"name": obj})
		old_sub = sub
		
	except:
		print "Top Level Error"
		pass;	
