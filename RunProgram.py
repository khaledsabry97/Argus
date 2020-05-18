import multiprocessing

from System.CameraNode import CameraNode
from System.Data.CONSTANTS import *
from System.Node import *
from PorgramMain import ProgramMain

ProgramMain().run()
#


# def detect():
#     Node(NodeType.Detetion, DETECTPORT).run()
#
#
# def track():
#     Node(NodeType.Tracking, TRACKPORT).run()
#
# def crash():
#     Node(NodeType.Crashing, CRASHPORT).run()
#
# def camera():
#     CameraNode(1, 'videos/1559.mp4').startStreaming()
# multiprocessing.Process(target=detect).start()
# # print("hekk")
# multiprocessing.Process(target=track).start()
# multiprocessing.Process(target=crash).start()
# multiprocessing.Process(target=camera).start()



