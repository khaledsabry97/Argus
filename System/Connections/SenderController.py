import threading
from time import time

import zmq


#to send all the messages jsons using ip and port
class SenderController(threading.Thread):

    def __init__(self,ip,port,msg):
        threading.Thread.__init__(self)
        self.ip =ip #ip of the receiver
        self.port = port #port of the receiver
        self.msg = msg# the message itself

    def run(self):
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            link = "tcp://"+self.ip+":"+str(self.port)
            socket.connect(link)
            socket.RCVTIMEO =200000 #so it suspends if the receiver didn't send a message in the past  20 sec
            socket.send_pyobj(self.msg)
            jsons = socket.recv_pyobj()
            # from Controller.JsonDecoder import JsonDecoder
            # thread = JsonDecoder(jsons)
            # thread.start()
        except Exception as e:
            print(e)
            pass


