import urllib
import json
import pymongo
import sys
import dataChannel
import types
import copy


"""MongoDB server"""


class MongoDB_server(dataChannel.dataChannel):
    """MongoDB server listens to the specific queues and puts the incoming data
    into MongoDB.  Uses the state vector to determine:  the collection, the database
    timeout,etc.."""
    def __init__(self, server_name='test', mq_exchange='', mq_queue='fooq', mq_host="localhost", tags="tags"):
        dataChannel.dataChannel.__init__(
            self, server_name=server_name, mq_exchange=mq_exchange, mq_queue=mq_queue, mq_host=mq_host)
        self.batch = {}
        self.state = {}
        self.conn = pymongo.Connection(host="localhost")
        self.db = self.conn[mq_exchange]
        self.coll = self.db[server_name]
        self.state["batch_len"] = 400
        self.state["watchdog_timer"] = 10
        self.state["dbname"] = mq_exchange
        self.state["collname"] = server_name
        self.default_state = copy.deepcopy(self.state)
        self.prev = {}

    def set_state(self, state):
        ## list of state variables
        for s in state:
            key, val = (s.items()[0])
            self.state[key] = val

    ## rebind the db and collection
        self.dbname = self.state['dbname']
        self.collname = self.state['collname']
        conn = pymongo.Connection()
        self.db = conn[self.dbname]
        self.coll = self.db[self.collname]

    def reset_state(self):
        try:
            self.state = copy.deepcopy(self.default_state)

        except:
            print 'Error resetting state'
            sys.exit(-1)

    def new_return(self):
        self.reset_state()
        return 0

    def handle_delivery(self, channel, method_frame, header_frame, body):
        """ the real meat of the code. handle_delivery is activated
            when a message arrives @ the message queue"""
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        json_data = None

        def timeout(self):
            print len(self.batch)
            if len(self.batch) > 0:
                try:
                    self.coll.insert(self.batch)
                    self.batch = []
                except Exception, err:
                    print self.batch
                    sys.stderr.write('Publishing_2 ERROR: %s\n' % str(err))
                    pass
                except Exception, err:
                    pass
            self.connection.add_timeout(
                self.state['watchdog_timer'], self.timeout)


###  GenericServer(current server name,next server)
mdbs = MongoDB_server("mongodb_server", mq_exchange="tweets",
                      mq_queue='testq', mq_host="hackinista.com", tags='mongodb,archiving')
mdbs.connect()
mdbs.connection = mdbs.get_connection()
# gps.connection.ioloop.add_timeout(gps.state['watchdog_timer'],gps.timeout);
mdbs.connection.ioloop.start()
