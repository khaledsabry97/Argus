from System.CameraNode import CameraNode
from System.Data.CONSTANTS import *
from System.Node import *
from VIF.vif import VIF


class ProgramMain:
    vif = None
    def __init__(self):
        if ProgramMain.vif == None:
            ProgramMain.vif = VIF()
    def run(self):
        Node(NodeType.Detetion,DETECTPORT).start()
        Node(NodeType.Tracking,TRACKPORT).start()
        Node(NodeType.Crashing,CRASHPORT).start()
        CameraNode(1,'videos/1559.mp4').startStreaming()

