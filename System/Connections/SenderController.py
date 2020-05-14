import threading
import zmq


#to send all the messages jsons using ip and port
class SenderController(threading.Thread):

    def __init__(self,ip,port,json):
        threading.Thread.__init__(self)
        self.ip =ip #ip of the receiver
        self.port = port #port of the receiver
        self.json = json# the message itself

    def run(self):
        self.send()


    def send(self):
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            link = "tcp://"+self.ip+":"+str(self.port)
            socket.connect(link)
            socket.RCVTIMEO =100000 #so it suspends if the receiver didn't send a message in the past  10 sec

            socket.send_json(self.json)
            # jsons = socket.recv_json()
            # from Controller.JsonDecoder import JsonDecoder
            # thread = JsonDecoder(jsons)
            # thread.start()
        except:
            pass


