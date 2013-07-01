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
        self.conn = pymongo.Connection(host="data.hackinista.com")
        self.db = self.conn[mq_exchange]
        self.coll = self.db[server_name]
        self.state["batch_len"] = 1000
        self.state["watchdog_timer"] = 2
        self.state["dbname"] = mq_exchange
        self.state["collname"] = server_name+"_"+mq_queue
        self.default_state = copy.deepcopy(self.state)
        self.prev = {}

    def set_state(self, state):
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

    def insert(self, val):
        try:
            obj_id = self.coll.save(val)
            return obj_id
        except:
            print 'Error inserting data'
            pass

    def handle_delivery(self, channel, method_frame, header_frame, body):
        """ the real meat of the code. handle_delivery is activated
            when a message arrives @ the message queue"""
        try:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except:
            print 'Error acking'
        json_data = None
        print 'ff'
        ## Is this a string if so; convert to json object
        ## else determine what type of object
        if isinstance(body, types.StringType):
            ## what type of string is this.  json??
            ## if it is .. determine what data structures inside
            try:
                _type = json.loads(body)
            except:
                print 'Failed in the json.loads'
                pass
            try:
                self.batch.append(_type)
                if len(self.batch) > self.state["batch_len"]:
                    print 'trigger'
                    self.coll.insert(self.batch)
                    self.batch = []
            except:
                print 'Failed in insert'
                pass
        return 0

    def timeout(self):
        print 'timeout'
        if len(self.batch) > 0:
            try:
                self.coll.insert(self.batch)
                print 'batch insert'
                self.batch = []
            except Exception, err:
                sys.stderr.write('Publishing_2 ERROR: %s\n' % str(err))
                pass
            self.connection.add_timeout(self.state[
                                        'watchdog_timer'], self.timeout)


if __name__ == '__main__':
    mdbs = MongoDB_server("mongodb_server2", mq_exchange="tweets",
                          mq_queue='testq', mq_host="hackinista.com", tags='mongodb,archiving')
    mdbs.connect()
    mdbs.connection = mdbs.get_connection()
    mdbs.connection.add_timeout(mdbs.state['watchdog_timer'], mdbs.timeout)
    mdbs.connection.ioloop.start()
