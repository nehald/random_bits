import pika
import sys
import json
import time
from pika.adapters.tornado_connection import TornadoConnection
import types
import log_class
# Detect if we're running in a git repo
from os.path import exists, normpath
if exists(normpath('../pika')):
    sys.path.insert(0, '..')

from pika.adapters import SelectConnection
from pika.connection import ConnectionParameters

# We use these to hold our connection & channel


class dataChannel:
    """ The dataChannel is the base class of all our datasource.
    It's purpose is to: a).  Setup the queues"""
    def __init__(self, server_name='test', mq_queue_exchange='', mq_host=''):
        self.channel = None
        self.id = server_name
        self.queue_counter = 0
        self.queue = ''
        self.routing_key = ''
        self.exchange = mq_queue_exchange
        self.connection = None
        self.connected = False
        self.connecting = False
        self.rabbithost = mq_host
        self.L = log_class.Logger()

    def get_connection(self):
        return self.connection

    def connect(self):
        if self.connecting:
            return
        self.connecting = True
        credentials = pika.PlainCredentials('guest', 'guest')
        params = pika.ConnectionParameters(host=self.rabbithost,
                                           port=5672,
                                           virtual_host="/",
                                           credentials=credentials)

        host = (len(sys.argv) > 1) and sys.argv[1] or '127.0.0.1'

        try:
            self.connection = SelectConnection(params, self.on_connected)
        except:
            # self.L.critical("Error connecting to rabbitmq on host =
            # "+self.host);
            sys.exit(-1)
        ###

    def on_connected(self, connection):
        self.connection = connection
        self.connection.channel(self.on_channel_open)
        self.connected = True

    def on_channel_open(self, channel):
        self.channel = channel
        if 
        self.channel.exchange_declare(exchange=self.exchange,
                                      type="direct", passive=True, 
                                      auto_delete=False,
                                      durable=True,
                                      callback=self.on_exchange_declared)

    def on_exchange_declared(self, frame):
        try:
            self.channel.queue_declare(queue=self.queue,
                                       auto_delete=False,
                                       durable=True,
                                       exclusive=False,
                                       callback=self.on_queue_declared)
        except:
            self.logger.warn("Error declaring queue = " + self.queue)
            pass

    def on_queue_declared(self, frame):
        try:
            self.channel.queue_bind(exchange=self.exchange,
                                    queue=self.queue,
                                    routing_key=self.routing_key,
                                    callback=self.on_queue_bound)
        except:
                self.logger.warn("Error binding to queue = " + self.queue)
                pass

    def on_queue_bound(self, frame):
        self.channel.basic_consume(consumer_callback=self.handle_delivery,
                                   queue=self.queue, no_ack=False)

    def handle_delivery(self, channel, method_frame, header_frame, body):
        print "7...Basic.Deliver %s delivery-tag %i: %s" %\
              (header_frame.content_type,
              method_frame.delivery_tag,
              body)
        self.data_op(body)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def data_op(self, args):
        print "Please implement get_data"

    def basic_publisher(self, rk, data):
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key=rk,
                                       body=data, properties='')
        except:
            print 'Error in basic_publisher'
            pass
