import zmq
import sys
import json
port = "5556"
import cv2

def getFrames(vidpath):
    cap = cv2.VideoCapture(vidpath)
    print(vidpath)
    if (cap.isOpened() == False):
        print("Error opening video  file")
    vid = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            vid.append(frame.tolist())
        else:
            return vid
    return vid

context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
# message = socket.recv_json()
res = getFrames('1.mp4')
print(len(res))
# for request in range (1,10):
print("Sending request ", 1, "...")
socket.send_json(json.dumps([res, [1,1,1,1], 'Hello']))
#  Get the reply.
message = socket.recv()
print("Received reply ", 1, "[", message, "]")