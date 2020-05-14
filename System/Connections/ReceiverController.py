import json
import threading

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
            try:
                #  Wait for next request from client
                message = socket.recv_json() #receive a message json
                type(message)
                jsons = json.loads(message)
                jsonDecoder = JsonDecoder(jsons) # start the processing decoding method
                jsonDecoder.start()
                # socket.send_json({"func":"success"})
            except:
                # socket.send_json({"func": "failed"})
                print("error")


