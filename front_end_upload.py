#!/usr/bin/env python

"""A Tornado example of RPC.

Designed to work with rpc_server.py as found in RabbitMQ Tutorial #6:
http://www.rabbitmq.com/tutorials/tutorial-six-python.html

Some code is borrowed from pika's tornado example.
"""

import platform
import os
import sys
import time
import uuid

import pika
import tornado.ioloop
import tornado.httpserver
import tornado.httputil
import tornado.web
import log_class  
import json
import pdb
from pika.adapters.tornado_connection import TornadoConnection
from routes import Mapper
from pyrabbit.api import Client
import string
import random
## original author of the tornado rpc code
__author__ = 'Brian McFadden'
__email__ = 'brimcfadden+gist.github.com@gmail.com'

##  I modified things sig
HTML_HEADER = '<html><head><title>Tornado/Pika RPC</title></head><body>'
HTML_FOOTER = '</body></html>'
EXCHANGE = 'central'
g_port = 0; 

cl = Client('localhost:55672', 'guest', 'guest')
class MainHandler(tornado.web.RequestHandler):
    def initialize(self,database):
        self.mapper=Mapper() 
        self.mapper.connect(None,"/{action_type}/{queue}") 
    def test(self):
        N = 2048 
        return(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N)))
    def get (self):
        self.write(str(g_port)) 
        self.write("\n")
        self.write('Hello Uma webpage ')        
        self.write(str(uuid.uuid4()))        
        self.write(self.test())        
        self.finish() 
    def post(self):
        self.finish()

class UploadHandler(tornado.web.RequestHandler):
    """Uses an aysnchronous call to an RPC server to calculate fib(x).
    As with examples of asynchronous HTTP calls, this request will not finish
    until the remote response is received."""
    def initialize(self,database):
        self.mapper=Mapper() 
        self.mapper.connect(None,"/{action}/{exchange}/{queue}") 
        self.mapper.connect(None,"/{action}/{exchange}/") 
   
    def get(self):
	self.write("get")
 
    def post(self, number=''):
        request = self.request
        self.data = request.body
       	result = self.mapper.match(request.uri) 
	self.queue =''
	try:
		self.queue = result['queue']
	except:
		pass; 	
	self.pika_client = self.application.settings.get('pika_client')
        self.mq_ch = self.pika_client.channel
        self.corr_id = str(uuid.uuid4())
	self.exchange= result['exchange']
        try:
	    pub=self.mq_ch.basic_publish(exchange=self.exchange, routing_key=self.queue,body=self.data)
            response={"Response":"Message sent"}
            self.write(json.dumps(response))
        except:
	    response={"Reponse":"Error publishing msg to exchange"}
            self.write(json.dumps(response))


class PikaClient(object):
    """A modified class as described in pika's demo_tornado.py.
    It handles the connection for the Tornado instance. Messaging/RPC
    callbacks are handled by the Tornado RequestHandler above."""
    def __init__(self):
        self.connecting = False
        self.connection = None
        self.channel = None
        #self.L = log_class.Logger() 
    def connect(self):
        if self.connecting:
            log.info('Already connecting to RabbitMQ.')
            return
        #self.L.logger.info("Connecting to RabbitMQ")
        self.connecting = True
        creds = pika.PlainCredentials('guest', 'guest')
        params = pika.ConnectionParameters(host='localhost', port=5672,
                                           virtual_host='/', credentials=creds)
        self.connection = TornadoConnection(params,
                                            on_open_callback=self.on_connect)
        self.connection.add_on_close_callback(self.on_closed)

    def on_connect(self, connection):
        self.connection = connection
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        #self.L.logger.info('Channel Open')
        self.channel = channel
        # I'm having trouble using named exchanges.
        ## channel.exchange_declare(exchange='rpc_ex', type='direct',
        ##                          auto_delete=True, durable=False,
        ##                          callback=self.on_exchange_declare)

    def on_exchange_declare(self, frame):
        log.info("Exchange declared.")

    def on_basic_cancel(self, frame):
        log.info('Basic Cancel Ok.')
        # If we don't have any more consumer processes running close
        self.connection.close()

    def on_closed(self, connection):
        # We've closed our pika connection so stop the demo
        tornado.ioloop.IOLoop.instance().stop()


def main():
    pika_client = PikaClient()
    database={}
    database['g'] = 'f'
    database['gg'] = 'ff'
    database['ggg'] = 'gff'
    global g_port;
    
    application = tornado.web.Application(
    [(r'/sensor/.*', SensorHandler,dict(database=database)),(r'/.*',MainHandler,dict(database=database))],
#        [(r'/index.html',MainHandler)],
#        [(r'/tom/*',SensorHandler),(r'/index.html',MainHandler)],
#        **{'pika_client': pika_client, 'debug': True}

        #     **{'pika_client': pika_client, 'debug': True}
        #     [(r'/tom/*', Fib)],
             **{'pika_client': pika_client, 'debug': True}
    )
    try:
        port = int(sys.argv[1])  # $ python tornadoweb_pika.py 80
    except:
        port = 8000 
    g_port = port
    application.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_timeout(time.time() + .1, pika_client.connect)
    ioloop.start()

if __name__ == '__main__':
    main()
