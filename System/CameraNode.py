import base64
import copy
import json
import pickle
from io import BytesIO
from time import time, sleep

import cv2
from PIL import Image

from System.Connections.SenderController import SenderController
from System.Data.CONSTANTS import *
from yoloFiles import loadFile


class CameraNode:

    def __init__(self,camera_id,file_path = None,files = True):
        self.camera_id = camera_id
        self.read_file = files
        self.file_path= file_path
        self.no_of_frames = 0
        self.frame_width = 480
        self.frame_height = 360


    def startStreaming(self):

        if self.read_file:
            fileBoxes = loadFile(self.file_path)

        cap = cv2.VideoCapture(self.file_path)
        frames = []
        boxes = []

        while True:
            t = time()
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (self.frame_width,self.frame_height), interpolation=cv2.INTER_AREA)
            frames.append(frame)
            if self.read_file:
                bboxes = fileBoxes[self.no_of_frames]
                boxes.append(bboxes)

            self.no_of_frames +=1
            if len(frames) == 30:
                new_frames_list = []
                for frame in frames:
                    img = self.im2json(frame)
                    new_img = self.json2im(img)
                    new_frames_list.append()
                frames = []
                new_boxes_list = copy.deepcopy(boxes)
                boxes = []
                self.makeJson(new_frames_list,new_boxes_list)
                current_time = (time() - t)/1000
                sleep(1-current_time)




    def makeJson(self,frames,boxes):
        t = time()

        sendingMsg = {FUNCTION:DETECT,
                      CAMERA_ID:self.camera_id,
                      STARTING_FRAME_ID:self.no_of_frames,
                      FRAMES:frames,
                      FRAME_WIDTH:self.frame_width,
                      FRAME_HEIGHT:self.frame_height,
                      READ_FILE:self.read_file,
                      BOXES:boxes}

        jsons = json.dumps(sendingMsg)
        print(time() - t)

        self.send(DETECTIP,DETECTPORT,jsons)

            # m = MainFlow(None, select=False)
            # m.run('videos/1508.mp4')

    def send(self,ip,port,json):
        thread = SenderController(ip,port,json)
        thread.start()

    def im2json(self,im):
        _, imdata = cv2.imencode('.JPG', im)
        jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
        return jstr

    def json2im(self,jstr):
        load = json.loads(jstr)
        imdata = base64.b64decode(load['image'])
        im = Image.open(BytesIO(imdata))
        return im




