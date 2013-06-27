import urllib
import json
import pymongo
import sys
import dataChannel
import types
import copy
import log_class
"""MongoDB server"""


class MongoDB_server(dataChannel.dataChannel):
    """MongoDB server listens to the specific queues and puts the incoming data
    into MongoDB.  Uses the state vector to determine:  the collection, the database
    timeout,etc.."""
    def __init__(self, server_name='test', mq_exchange='', mq_queue='fooq', mq_host="localhost", tags="tags"):
        dataChannel.dataChannel.__init__(
            self, server_name=server_name, mq_exchange=mq_exchange, mq_queue=mq_queue, mq_host=mq_host)
        self.batch = []
        self.state = {}
        self.state["batch_len"] = 1000
        self.state["watchdog_timer"] = 2
        self.default_state = copy.deepcopy(self.state)
        self.prev = {}

    def handle_delivery(self, channel, method_frame, header_frame, body):
        """ the real meat of the code. handle_delivery is activated
            when a message arrives @ the message queue"""
        try:
            	channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except:
		pass; 		
	print body[0]


    def timeout(self):
        print 'timeout'
	return

if __name__ == '__main__':
    mdbs = MongoDB_server("collectd", mq_exchange="amq.fanout",
                          mq_queue='', mq_host="hackinista.com", tags='mongodb,archiving')
    mdbs.connect()
    mdbs.connection = mdbs.get_connection()
    mdbs.connection.add_timeout(mdbs.state['watchdog_timer'], mdbs.timeout)
    mdbs.connection.ioloop.start()
