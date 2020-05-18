from System.CameraNode import CameraNode
from System.Data.CONSTANTS import *
from System.Node import *


class ProgramMain:
    def run(self):
        # Node(NodeType.Detetion,DETECTPORT).start()
        # Node(NodeType.Tracking,TRACKPORT).start()
        Node(NodeType.Crashing,CRASHPORT).start()
        CameraNode(1,'videos/1566.mp4').startStreaming()

