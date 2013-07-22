from bulbs.neo4jserver import *
## input the dbpedia dataset
def parse_dbpedia(fname): 
        f =  open(fname);
	## skip the first comment line
	f.readline()
	old_nodename = ""
	node1=None
	node2=None
        try:
		for line in f:	
			fsplit =line.split(" ")
			if len(fsplit) == 4:
                		vals = [fsplit[i].split("/")[4][:-1] for i in range(0,3)]
				if vals[0] != old_nodename:
					print "changing node from ",old_nodename+" to "+ vals[0]
					node1 = g.vertices.create({'name':vals[0]})
				node2 = g.vertices.create({'name':vals[2]})
				#print vals[0]+"-----> "+vals[2] +"\n"
				edge = g.edges.create(node1,"wikilinks",node2);
				edge = g.edges.create(node2,"wikilinks",node1);
				old_nodename = vals[0]
        except:
                print "Unable to parse string"
		pass;	
       
##
# Bulbs 0.3 Neo4j Batch Example
# by James Thornton (http://jamesthornton.com)
## gist 1949517
# Batch isn't fully baked yet, but this works...
#>>> from bulbs.neo4jserver import Neo4jBatch
#>>> from bulbs.neo4jserver import Graph
#>>> g = Graph()
#>>> batch = Neo4jBatch(g.client)
#>>> message1 = g.client.message.create_vertex({'name':'James'})
#>>> message2 = g.client.message.create_vertex({'name':'Julie'})
#>>> batch.add(message1)
#>>> batch.add(message2)
#>>> batch.send()


## create the Graph
g = Graph()
g.clear()
## down page_links_en.nt from dpedia site
#parse_dbpedia("/mnt/page_links_en.nt")  
parse_dbpedia("/tmp/test_output.nt")  
