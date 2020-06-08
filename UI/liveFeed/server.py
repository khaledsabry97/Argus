import zmq
import time
import json
port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv_json()
    message = json.loads(message)
    print("Received request: ", message)
    time.sleep(1)
    socket.send(b'loud and clear')
    # socket.send(b'World from %s' % port)



#
# import zmq
# import time
# import json
# import cv2
#
# def getFrames(vidpath):
#     cap = cv2.VideoCapture(vidpath)
#     print(vidpath)
#     if (cap.isOpened() == False):
#         print("Error opening video  file")
#     vid = []
#     while (cap.isOpened()):
#         ret, frame = cap.read()
#         if ret == True:
#             vid.append(frame.tolist())
#         else:
#             return vid
#     return vid

#
# port = "5556"
# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:%s" % port)
#
# # while True:
#     #  Wait for next request from client
#     # message = socket.recv_json()
#     # message = json.loads(message)
#     # print("Received request: ", message)
#     # time.sleep(13)
# tosend = []
# for i in range(1, 1):
#         # res = getFrames(str(i)+'.mp4')
#     tosend.append([getFrames(str(i)+'.mp4'), '11-3-2020', str(i), 'Omda'])
#
# comp = json.dumps(tosend)
# socket.send_json(comp)
#     # socket.send(b'World from %s' % port)