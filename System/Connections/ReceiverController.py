import json
import threading
from time import time, sleep

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
        jsonDecoder = JsonDecoder()  # start the processing decoding method

        while True:
            #  Wait for next request from client
            try:

                message = socket.recv_pyobj() #receive a message json
                socket.send_pyobj("")
                # print("see")
                # jsons = json.loads(message)
                jsonDecoder.run(message)
                # socket.close()
                # socket.send_json({"func":"success"})
            except:
                print("reciever error")
                # sleep(2)
                pass



