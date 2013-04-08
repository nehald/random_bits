import pycap.capture
import requests
import json
import time
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
#payload = {'json_payload': data_json}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
p = pycap.capture.capture(device="lo")
print 'f'
while (p):
    try: 
        packet = p.next()
        data={}
        data['src'] = packet[1].source
        data['dst'] = packet[1].destination
        data['length'] = int(packet[1].length)
        data['protocol'] = packet[1].protocol
        data['dstp'] = int(packet[2].destinationport)
        data['srcp'] = int(packet[2].sourceport)
        payload = json.dumps(data)
        print payload
#        requests.post("http://eggdroplabs.com:8000/sensor/ex1/",data=payload,headers=headers)
        channel.basic_publish(exchange="ex1",routing_key='',body=payload)
    except:
        pass
#while (p):
#    packet = p.next()
#print packet[1].source 
#rint packet[1].destination 
#print packet[2].destinationport 
#print packet[2].sourceport 
