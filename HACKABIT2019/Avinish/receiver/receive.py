import pika




def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

class receive:
    def __init__(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='website')
        channel.queue_declare(queue='process')
        channel.queue_declare(queue='youtube')
        channel.queue_declare(queue='ml')



        channel.basic_consume(
            queue='website', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(
            queue='process', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(
            queue='youtube', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(
            queue='ml', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


receive()