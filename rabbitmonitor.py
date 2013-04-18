from pyrabbit.api import Client
import sched,time
import threading


class rabbitmonitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__ (self)
		self.scheduler = sched.scheduler(time.time,time.sleep)
		self.cl = Client("http://54.241.14.229","guest","guest")

	def rabbit_stats(self):
		exchanges = self.cl.get_exchanges()	
		queues = self.cl.get_queues()
		binding = self.cl.get_bindings()
		for b in binding:
			source = b['source']
			dest = b['destination']
			if source == '':
				source = "None"	
			print source,dest
		print '==='
		for i in exchanges:
			print i
		print '***'
		print queues
	def run(self):
		self.scheduler.enter(2,1,self.rabbit_stats,());	
		self.scheduler.run()
		self.run()

r = rabbitmonitor()
r.run()
