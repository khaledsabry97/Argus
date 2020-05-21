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
                    camera_id = pending_crash[1]
                    starting_frame_id = pending_crash[2]
                    from_no = pending_crash[3]
                    current_frames_id = self.database.selectSavedFrames(camera_id,starting_frame_id)
                    limit = TOTAL_FRAMES_NO-from_no
                    #current_frames_id = current_frames_id[:TOTAL_FRAMES_NO-from_no]
                    new_from_no = from_no + len(current_frames_id)
                    new_limit = 0
                    if len(current_frames_id) == 0:
                        continue
                    exchange = 1
                    if (starting_frame_id-16)% 30 == 0:
                        exchange = 16
                    frames = self.master.getVideoFrames(camera_id,starting_frame_id,True)
                    for frame_id in current_frames_id:
                        frame_id = frame_id[0]
                        if new_limit == limit:
                            break
                        if (exchange == 16 and (frame_id-16)% 30 != 0) or (exchange == 1 and (frame_id-1)% 30 != 0):
                            continue
                        frames.extend(self.master.getVideoFrames(camera_id, frame_id, False))
                        limit+=1

                    frame_width = len(frames[0][0])
                    frame_height = len(frames[0])


                    self.master.write(camera_id,frames,starting_frame_id,frame_width,frame_height,True)
                    self.database.updateCrashFramesVid(camera_id,starting_frame_id,new_from_no)

            # self.deleteExceeded()
            sleep(1)
    # def deleteExceeded(self):
    #     self.database.deleteCrashFramesVid()


