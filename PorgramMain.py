from System.CameraNode import CameraNode
from System.Data.CONSTANTS import *
from System.Node import *


class ProgramMain:
    def run(self):
        # Node(NodeType.Detetion,DETECTPORT).start()
        # Node(NodeType.Tracking,TRACKPORT).start()
        Node(NodeType.Crashing,CRASHPORT).start()
        video_id = 1500
        CameraNode(video_id,'videos/'+str(video_id)+'.mp4').startStreaming()

