import json
import threading
from time import time

from System.Controller.JsonEncoder import JsonEncoder
from System.Data.CONSTANTS import *
from System.Functions.Crashing import Crashing
from System.Functions.Detection import Detection
from System.Functions.Tracking import Tracking
from VIF.vif import VIF


class JsonDecoder(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.msg = None
        self.sender_encode = JsonEncoder()
        self.vif = None

    def run(self,message):
        self.msg = message
        self.decode()


    def decode(self):
        msg = self.msg
        func = msg[FUNCTION]

        if(func == DETECT):
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            read_file = msg[READ_FILE]
            boxes_file = msg[BOXES]

            start_detect_time = time()
            detection = Detection()
            boxes = detection.detect(frames,frame_width,frame_height,read_file,boxes_file)
            self.sender_encode.track(camera_id,starting_frame_id,frames,boxes,frame_width,frame_height,start_detect_time)


        elif(func == TRACK):
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            boxes = msg[BOXES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            start_detect_time = msg[START_DETECT_TIME]
            end_detect_time = msg[END_DETECT_TIME]

            start_track_time = time()
            track = Tracking()
            trackers = track.track(frames,boxes,frame_width,frame_height)
            self.sender_encode.crash(camera_id,starting_frame_id,frames,trackers,start_detect_time,end_detect_time,start_track_time)

        elif(func == CRASH):
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            trackers = msg[TRACKERS]
            start_detect_time = msg[START_DETECT_TIME]
            end_detect_time = msg[END_DETECT_TIME]
            start_track_time = msg[START_TRACK_TIME]
            end_track_time = msg[END_TRACK_TIME]
            if self.vif == None:
                self.vif = VIF()

            start_crash_time = time()
            crashing = Crashing(self.vif)
            crash_dimentions = crashing.crash(frames,trackers)
            self.sender_encode.result(camera_id,starting_frame_id,crash_dimentions,start_detect_time,end_detect_time,start_track_time,end_track_time,start_crash_time)


