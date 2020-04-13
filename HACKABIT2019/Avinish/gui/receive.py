import pika
import time
import gaze_dnn
import multiprocessing
from threading import Thread
import sys
import tkinter as tk
import tkinter.messagebox as tm
import json
# t = Thread(target=drowsiness.track() )
# t.daemon = True
# t.start()
# t.join()

class alert(Thread):
    def run(self):
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='hello')
        self.channel.queue_declare(queue='drowsiness')
        self.channel.queue_declare(queue='website')
        self.channel.queue_declare(queue='youtube')
        self.channel.queue_declare(queue='blink')

        def callback_ml(ch, method, properties, body):
            if body == b'noFaceStart':
                print("popup should pop")
                tm.showwarning("No face Detected", "There was no face")
            if body == b'drowStart':
                tm.showwarning("Drowsy", "Laugh and the world laughs with you, snore and you sleep alone")

        def callback_web(ch, method, properties, body):
            data = body.decode("utf-8")
            web = json.loads(data)
            if web['bool'] == "false":
                tm.showwarning("Website", "Wrong domain opened:- "+web['domain'])

        def callback_you(ch, method, properties, body):
            data = body.decode("utf-8")
            web = json.loads(data)
            if web['bool'] == "false":
                tm.showwarning("Youtube", "Wrong video opened:- "+web['title'])        

        def callback_blink(ch, method, properties, body):
            data = body.decode("utf-8")
            web = json.loads(data)
            file = open("blink.json", "w+")
            file.write()

        def callback(ch, method, properties, body):
            print(" [x] Received {} {}".format(body,time.time()), flush=True)


        self.channel.basic_consume(
            queue='website', on_message_callback=callback_web, auto_ack=True)

        
        self.channel.basic_consume(
            queue='youtube', on_message_callback=callback_you, auto_ack=True)


        self.channel.basic_consume(
            queue='drowsiness', on_message_callback=callback_ml, auto_ack=True)

        self.channel.basic_consume(
            queue='blink', on_message_callback=callback_blink, auto_ack=True)


        print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
        self.channel.start_consuming()
    def stop(self):
        self.channel.stop_consuming()
        self.connection.close()



