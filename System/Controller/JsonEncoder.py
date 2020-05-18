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

    def track(self,camera_id, starting_frame_id, frames, boxes,frame_width,frame_height,start_detect_time):
        func = TRACK
        sendingMsg = {FUNCTION: func,
                      CAMERA_ID: camera_id,
                      STARTING_FRAME_ID: starting_frame_id,
                      FRAMES: frames,
                      BOXES: boxes,
                      FRAME_WIDTH:frame_width,
                      FRAME_HEIGHT:frame_height,
                      START_DETECT_TIME:start_detect_time,
                      END_DETECT_TIME:time()}

        self.send(TRACKIP, TRACKPORT, sendingMsg)

    def crash(self,camera_id, starting_frame_id, frames, trackers,start_detect_time,end_detect_time,start_track_time):
        func = CRASH
        sendingMsg = {FUNCTION: func,
                      CAMERA_ID: camera_id,
                      STARTING_FRAME_ID: starting_frame_id,
                      FRAMES: frames,
                      TRACKERS: trackers,
                      START_DETECT_TIME: start_detect_time,
                      END_DETECT_TIME: end_detect_time,
                      START_TRACK_TIME: start_track_time,
                      END_TRACK_TIME: time()}

        # jsons = json.dumps(sendingMsg)
        self.send(CRASHIP, CRASHPORT, sendingMsg)


    def result(self,camera_id,starting_frame_id,crash_dimentions,start_detect_time,end_detect_time,start_track_time,end_track_time,start_crash_time):
        func = PROCESSED
        end_crash_time = time()
        sendingMsg = {FUNCTION: func,
                      CAMERA_ID: camera_id,
                      STARTING_FRAME_ID: starting_frame_id,
                      CRASH_DIMENTIONS: crash_dimentions,
                      START_DETECT_TIME:start_detect_time,
                      END_DETECT_TIME:end_detect_time,
                      START_TRACK_TIME:start_track_time,
                      END_TRACK_TIME:end_track_time,
                      START_CRASH_TIME:start_crash_time,
                      END_CRASH_TIME:end_crash_time}
        print(end_detect_time - start_detect_time + end_track_time - start_track_time + end_crash_time - start_crash_time)
        # self.send(MASTERIP, MASTERPORT, sendingMsg)




    #send duplication request to the data node
    def duplicate(self,userId,fileName,senderNodeIp,senderNodePort,receiverNodeIp,recieverNodePort):
        func = "duplicate_request"
        sendingMsg = {"func":func,
                      "user_id":userId,
                      "file_name":fileName,
                      "receiver_ip":receiverNodeIp,
                      "receiver_port":recieverNodePort}

        jsons = json.dumps(sendingMsg)
        self.send(senderNodeIp,senderNodePort,jsons)


    def uploadReqSuccess(self,nodeIp,nodePort,receiverIp):
        func = "upload_req_success"
        sendingMsg = {"func":func,
                      "node_ip":nodeIp,
                      "node_port":nodePort}

        jsons = json.dumps(sendingMsg)
        self.send(receiverIp,3000,jsons)

    def uploadReqFailed(self,msg,reason,fileName,receiverIp):
        func = "upload_req_failed"
        sendingMsg = {"func":func,
                      "msg":msg,
                      "reason":reason,
                      "file_name":fileName}

        jsons = json.dumps(sendingMsg)
        self.send(receiverIp,3000,jsons)


    def showFiles(self,fileArray,sizesArray,receiverIp):
        func = "show_files"
        sendingMsg = {"func":func,
                      "files":fileArray,
                      "fileSizes":sizesArray}

        jsons = json.dumps(sendingMsg)
        self.send(receiverIp,3000,jsons)



    def downloadReqFailed(self,msg,fileName,receiverIp):
        func = "download_req_failed"
        sendingMsg = {"func":func,
                      "msg":msg,
                      "file_name":fileName}

        jsons = json.dumps(sendingMsg)
        self.send(receiverIp,3000,jsons)

    def downloadIpsPorts(self,ips,ports,receiverIp):
        func = "download_ips_ports"
        sendingMsg = {"func":func,
                      "ips":ips,
                      "ports":ports,
                      }

        jsons = json.dumps(sendingMsg)
        self.send(receiverIp,3000,jsons)

