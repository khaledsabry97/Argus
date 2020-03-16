from time import time

import cv2

from Mosse_Tracker.Mosse import MOSSE
from Mosse_Tracker.utils import RectSelector


class Tracker:
    def __init__(self, srcVid, paused = False):
        self.cap = cv2.VideoCapture(srcVid)
        ret, self.frame = self.cap.read()
        if not ret:
            print("ERROR: not return any feed from this src vid"+srcVid)
            return
        cv2.imshow('frame', self.frame)
        self.rect_sel = RectSelector('frame', self.onrect)
        self.trackers = []
        self.paused = paused

    def onrect(self, rect):
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        tracker = MOSSE(frame_gray, rect)
        self.trackers.append(tracker)

    def run(self):
        f = 1
        cum = 0
        while True:
            if not self.paused:
                ret, self.frame = self.cap.read()
                if not ret:
                    break
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                for tracker in self.trackers:
                    t = time()
                    tracker.updateTracking(frame_gray)
                    cum += time() -t
                    f+=1

            vis = self.frame.copy()
            for tracker in self.trackers:
                tracker.draw_state(vis)
            if len(self.trackers) > 0:
                cv2.imshow('tracker state', self.trackers[-1].state_vis)
            self.rect_sel.draw(vis)

            cv2.imshow('frame', vis)
            ch = cv2.waitKey(10)
            if ch == 27:
                break
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == ord('c'):
                self.trackers = []
            if f%90 == 0:
                print(f/cum)


if __name__ == '__main__':
    print (__doc__)
    import sys, getopt
    opts, args = getopt.getopt(sys.argv[1:], '', ['pause'])
    opts = dict(opts)
    try:
        video_src = args[0]
    except:
        video_src = '0'

    Tracker(video_src, paused ='--pause' in opts).run()