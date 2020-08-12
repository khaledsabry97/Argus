import base64
import copy
import json
import pickle
from io import BytesIO
from time import time, sleep

import numpy as np
import cv2
from PIL import Image
import threading
from System.Connections.SenderController import SenderController
from System.Controller.JsonEncoder import JsonEncoder
from System.Data.CONSTANTS import *
from yoloFiles import loadFile


class CameraNode(threading.Thread):

    def __init__(self,camera_id,file_path = None,files = True,city = "None",district_no = "None"):
        threading.Thread.__init__(self)
        self.camera_id = camera_id  #speical id for every camera
        self.read_file = files  #do you want to read detected cars from file ?
        self.file_path= file_path   #file path if you want to detect cars from file
        self.no_of_frames = 0   #current no of frames processed by the camera
        self.frame_width = 480  #camera resolution from frame width
        self.frame_height = 360 #camera resolution from frame height
        self.city = city
        self.district_no = district_no
        self.json_encoder = JsonEncoder()

    def run(self):
        self.startStreaming()

    def startStreaming(self):

        if self.read_file:
            fileBoxes = loadFile(self.file_path) #return boxes of cars in the frames

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

                self.json_encoder.feed(self.camera_id,self.no_of_frames -29,new_frames_list,self.frame_width,self.frame_height,self.read_file,new_boxes,self.city,self.district_no)
                # current_time = time() - t
                # sleep(max(1-current_time,0))
                # sleep(0.5)
                print(int(self.no_of_frames/30))
                # sleep(20)
                # t = time()
            if self.no_of_frames %30 == 0:
                current_time = time() - t
                print(max(1 - current_time, 0))
                # sleep((max(1-current_time,0))/2)
                t = time()






