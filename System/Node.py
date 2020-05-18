import threading
import enum

# Using enum class create enumerations
from System.Connections.ReceiverController import ReceiverController
from VIF.vif import VIF


class NodeType(enum.Enum):
   Master = 1
   Detetion = 2
   Tracking = 3
   Crashing = 4

class Node(threading.Thread):
    def __init__(self,node_type, port):
        threading.Thread.__init__(self)
        self.port = port
        self.node_type = node_type

    def run(self):
        if self.node_type == NodeType.Master:
            ReceiverController(self.port).run()
            pass
        elif self.node_type == NodeType.Detetion:
            ReceiverController(self.port).run()
            pass
        elif self.node_type == NodeType.Tracking:
            ReceiverController(self.port).run()
            pass
        elif self.node_type == NodeType.Crashing:
            ReceiverController(self.port).run()
            pass






