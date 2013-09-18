from py2neo import * 
import sys

for k in range(100):
    batch.get_or_create_indexed_node(index_name,'id',k,{'id':str(k+1.23)})
batch.submit()

def parse_dbpedia(fname,batch,index):
	try:
		f=open(fname)
		f.readline()
	except:
		sys.exit(-1)
        old_nodename = ""
        node1=None
        node2=None
        for line in f:
                fsplit =line.split(" ")
                if len(fsplit) == 4:
                        try:
                                vals = [fsplit[i].split("/")[4][:-1] for i in range(0,3)]
                       		if vals[0] != old_name:
					batch.get_or_create_indexed_node(index,'id', 				 

			except:
                                print  'Unable to parse string'
                                pass;


graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
index_name = "index2"
idx=graph_db.get_or_create_index(neo4j.Node,index_name)
batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

parse_dbpedia("/mnt/test_output.dat",batch,idx)
