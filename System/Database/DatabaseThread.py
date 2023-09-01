import threading
from time import sleep

from System.Data.CONSTANTS import *
from System.Database.DatabaseConnection import DatabaseConnection
from System.Functions.Master import Master


class DatabaseThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.database = DatabaseConnection()
        self.master = Master()

    def run(self):
        while True:
            pending_crashes = self.database.selectCrashFrames()
            if pending_crashes != None:

                for pending_crash in pending_crashes:
                    camera_id = pending_crash[0]
                    starting_frame_id = pending_crash[1]
                    from_no = pending_crash[2]
                    current_frames_id = self.database.selectSavedFrames(camera_id,starting_frame_id)
                    limit = TOTAL_FRAMES_NO-from_no
                    new_limit = 0
                    if len(current_frames_id) == 0:
                        continue

                    frames = self.master.getVideoFrames(camera_id,starting_frame_id,True)
                    temp = starting_frame_id + (from_no - PRE_FRAMES_NO - 1)*30
                    for frame_id in current_frames_id:
                        frame_id = frame_id[0]
                        if new_limit == limit:
                            break
                        if temp + 30 != frame_id:
                            continue
                        temp +=30
                        frames.extend(self.master.getVideoFrames(camera_id, temp, False))
                        new_limit+=1
                    new_from_no = from_no + new_limit
                    if (frames == None or len(frames) == 0):
                        continue
                    frame_width = len(frames[0][0])
                    frame_height = len(frames[0])

                    if new_from_no > 5:
                        print("Above")
                    self.master.write(camera_id,frames,starting_frame_id,frame_width,frame_height,True)
                    self.database.updateCrashFramesVid(camera_id,starting_frame_id,new_from_no)

            # self.deleteExceeded()
            sleep(1)
    # def deleteExceeded(self):
    #     self.database.deleteCrashFramesVid()


