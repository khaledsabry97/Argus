import json
import threading
from time import time

import zmq

from System.Controller.JsonDecoder import JsonDecoder


#responsible for receiving all the messages from servers and data nodes
class ReceiverController(threading.Thread):

    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        self.receive()


    def receive(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % self.port)

        while True:
            #  Wait for next request from client
            try:
                message = socket.recv_pyobj() #receive a message json

                # jsons = json.loads(message)
                jsonDecoder = JsonDecoder(message) # start the processing decoding method
                jsonDecoder.run()
                # socket.send_json({"func":"success"})
            except:
                pass



