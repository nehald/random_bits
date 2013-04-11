from hotqueue import HotQueue
import time
import Queue
import grequests
import requests
import collections
queue = HotQueue("myqueue", host="localhost", port=6379, db=0)
q=collections.deque(maxlen=1000)
@queue.worker(timeout = 1)
def square(msg):
    h = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    q.append(msg)
    if len(q) > 100:
   	start = time.time()	 
	r = ((grequests.post("http://localhost/sensor/haystack/", data=d,headers=h)) for d in q)
        grequests.map(r)
        q.clear()
	print time.time()-start
#    time.sleep(1)
square()

