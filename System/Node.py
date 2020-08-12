import threading

# Using enum class create enumerations
from System.Connections.ReceiverController import ReceiverController
from System.Database.DatabaseThread import DatabaseThread
from System.NodeType import NodeType




class Node(threading.Thread):
    def __init__(self,node_type, port):
        threading.Thread.__init__(self)
        self.port = port
        self.node_type = node_type

    def run(self):
        if self.node_type == NodeType.Master:
            DatabaseThread().start()
            ReceiverController(self.port,type = NodeType.Master).run()
            pass
        elif self.node_type == NodeType.Detetion:
            ReceiverController(self.port,type = NodeType.Detetion,read_file= True,tf=False).run()
            pass
        elif self.node_type == NodeType.Tracking:
            ReceiverController(self.port,type = NodeType.Tracking).run()
            pass
        elif self.node_type == NodeType.Crashing:
            ReceiverController(self.port,type = NodeType.Crashing).run()
            pass






