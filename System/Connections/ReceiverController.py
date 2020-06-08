import threading
import zmq
from System.Controller.JsonDecoder import JsonDecoder


#responsible for receiving all the messages
class ReceiverController(threading.Thread):
    '''
    port: the port number that the thread will open on it
    '''
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port


    def run(self):
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



