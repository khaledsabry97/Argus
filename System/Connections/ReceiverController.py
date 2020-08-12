import threading
import zmq
from System.Controller.JsonDecoder import JsonDecoder


#responsible for receiving all the messages
class ReceiverController(threading.Thread):
    '''
    port: the port number that the thread will open on it
    '''
    def __init__(self,port,type=None,read_file = False,tf=False):
        threading.Thread.__init__(self)
        self.port = port
        self.type = type
        self.read_file = read_file
        self.tf = tf


    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % self.port)

        jsonDecoder = JsonDecoder(type=self.type,read_file = self.read_file,tf=self.tf)  # start the processing decoding method

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
            except Exception as e:
                print(e.__class__)
                print("reciever error")
                # sleep(2)
                pass



