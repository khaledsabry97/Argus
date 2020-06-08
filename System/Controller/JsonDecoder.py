import json
import threading
from time import time

# from Car_Detection_TF.yolo import YOLO
from System.Controller.JsonEncoder import JsonEncoder
from System.Data.CONSTANTS import *
from System.Functions.Crashing import Crashing
from System.Functions.Detection import Detection
from System.Functions.Master import Master
from System.Functions.Tracking import Tracking
from VIF.vif import VIF


class JsonDecoder(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sender_encode = JsonEncoder()
        self.yolo = None
        self.vif = None

    def run(self,message):
        self.decode(message)


    def decode(self,msg):
        func = msg[FUNCTION]

        if func == FEED:    #1st step: recieve feed from cctv camera
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            read_file = msg[READ_FILE]
            boxes_file = msg[BOXES]

            self.feed(camera_id, starting_frame_id, frames, frame_width, frame_height, read_file, boxes_file)

        elif func == DETECT:    #2nd step: detect cars in the first frame
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            read_file = msg[READ_FILE]
            boxes_file = msg[BOXES]

            self.detect(camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file)


        elif(func == TRACK):    #3rd step: track given cars in the first frame over the next 29 frames
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            boxes = msg[BOXES]
            start_detect_time = msg[START_DETECT_TIME]
            end_detect_time = msg[END_DETECT_TIME]

            self.track(camera_id,starting_frame_id,frames,frame_width,frame_height,boxes,start_detect_time,end_detect_time)

        elif func == CRASH: #4th step: check if any car did a crash or not
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            trackers = msg[TRACKERS]
            start_detect_time = msg[START_DETECT_TIME]
            end_detect_time = msg[END_DETECT_TIME]
            start_track_time = msg[START_TRACK_TIME]
            end_track_time = msg[END_TRACK_TIME]

            self.crash(camera_id,starting_frame_id,frames,trackers,start_detect_time,end_detect_time,start_track_time,end_track_time)

        elif func == RESULT:    #5th step: send the result to the master to send notification and save accident or send and save none if not an accident
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            crash_dimentions = msg[CRASH_DIMENTIONS]

            self.result(camera_id,starting_frame_id,crash_dimentions)


    def feed(self,camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file):
        master = Master()

        master.saveFrames(camera_id, starting_frame_id, frames, frame_width, frame_height)
        self.sender_encode.detect(camera_id, starting_frame_id, frames, frame_width, frame_height, read_file,
                                  boxes_file)

    def detect(self,camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file):
        start_detect_time = time()
        if not read_file and self.yolo == None:
            self.yolo = YOLO()
        detection = Detection(self.yolo)

        boxes = detection.detect(frames, frame_width, frame_height, read_file, boxes_file)
        self.sender_encode.track(camera_id, starting_frame_id, frames, boxes, frame_width, frame_height,start_detect_time)


    def track(self,camera_id,starting_frame_id,frames,frame_width,frame_height,boxes,start_detect_time,end_detect_time):
        start_track_time = time()
        track = Tracking()
        trackers = track.track(frames, boxes, frame_width, frame_height)
        self.sender_encode.crash(camera_id, starting_frame_id, frames, trackers, start_detect_time, end_detect_time,start_track_time)


    def crash(self,camera_id,starting_frame_id,frames,trackers,start_detect_time,end_detect_time,start_track_time,end_track_time):
        if self.vif == None:
            self.vif = VIF()

        start_crash_time = time()
        crashing = Crashing(self.vif)
        crash_dimentions = crashing.crash(frames, trackers)
        self.sender_encode.result(camera_id, starting_frame_id, crash_dimentions, start_detect_time, end_detect_time,start_track_time, end_track_time, start_crash_time)

    def result(self, camera_id, starting_frame_id, crash_dimentions):
        master = Master()
        master.checkResult(camera_id, starting_frame_id, crash_dimentions)