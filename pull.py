####
import pika
import sys

class consume():
	def __init__(self, e,q,h='localhost'):
		self.exchange = e
		self.queue = q
		self.host = h 
		queue_bind(exchange=e, queue=q)
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                        host=h))
		channel = self.connection.channel();
		try:	
				
			channel.queue_declare(exclusive=True)
		except:
			print 'Error declaring queue'
			sys.exit(-1)

	def callback(self):
		print kdkd 

	def consume(self):
		basic_consume(self.callback,queue = self.queue) 
