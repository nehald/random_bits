from flask import Flask
from flask.ext.pymongo import PyMongo
from flask import request
import json
import time
import logging
from logging.handlers import RotatingFileHandler
app = Flask(__name__)
import pymongo

connect = pymongo.Connection()


def _list_all_channels():
    channels = []
    db = connect['accounts']
    cursor = db['info'].find()
    if cursor.count() > 0:
        channels = [c['channel'] for c in cursor]
    return channels


def _get_channel_info(channel_id):
    db = connect['accounts']
    cursor = db['info'].find_one({"channel":channel_id})
    
def _create_channel(account, channel_id):
    if _check_info(account, channel_id) == False:
        log_string = "creating channel -- account={0},channel_id={1}".format(
            account, channel_id)
        app.logger.debug(log_string)
        init = {}
        init['created'] = time.ctime()
        init['account'] = account
        init['channel'] = channel_id
        db = connect['accounts']
        db['info'].save(init)
        try:
            db = connect[account]
            db[channel_id].save(init)
            db[channel_id].create_index([("loc", pymongo.GEO2D)])
            return 0
        except:
            return -1
    return 1


def _check_info(account, channel_id):
    try:
        db = connect['accounts']
        exists = db['info'].find_one({
                                     "channel": channel_id, "account": account})
        if exists == None:
            return False
        return True
    except:
        return False


def _check_hash(account, channel_id, hashval):

    try:
        db = connect[account]
        cursor = db[channel_id].find_one({"hash": hashval})
        if cursor == None:
            return False
        if cursor['hash'] == hashval:
            return True
        return False
    except:
        return False


def _create_point(account, channel_id, title, desc, loc):
    log_string = "creating point account={0}, channel_id={1},title={2},loc={3}".format(
        account, channel_id, title, loc)
    app.logger.debug(log_string)
    pt_info = {}
    loc_array = loc.split(",")
    pt_info['loc'] = [float(loc_array[0]), float(loc_array[1])]
    pt_info['title'] = title
    pt_info['desc'] = desc
    pt_info['hash']= hash(loc+title+account+channel_id)
    json.dumps(pt_info)
    db = connect[account]
    conn = db[channel_id]
    try:
        conn.save(pt_info)
    except:
        print 'Error in collection save'
    return 0


@app.route('/delete/<account>')
def delete(account):
	try:
		C=Connection()
		C.dropDatabase[account]
	except:
		pass;	

@app.route('/create/<account>')
def create(account):
    error = {-1: "Error creating channel", 0:
             "Channel created", 1: "Channel already exists"}
    rc = _create_channel(account, account)
    return error[rc]


@app.route('/createx/<account>/<channel>')
def createx(account, channel):
    error = {-1: "Error creating channel", 0:
             "Channel created", 1: "Channel already exists"}
    rc = _create_channel(account, channel)
    return error[rc]


@app.route('/create_point', methods=['POST'])
def create_point():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            try:
                loc = str(data['loc'])
                if not isinstance(loc, type("string")):
                    return """Unable to create point.. loc string should be "lat,lon" """
                title = str(data['title'])
                desc = str(data['desc'])
                account = str(data['account'])
                try:
                    channel = str(data['channel_id'])
                except:
                    channel = account
            except:
                log_string = "Error in create_point"
                app.logger.debug(log_string)
                pass

            hashval = hash(loc+title+account+channel)

            if _check_info(account, channel) == True:
            	if _check_hash(account, channel, hashval) == True:
                	return 'Location already exists'
		_create_point(account, channel, title, desc, loc)
                return "Data point created"
            else:
                return 'No account/channel does not exists'


@app.route('/list_channels')
def list_channels():
    channels = "\n".join(_list_all_channels())
    return(channels)


@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            try:
	        account = data['account']
                loc = data['loc']
                channels = data['channels']
		for c in channels:
			print c		
	
	    except:
                pass
	return 'query complete'

@app.route('/')
def home():
    return 'hello world'

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=8080)
