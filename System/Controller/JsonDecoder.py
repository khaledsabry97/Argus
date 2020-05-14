import json
import threading

from System.Controller.JsonEncoder import JsonEncoder
from System.Data.CONSTANTS import *
from System.Functions.Crashing import Crashing
from System.Functions.Detection import Detection
from System.Functions.Tracking import Tracking



class JsonDecoder(threading.Thread):

    def __init__(self,jsons):
        threading.Thread.__init__(self)
        self.jsons = jsons
        self.sender_encode = JsonEncoder()

    def run(self):
            self.decode()


    def decode(self):
        jsons = self.jsons
        func = jsons[FUNCTION]

        if(func == DETECT):
            camera_id = jsons[CAMERA_ID]
            starting_frame_id = jsons[STARTING_FRAME_ID]
            frames = jsons[FRAMES]
            frame_width = jsons[FRAME_WIDTH]
            frame_height = jsons[FRAME_HEIGHT]
            read_file = jsons[READ_FILE]
            boxes_file = jsons[BOXES]

            detection = Detection()
            trackers = detection.detect(frames,frame_width,frame_height,read_file,boxes_file)
            self.sender_encode.track(camera_id,starting_frame_id,frames,trackers)


        elif(func == TRACK):
            camera_id = jsons[CAMERA_ID]
            starting_frame_id = jsons[STARTING_FRAME_ID]
            frames = jsons[FRAMES]
            trackers= jsons[TRACKERS]

            track = Tracking()
            trackers = track.track(frames,trackers)
            self.sender_encode.crash(camera_id,starting_frame_id,frames,trackers)

        elif(func == CRASH):
            camera_id = jsons[CAMERA_ID]
            starting_frame_id = jsons[STARTING_FRAME_ID]

            frames = jsons[FRAMES]
            trackers = jsons[TRACKERS]
            crashing = Crashing()
            crash_dimentions = crashing.crash(frames,trackers)
            self.sender_encode.result(camera_id,starting_frame_id,crash_dimentions)


