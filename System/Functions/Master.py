import os

import cv2

from System.Data.CONSTANTS import *
from System.Database.DatabaseConnection import DatabaseConnection


class Master:
    def __init__(self):
        self.database = DatabaseConnection()


    def saveFrames(self,camera_id,starting_frame_id,frames,frame_width,frame_height):
        self.write(camera_id,frames,starting_frame_id,frame_width,frame_height,False)
        self.database.insertSavedFramesVid(camera_id,starting_frame_id)



    def write(self,camera_id,frames,starting_frame_id,frame_width,frame_height,is_crash = False ):
        if is_crash:
            folder = "saved_crash_vid"
        else:
            folder = "saved_frames_vid"

        file_path = './'+folder+'/' +"(" + str(camera_id) + ") " + str(starting_frame_id) + '.avi'
        if (not os.path.exists(folder)):
            os.makedirs(folder)
        out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))

        size = len(frames)
        for i in range(size):
            out.write(frames[i])
        print("camera_id_"+str(camera_id)+"_" + str(starting_frame_id) + folder+" saved!" + str(size))
        out.release()

    def getVideoFrames(self,camera_id,frame_id,is_crash = False):
        folder = "saved_frames_vid"
        if is_crash:
            folder = "saved_crash_vid"

        file_path = './'+folder+'/' + "(" + str(camera_id) + ") " + str(frame_id) + '.avi'
        cap = cv2.VideoCapture(file_path)

        frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        return frames



    def recordCrash(self,camera_id,starting_frame_id,crash_dimensions):

        new_frames = []
        from_no_of_times = PRE_FRAMES_NO

        while from_no_of_times >= 0:
            last_frames = from_no_of_times * 30
            new_frames_id = starting_frame_id - last_frames
            if new_frames_id > 0:
                new_frames.extend(self.getVideoFrames(camera_id,new_frames_id,False))
                frame_width = len(new_frames[0][0])
                frame_height = len(new_frames[0])

            from_no_of_times -=1


        xmin = crash_dimensions[0]
        ymin = crash_dimensions[1]
        xmax = crash_dimensions[2]
        ymax = crash_dimensions[3]
        #
        # if len(new_frames) >= 90:
        #     for i in range(len(new_frames) - 90, len(new_frames) - 60, 8):
        #         fill = -1
        #         cv2.rectangle(new_frames[i], (xmin, ymin), (xmax, ymax), (0, 0, 255), fill)
        #         cv2.putText(new_frames[i], "Crash!", (12, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 4)
        if len(new_frames) > 60:
            no_of_frames = 3
        elif len(new_frames) > 30:
            no_of_frames = 2
        else:
            no_of_frames =1

        if len(new_frames) >= 60:
            for i in range(len(new_frames)-60, len(new_frames)-30,6):
                fill = -1
                cv2.rectangle(new_frames[i], (xmin, ymin), (xmax, ymax), (0, 0, 255), fill)
                # cv2.rectangle(new_frames[i], (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

                cv2.putText(new_frames[i], "Crash!", (12, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 4)
            no_of_frames = 3
        for i in range(len(new_frames)-30,len(new_frames),2):
            fill = -1
            cv2.rectangle(new_frames[i], (xmin,ymin), (xmax,ymax), (0,0,255),fill)
            # cv2.rectangle(new_frames[i], (xmin,ymin), (xmax,ymax), (0,0,255),1)

            cv2.putText(new_frames[i], "Crash!", (12,  40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 4)

        self.write(camera_id, new_frames, starting_frame_id, frame_width, frame_height, True)
        return no_of_frames

    def checkResult(self,camera_id,starting_frame_id,crash_dimentions):
        if len(crash_dimentions) == 0:
            return

        no_of_from_no = self.recordCrash(camera_id,starting_frame_id,crash_dimentions)
        self.database.insertCrashFramesVid(camera_id,starting_frame_id,PRE_FRAMES_NO+1)





