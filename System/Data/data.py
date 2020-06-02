import random
import socket


class Data:

    def __init__(self):
        self.masterIp = (socket.getfqdn())
        self.masterPorts = [10000,10002,10004]


    def getMasterIp(self):
        return self.masterIp

    def getMasterPort(self):
        random.shuffle(self.masterPorts)  # randomize the array of nodes
        return self.masterPorts[0]