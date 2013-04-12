from pyrabbit.api import Client
import sched,time
import threading


class rabbitmonitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__ (self)
		self.scheduler = sched.scheduler(time.time,time.sleep)
		self.cl = Client("localhost:55672","guest","guest")

	def print_time(self): print "From print_time", time.time()

	def rabbit_stats(self):
		exchanges = self.cl.get_exchanges()	
		for e in exchanges:
			try:
				print e['message_stats_out'] 
				print e['message_stats_in'] 
			except:
				pass; 
	
	def run(self):
		self.scheduler.enter(5,1,self.rabbit_stats,());	
		self.scheduler.run()
		self.run()

r = rabbitmonitor()
r.run()
