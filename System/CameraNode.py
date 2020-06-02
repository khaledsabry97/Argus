import base64
import copy
import json
import pickle
from io import BytesIO
from time import time, sleep

import numpy as np
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
        t = time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (self.frame_width,self.frame_height), interpolation=cv2.INTER_AREA)
            frames.append(frame)
            # if self.read_file and len(boxes) == 0:
            #     boxes.append(bboxes)

            self.no_of_frames +=1
            if len(frames) == 30:
                new_frames_list = []
                new_frames_list =copy.deepcopy(frames)
                frames = frames[15:]
                # frames = []
                new_boxes = fileBoxes[self.no_of_frames - 30]

                self.makeJson(new_frames_list,new_boxes)
                # current_time = time() - t
                # sleep(max(1-current_time,0))
                # sleep(0.5)
                print(int(self.no_of_frames/30))
                # sleep(20)
                # t = time()
            if self.no_of_frames %30 == 0:
                current_time = time() - t
                sleep(max(1-current_time,0))
                t = time()





    def makeJson(self,frames,boxes):

        sendingMsg = {FUNCTION:FEED,
                      CAMERA_ID:self.camera_id,
                      STARTING_FRAME_ID:self.no_of_frames -29,
                      FRAMES:frames,
                      FRAME_WIDTH:self.frame_width,
                      FRAME_HEIGHT:self.frame_height,
                      READ_FILE:self.read_file,
                      BOXES:boxes}

        self.send(MASTERIP,MASTERPORT,sendingMsg)

    def send(self,ip,port,json):
        thread = SenderController(ip,port,json)
        thread.run()

