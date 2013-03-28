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

import pdb
from pika.adapters.tornado_connection import TornadoConnection
from routes import Mapper
from pyrabbit.api import Client

## original author of the tornado rpc code
__author__ = 'Brian McFadden'
__email__ = 'brimcfadden+gist.github.com@gmail.com'

##  I modified things sig
HTML_HEADER = '<html><head><title>Tornado/Pika RPC</title></head><body>'
HTML_FOOTER = '</body></html>'

EXCHANGE = 'central'

class MainHandler(tornado.web.RequestHandler):
    def initialize(self,database):
        self.mapper=Mapper() 
        self.mapper.connect(None,"/{action_type}/{queue}") 
    def get (self):
        print 'hello Uma from eggdroplabs.com' 
        self.write('Hello Uma webpage ')        
        results = self.mapper.match(self.request.uri);
        #self.write(str(uuid.uuid4()))        
        print results 
    def post(self):
        self.write('Hello post webpage ') 
        print self.request


class SensorHandler(tornado.web.RequestHandler):
    """Uses an aysnchronous call to an RPC server to calculate fib(x).
    As with examples of asynchronous HTTP calls, this request will not finish
    until the remote response is received."""
    def initialize(self,database):
        self.mapper=Mapper() 
        self.mapper.connect(None,"/{action}/{exchange}/{queue}") 
        ##  need to know something about the exchanges and queues in the 
        ## broker
        self.cl = Client('localhost:55672', 'guest', 'guest')
   
    @tornado.web.asynchronous
    def get(self, number=''):
        self.L = log_class.Logger() 
        request = self.request
        self.L.logger.critical(request); 
        self.data = request.uri
        ## determine whether the q exists 
        result = self.mapper.match(request.uri)
        self.queue = result['queue']
        self.number = number
        self.pika_client = self.application.settings.get('pika_client')
        self.mq_ch = self.pika_client.channel
        self.corr_id = str(uuid.uuid4())

        # Currently, one callback queue is made per request. Is mapping
        # responses in one queue to multiple RequestHandlers with a
        # correlation ID a better approach or not?
        self.callback_queue_name = "{0}-{1}-{2}".format(platform.node(), os.getpid(),
                                               id(self))
        # Trying to bind to the nameless exchange breaks the program.
        callback = self.on_queue_bind
        try:
            self.mq_ch.queue_declare(exclusive=True, queue=self.callback_queue_name,
                                 callback=callback, auto_delete=False)
        except:
            log.info("Unable to declare the return clue\n")

    @tornado.web.asynchronous
    def post(self, number=''):
        request = self.request
        self.L = log_class.Logger() 
        result = self.mapper.match(request.uri)
        self.queue = result['queue']
        self.exchange= result['exchange']
        ## determine whether the queue exists or not 
        ## whether its bound to the right exchange (e.g. can we get ther from here)
        q_info=self.cl.get_queue_bindings('/',self.queue)
        if q_info != None: 
            if len([q for q in range(0,len(q_info)) if self.exchange in q_info[q]['source']]) ==0:
                response={"Response":"No exchange/queue pair"}
                self.write(json.dumps(response))
                self.finish()
                return 0;  
        else:
                self.write("Response: No queue by that name found\n")
                self.finish()
                return 0;
        self.data = request.body
        self.pika_client = self.application.settings.get('pika_client')
        self.mq_ch = self.pika_client.channel
        self.corr_id = str(uuid.uuid4())
        
       #
        if no_rpc:
            props = pika.BasicProperties(content_type='text/plain', 
        
        # Currently, one callback queue is made per request. Is mapping
        # responses in one queue to multiple RequestHandlers with a
        # correlation ID a better approach or not?
        self.callback_queue_name = "{0}-{1}-{2}".format(platform.node(), os.getpid(),
                                               id(self))
        # Trying to bind to the nameless exchange breaks the program.
        callback = self.on_queue_bind_rpc
        try:
            self.mq_ch.queue_declare(exclusive=True, queue=self.callback_queue_name,
                                     callback=callback, auto_delete=False)
        except:
            log.info("Unable to declare the return clue\n")

    def on_queue_bind_rpc(self, frame):
        print 'Queue Bound. Issuing Basic Consume.'
        self.mq_ch.basic_consume(consumer_callback=self.on_rpc_response,
                                 queue=self.callback_queue_name, no_ack=True)

        # After binding and listening to the queue with basic_consume,
        # publish the message.
        props = pika.BasicProperties(content_type='text/plain',
                                     delivery_mode=1,
                                     correlation_id=self.corr_id,
                                     reply_to=self.callback_queue_name)
        
        
        try:
        ### publish to the routing_key
            is_published=self.mq_ch.basic_publish(exchange=self.exchange, routing_key=self.queue,
                                     body=self.data, properties=props)

#           self.write("push to rabbitmq complete {0}")
            self.finish()
            print 'published' 
        except:
            print 'Error publishing data'
            pass

    def on_rpc_response(self, channel, method, header, body):
        print 'rpc response' 
        lg = "RPC response: delivery tag #{0} | Body: {1}"
        #self.L.logger.critical(lg.format(method.delivery_tag,body)); 
        if header.correlation_id != self.corr_id:
            # I'm actually not sure what to do here yet.
            raise Exception('Someone dialed a wrong number.')
        ## delete the temporary queue
        delete_q="deleting queue = "+self.callback_queue_name+"\n"
        self.L.logger.critical(delete_q)
        self.mq_ch.queue_delete(queue=self.callback_queue_name)
        # After the RPC response has been received, write to the browser.
        #self.write(HTML_HEADER)
        #self.write("push to rabbitmq complete {0}".format(body))
        #self.write(HTML_FOOTER)
        #self.finish()


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
        port = 80
    application.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_timeout(time.time() + .1, pika_client.connect)
    ioloop.start()

if __name__ == '__main__':
    main()
