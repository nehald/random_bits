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
			print rabbit_data
		except:
			pass; 
	def run(self):
		while(1):	
			self.scheduler.enter(2,1,self.rabbit_stats,());	
			self.scheduler.run()
			
r = rabbitmonitor()
r.run()
