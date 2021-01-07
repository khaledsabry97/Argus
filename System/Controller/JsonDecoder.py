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
from System.NodeType import NodeType
from VIF.vif import VIF


class JsonDecoder(threading.Thread):

    def __init__(self, type=None, read_file=False, tf=False):
        threading.Thread.__init__(self)
        self.sender_encode = JsonEncoder()
        self.yolo = None
        self.read_file = read_file
        self.tf = tf
        if type == NodeType.Detetion and not read_file:
            if tf:
                self.yolo = YOLO()
            else:
                self.yolo = YOLO()
        self.vif = None
        if NodeType.Crashing == type:
            self.vif = VIF()

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
            city =msg[CITY]
            district_no = msg[DISTRICT]

            self.feed(camera_id, starting_frame_id, frames, frame_width, frame_height, read_file, boxes_file,city,district_no)

        elif func == DETECT:    #2nd step: detect cars in the first frame
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            read_file = msg[READ_FILE]
            boxes_file = msg[BOXES]
            city =msg[CITY]
            district_no = msg[DISTRICT]

            self.detect(camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file,city,district_no)


        elif(func == TRACK):    #3rd step: track given cars in the first frame over the next 29 frames
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            frame_width = msg[FRAME_WIDTH]
            frame_height = msg[FRAME_HEIGHT]
            boxes = msg[BOXES]
            city =msg[CITY]
            district_no = msg[DISTRICT]
            start_detect_time = msg[START_DETECT_TIME]
            end_detect_time = msg[END_DETECT_TIME]


            self.track(camera_id,starting_frame_id,frames,frame_width,frame_height,boxes,start_detect_time,end_detect_time,city,district_no)

        elif func == CRASH: #4th step: check if any car did a crash or not
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            frames = msg[FRAMES]
            trackers = msg[TRACKERS]
            city =msg[CITY]
            district_no = msg[DISTRICT]
            start_detect_time = msg[START_DETECT_TIME]
            end_detect_time = msg[END_DETECT_TIME]
            start_track_time = msg[START_TRACK_TIME]
            end_track_time = msg[END_TRACK_TIME]

            self.crash(camera_id,starting_frame_id,frames,trackers,start_detect_time,end_detect_time,start_track_time,end_track_time,city,district_no)

        elif func == RESULT:    #5th step: send the result to the master to send notification and save accident or send and save none if not an accident
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            crash_dimentions = msg[CRASH_DIMENTIONS]
            city =msg[CITY]
            district_no = msg[DISTRICT]

            self.result(camera_id,starting_frame_id,crash_dimentions,city,district_no)

        elif func == SEARCH:
            start_date = msg[START_DATE]
            end_date = msg[END_DATE]
            start_time = msg[START_TIME]
            end_time = msg[END_TIME]
            city =msg[CITY]
            district = msg[DISTRICT]
            self.query(start_date,end_date,start_time,end_time,city,district)
        elif func == REQ_VIDEO:
            camera_id = msg[CAMERA_ID]
            starting_frame_id = msg[STARTING_FRAME_ID]
            self.reqVideo(camera_id,starting_frame_id)

        elif func == RECENT_CRASHES:
            self.sendRecentCrashes()


    def feed(self,camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file,city,district_no):
        master = Master()

        master.saveFrames(camera_id, starting_frame_id, frames, frame_width, frame_height)
        self.sender_encode.detect(camera_id, starting_frame_id, frames, frame_width, frame_height, read_file,
                                  boxes_file,city,district_no)

    def detect(self,camera_id,starting_frame_id,frames,frame_width,frame_height,read_file,boxes_file,city,district_no):
        start_detect_time = time()
        # if not read_file and self.yolo == None:
        #     self.yolo = YOLO()

        detection = Detection(self.yolo)

        boxes = detection.detect(frames, frame_width, frame_height, read_file, boxes_file, self.read_file, self.tf)
        self.sender_encode.track(camera_id, starting_frame_id, frames, boxes, frame_width, frame_height,start_detect_time,city,district_no)


    def track(self,camera_id,starting_frame_id,frames,frame_width,frame_height,boxes,start_detect_time,end_detect_time,city,district_no):
        start_track_time = time()
        track = Tracking()
        trackers = track.track(frames, boxes, frame_width, frame_height)
        self.sender_encode.crash(camera_id, starting_frame_id, frames, trackers, start_detect_time, end_detect_time,start_track_time,city,district_no)


    def crash(self,camera_id,starting_frame_id,frames,trackers,start_detect_time,end_detect_time,start_track_time,end_track_time,city,district_no):
        if self.vif == None:
            self.vif = VIF()

        start_crash_time = time()
        crashing = Crashing(self.vif)
        crash_dimentions = crashing.crash(frames, trackers)
        self.sender_encode.result(camera_id, starting_frame_id, crash_dimentions, start_detect_time, end_detect_time,start_track_time, end_track_time, start_crash_time,city,district_no)

    def result(self, camera_id, starting_frame_id, crash_dimentions,city,district_no):
        master = Master()
        master.checkResult(camera_id, starting_frame_id, crash_dimentions,city,district_no)


    def query(self,start_date,end_date,start_time,end_time,city,district):
         master = Master()
         master.executeQuery(start_date,end_date,start_time,end_time,city,district)

    def reqVideo(self, camera_id, starting_frame_id):
        master = Master()
        master.sendVideoToGUI(camera_id,starting_frame_id)

    def sendRecentCrashes(self):
        master = Master()
        master.sendRecentCrashesToGUI()