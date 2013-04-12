import pika
import json
import log_class


## callback function for the consume
def on_message(channel, method_frame, header_frame, body):
	print body 
	pass;

L = log_class.Logger()
connection = pika.BlockingConnection()
channel = connection.channel()
## listen to msq_q. When something comes in
## do something with the data
channel.basic_consume(on_message, 'data',no_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
