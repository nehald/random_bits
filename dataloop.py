import pika
import json
import log_class

def basic_publish(channel,method_frame,header_frame,body):
        publish_info = "routing_key = "+ header_frame.reply_to+" "+body+"\n\n" 
        print publish_info
        L.logger.critical(publish_info)
        L.logger.critical("test")
    
        try: 
            channel.basic_publish(exchange='', routing_key=header_frame.reply_to,
                           properties=pika.BasicProperties(correlation_id=
                            header_frame.correlation_id), body=body)
        except:
            pass;
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

## callback function for the consume
def on_message(channel, method_frame, header_frame, body):
    try:
        basic_publish(channel,method_frame,header_frame,body)
    except:
        L.logger.critical("Error in basic_publish") 

L = log_class.Logger()
connection = pika.BlockingConnection()
channel = connection.channel()
## listen to msq_q. When something comes in
## do something with the data
channel.basic_consume(on_message, 'msg_q')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
