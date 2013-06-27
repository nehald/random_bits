from pyrabbit.api import Client
import sched,time
import threading
## monitor the rabbitmq 
class rabbitmonitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__ (self)
		self.scheduler = sched.scheduler(time.time,time.sleep)
		self.cl = Client("localhost:55672","guest","guest")

	def rabbit_stats(self):
		rabbit_data={}	
		try:
			exchanges = self.cl.get_exchanges()	
			queues = self.cl.get_queues()
			binding = self.cl.get_bindings()
			rabbit_data['time'] = time.time()
			rabbit_data['exchanges'] = exchanges
			rabbit_data['queues'] = queues
			for q in rabbit_data['queues']:
				## delete a tmp query with no consumer
				## zombie queue
				if "amq" in q['name'] and q['consumers'] == 0: 
					vhost = q['vhost']					
					self.cl.delete_queue(vhost,q['name']) 
		except:
			print 'error'
			pass; 
	def run(self):
		while(1):	
			self.scheduler.enter(10,1,self.rabbit_stats,());	
			self.scheduler.run()
			
r = rabbitmonitor()
r.run()
