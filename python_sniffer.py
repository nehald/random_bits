import pycap.capture
import requests
import json
import time
import pika
import sys
from hotqueue import HotQueue
import collections
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
#payload = {'json_payload': data_json}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
p = pycap.capture.capture(device="eth0")
count = 0; 
queue = HotQueue("myqueue", host="localhost", port=6379, db=0)
q=collections.deque(maxlen=100)

count = 0; 
while (p):
    try: 
        packet = p.next()
        data={}
	data['time'] = packet[4]
        data['src'] = packet[1].source
        data['dst'] = packet[1].destination
        data['length'] = int(packet[1].length)
        data['protocol'] = packet[1].protocol
        data['dstp'] = int(packet[2].destinationport)
        data['srcp'] = int(packet[2].sourceport)
        payload = json.dumps(data)
	print payload 
	count = count +1
	#queue.put(payload)	
        channel.basic_publish(exchange="haystack",routing_key='',body=payload)
	#r = requests.post("http://54.241.14.229/sensor/haystack/", data=payload,headers=headers)
    except:
        pass
#while (p):
#    packet = p.next()
#print packet[1].source 
#rint packet[1].destination 
#print packet[2].destinationport 
#print packet[2].sourceport 
