from System.CameraNode import *
from System.Node import Node, NodeType


import os



# Node(NodeType.Detetion,DETECTPORT).start()
CameraNode(1,'videos/1508.mp4').startStreaming()