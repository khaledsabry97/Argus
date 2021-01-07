from time import time

import cv2

from Mosse_Tracker.TrackerManager import Tracker


class Tracking:
    def __init__(self):
        pass

    def track(self,frames,boxes,frame_width,frame_height):
        trackers = []
        trackerId = 0
        frame = frames[0]
        for _, box in enumerate(boxes):
            xmin = int(box[1])
            xmax = int(box[2])
            ymin = int(box[3])
            ymax = int(box[4])

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            trackerId += 1
            # no need for frame_width and frame_height
            xmax = min(xmax, frame_width - 1)
            ymax = min(ymax, frame_height - 1)

            trackers.append(Tracker(frame_gray, (xmin, ymin, xmax, ymax), frame_width, frame_height, trackerId))
        t = time()
        tot = 0
        for i in range(1,len(frames)):
            frame = frames[i]
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # updating trackers
            for i, tracker in enumerate(trackers):
                tracker.update(frame_gray)
                t1 = time()
                tracker.futureFramePosition()

        return trackers
 