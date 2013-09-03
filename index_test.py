from py2neo import * 

graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
index_name = "index2"
idx=graph_db.get_or_create_index(neo4j.Node,index_name)
batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database

for k in range(100):
    batch.get_or_create_indexed_node(index_name,'id',k,{'id':str(k+1.23)})
batch.submit()
