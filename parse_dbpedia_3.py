from py2neo import *
import pymongo
import json
import traceback
conn = pymongo.Connection(host="data.hackinista.com")
db = conn["wiki_large"] 
coll = db["link"]

graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data") 
batch=neo4j.WriteBatch(graph)
#graph.clear()
val=()
old_sub=""
link_dict={}
wikinodes_large	= graph.get_or_create_index(neo4j.Node,"wikinodes_large")
wikirels_large=graph.get_or_create_index(neo4j.Relationship, "wikirels_large")
link={}

		
for i in  open("/home/ubuntu/bigdata/page_links_en.nt"):
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
					root_node = str(nodes[0])[1:-1]
					root_id,rval= tuple(root_node.split(" "))
					root_val = json.loads(rval)['name'] 
					root={}
					root['node_id']=root_id;
					root['node_val']=root_val; 
					root['num_relationship'] = len(nodes[1:])	
					try:	
						if link_dict[root_id]==1:
							pass;
					except:
						link_dict[root_id] = 1; 
						try:
							coll.save(root)
							root.clear()				
						except:
							print 'Error saving root link'
							pass; 
					batch.clear()
					for n in nodes[1:]:
						node_string = str(n)[1:-1]
						node_id,val= tuple(node_string.split(" "))
						node_val = json.loads(val)['name'] 
						link['node_id'] = node_id 
						link['node_val'] = node_val
						try:
							if link_dict[node_id]==1:
								pass;	
						except:
							link_dict[node_id] = 1
							try:	
								coll.save(link)
								link.clear()
							except:
								print 'Error saving link'
								pass;
						linkstring = nodes[0].get_properties()['name']+":"+n.get_properties()['name']; 
						batch.get_or_create_indexed_relationship("wikirels_large","link",linkstring,nodes[0], "links", n)
					batch.submit()
					batch.clear()
			except:
				print 'Batch submit errori'
				traceback.print_exception() 
			print "Changing node from ",old_sub+" to "+ sub 
			batch.get_or_create_indexed_node("wikinodes_large", "name", sub, {"name": sub})
		batch.get_or_create_indexed_node("wikinodes_large", "name", obj, {"name": obj})
		old_sub = sub
		
	except:
		print "Top Level Error"
		pass;	
