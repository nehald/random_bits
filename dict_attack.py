import pika
import sys

def connect(user,passwd,host):
	credentials = pika.PlainCredentials(user, passwd)
	#connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'hackinista.com'))
	parameters = pika.ConnectionParameters(host,5672,"/",credentials)  
	
	try:
		connection = pika.BlockingConnection(parameters)
		channel = connection.channel()
	except:
		print 'connection error'
		pass; 
	
	try:
		channel.basic_publish(exchange='',
                      	routing_key='hello',
                      	body='Hello World!')
	except:
		print 'publish error'	



print connect('guest','guestt','hackinista.com') 
