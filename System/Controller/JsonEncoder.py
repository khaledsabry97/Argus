import json
import pickle as pickle
from time import time

from System.Connections.SenderController import SenderController
from System.Data.CONSTANTS import *


class JsonEncoder:

    def __init__(self):
       pass


    def send(self,ip,port,json):
        thread = SenderController(ip,port,json)
        thread.start()


    def detect(self,camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file,city,district_no):
        func = DETECT
        sendingMsg = {FUNCTION:func,
                      CAMERA_ID:camera_id,
                      STARTING_FRAME_ID:starting_frame_id,
                      FRAMES:frames,
                      FRAME_WIDTH:frame_width,
                      FRAME_HEIGHT:frame_height,
                      READ_FILE:read_file,
                      BOXES:boxes_file,
                      CITY:city,
                      DISTRICT_NO: district_no}

        self.send(DETECTIP, DETECTPORT, sendingMsg)

    def track(self,camera_id, starting_frame_id, frames, boxes,frame_width,frame_height,start_detect_time,city,district_no):
        func = TRACK
        sendingMsg = {FUNCTION: func,
                      CAMERA_ID: camera_id,
                      STARTING_FRAME_ID: starting_frame_id,
                      FRAMES: frames,
                      BOXES: boxes,
                      CITY: city,
                      DISTRICT_NO: district_no,
                      FRAME_WIDTH:frame_width,
                      FRAME_HEIGHT:frame_height,
                      START_DETECT_TIME:start_detect_time,
                      END_DETECT_TIME:time()}

        self.send(TRACKIP, TRACKPORT, sendingMsg)

    def crash(self,camera_id, starting_frame_id, frames, trackers,start_detect_time,end_detect_time,start_track_time,city,district_no):
        func = CRASH
        sendingMsg = {FUNCTION: func,
                      CAMERA_ID: camera_id,
                      STARTING_FRAME_ID: starting_frame_id,
                      FRAMES: frames,
                      TRACKERS: trackers,
                      CITY: city,
                      DISTRICT_NO: district_no,
                      START_DETECT_TIME: start_detect_time,
                      END_DETECT_TIME: end_detect_time,
                      START_TRACK_TIME: start_track_time,
                      END_TRACK_TIME: time()}

        # jsons = json.dumps(sendingMsg)
        self.send(CRASHIP, CRASHPORT, sendingMsg)


    def result(self,camera_id,starting_frame_id,crash_dimentions,start_detect_time,end_detect_time,start_track_time,end_track_time,start_crash_time,city,district_no):
        func = RESULT
        end_crash_time = time()
        sendingMsg = {FUNCTION: func,
                      CAMERA_ID: camera_id,
                      STARTING_FRAME_ID: starting_frame_id,
                      CRASH_DIMENTIONS: crash_dimentions,
                      CITY: city,
                      DISTRICT_NO: district_no,
                      START_DETECT_TIME:start_detect_time,
                      END_DETECT_TIME:end_detect_time,
                      START_TRACK_TIME:start_track_time,
                      END_TRACK_TIME:end_track_time,
                      START_CRASH_TIME:start_crash_time,
                      END_CRASH_TIME:end_crash_time}

        print("Detection time:"+str(end_detect_time - start_detect_time))
        print("Tracking time: "+str(end_track_time - start_track_time))
        print("Crashing time: " + str(end_crash_time - start_crash_time))
        print("Total Processing time: "+ str(end_detect_time - start_detect_time + end_track_time - start_track_time + end_crash_time - start_crash_time))

        self.send(MASTERIP, MASTERPORT, sendingMsg)




