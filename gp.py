from sklearn.neighbors import NearestNeighbors
import gpxpy
import gpxpy.gpx
import datetime
import numpy as np
from sklearn import cluster
from matplotlib import pyplot
import random
# Parsing an existing file:
# and get data
# -------------------------
def get_data():
	data=[]
	gpx_file = open('1747908.gpx','r')
	gpx = gpxpy.parse(gpx_file)
	for i in gpx.get_points_data():
		unix_time = (i[0].time-datetime.datetime(1970,1,1)).total_seconds()
		lat = i[0].latitude
		lon = i[0].longitude 
		data.append((unix_time,[lat,lon]))	
	rand_smpl = [data[i] for i in sorted(random.sample(xrange(len(data)), 1000)) ]
	return rand_smpl 
#  
# 
# -----------------------
def main():
	n_clusters=3
	data =get_data()
	g = [d[1] for d in data]
	nparray =np.array(g)
	kmeans = cluster.KMeans(n_clusters)
	kmeans.fit(nparray)
	values = kmeans.cluster_centers_.squeeze()
	labels = kmeans.labels_
	symbol={0:'o',1:'+',2:'-',3:'ro',4:'b+',5:'go'}
	for i in range(0,n_clusters):
		ds = nparray[np.where(labels==i)]
		pyplot.plot(ds[:,0],ds[:,1],symbol[i])
	pyplot.show()

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km 

def main2():
	data = get_data()
	glat = [d[1] for d in data]
	gtimes = [d[0] for d in data]
	data2=zip(gtimes,glat)
	for i in range(0,10):
		lat1,lon1 = tuple(glat[1])
		lat2,lon2 = tuple(glat[i+1])
		dist = haversine(lon1,lat1,lon2,lat2) 
		print lat1,lon1,lat2,lon2,dist
def main3():
	data = get_data()
	glat = [d[1] for d in data]
	nparray =np.array(glat)
	nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(nparray)
	distances, indices = nbrs.kneighbors(nparray)
	for i in range(0,len(data)):
		print i,indices[i],distances[i][1:] 
#	f = nbrs.kneighbors_graph(nparray).toarray()
#	print f
main()	
