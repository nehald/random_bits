import pdb
import pymongo
from py2neo import neo4j 


graph_db=neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

conn = pymongo.Connection(host="data.hackinista.com")
db = conn["wiki"]
coll = db["links"]
cursors = db.command("text","links",search="Cars")
for i in cursors['results']:
	print i['obj']['subject'],i['obj']['index'] 

node = graph_db.node(968) 
for i in node.match():
	print i.start_node.get_properties()['title']+" links to "+i.end_node.get_properties()['title'] 
