import threading

import zmq

from Data.Datakeepers import DataKeepers


class SubscriberLive(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        idIp1 = DataKeepers.getDataNodeIp(1) + ":" + str(5006+1*1000)
        idIp2 = DataKeepers.getDataNodeIp(2) + ":" + str(5006+2*1000)
        idIp3 = DataKeepers.getDataNodeIp(3) + ":" + str(5006+3*1000)
        idIp4 = DataKeepers.getDataNodeIp(3) + ":" + str(5006 + 4 * 1000)

        self.ips = [idIp1,idIp2,idIp3,idIp4]

    def run(self):
        self.sub()


    def sub(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        for i in range(len(self.ips)):
         socket.connect("tcp://"+self.ips[i] )
         socket.setsockopt_string(zmq.SUBSCRIBE, str(i + 1))

        for i in range(len(self.ips)):
            strs = str(i)

        while(True):
            s = socket.recv_string()
            DataKeepers.updateTime(int(s))
            print("[Data Node "+str(s)+" ] is alive!")

