from bulbs.neo4jserver import Graph

## input the dbpedia dataset
def parse_dbpedia(fname): 
        f =  open(fname);
	## skip the first comment line
	f.readline()
        try:
		for line in f:	
			fsplit =line.split(" ")
			print fsplit
			if len(fsplit) == 4:
                		vals = [fsplit[i].split("/")[4][:-1] for i in range(0,3)]
				node1 = g.vertices.create(name=vals[0])
				node2 = g.vertices.create(name=vals[2])
				g.edges.create(node1,"links",node2)
        except:
                print "Unable to parse string"
		pass;	
       

## create the Graph
g = Graph()


## down page_links_en.nt from dpedia site
parse_dbpedia("/mnt/page_links_en.nt")  
