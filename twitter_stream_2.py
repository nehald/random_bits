from twitter import * 
import grequests
import json
# see "Authentication" section below for tokens and keys

OAUTH_TOKEN = "585421028-zyBh2Opwk6SMiEAZRwb5CjHgB4utNfEKY5f8j6md"
OAUTH_SECRET = "1RXrBsgz88wqbX8En2urOnKKfP6DHATpH9dfIBNzBfU"
CONSUMER_KEY = "hwu3JBY0QHoLy05xpj1G6w"
CONSUMER_SECRET ="kJ27v6yuibGGzzkjI8lnDaOBEcdwHEb4c8YV5fs"


twitter_stream = TwitterStream(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET))
iterator = twitter_stream.statuses.sample()
msg_queue=[]
for tweet in iterator:
	try:
		payload = json.dumps(tweet)
		headers =  {'Content-type': 'application/json', 'Accept': 'text/plain'}	
		print tweet
	except:
		print 'error'
		pass	
