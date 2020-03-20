from time import time

import cv2

from Mosse_Tracker.Mosse import MOSSE
from Mosse_Tracker.common import draw_str
from Mosse_Tracker.utils import RectSelector

import sys, getopt

global id
id = 0
global frames
frames = []
class Tracker:
    def __init__(self, frame,cut_size,frame_width,frame_height,id =0):
        self.history = []
        self.tracker = MOSSE(frame, cut_size,learning_rate=0.225,psrGoodness=5)
        self.addHistory(self.tracker.getCutFramePosition())
        self.frame_width =frame_width
        self.frame_height= frame_height
        self.id =id
        self.index = 0

    #add current cut frame in history for later use
    #only append the dimensins : [xmin,ymin,xmax,ymax]
    def addHistory(self,cut_size):
        self.history.append(cut_size)

    #get history in :[[xmin,ymin,xmax,ymax]]
    def getHistory(self):
        return self.history

    #update the tracker to current frame
    #also add the updated position to history
    def update(self, frame):
        self.tracker.updateTracking(frame)
        self.addHistory(self.tracker.getCutFramePosition())
        return self.history[-1]

    #get last tracker position
    def getTrackerPosition(self):
        return self.history[-1]

    #get dimensions of the history to be able to make video clip later
    def getTrackedFramesBoxed(self,last_no_of_frame = 0):
        xmin = self.history[-1][0]
        ymin = self.history[-1][1]
        xmax = self.history[-1][2]
        ymax = self.history[-1][3]
        num_of_frames = len(self.history)
        if last_no_of_frame != 0:
            num_of_frames = last_no_of_frame
        size = len(self.history)
        for i in range(size-2,size-num_of_frames-1,-1):
            position = self.history[i]
            if position[0] < xmin:
                xmin = position[0]
            if position[1] < ymin:
                ymin = position[1]
            if position[2] > xmax:
                xmax = position[2]
            if position[3] > ymax:
                ymax = position[3]

        xmin = int(max(xmin,0))
        ymin = int(max(ymin,0))
        xmax = int(min(xmax,self.frame_width))
        ymax = int(min(ymax,self.frame_height))

        return xmin,ymin,xmax,ymax

    def showFrame(self, frame):
        (x, y) = self.tracker.getCenterOfTracker()

        xmin, ymin, xmax, ymax = self.tracker.getCutFramePosition()
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255))
        if self.tracker.isGood():
            cv2.circle(frame, (int(x), int(y)), 2, (0, 0, 255), -1)
        else:
            cv2.line(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255))
            cv2.line(frame, (xmax, ymin), (xmin, ymax), (0, 0, 255))

        draw_str(frame, (xmin, ymax + 16), 'Id: %i' % self.id)
        draw_str(frame, (xmin, ymax + 32), 'PSR: %.2f' % self.tracker.getPsr())
        draw_str(frame, (xmin, ymax + 48), 'L_R: %.2f' % self.tracker.getLearningRate())

    def clearHistory(self):
        self.history = []

    def saveTracking(self):
        global frames
        if len(self.history) < 30:
            return
        last_no_of_frames = 30
        xmin, ymin, xmax, ymax = self.getTrackedFramesBoxed(last_no_of_frames)

        width,height = xmax-xmin,ymax-ymin
        out = cv2.VideoWriter('./track_videos/'+ str(self.id)+") "+str(self.index) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (width, height))


        size = len(frames)
        for i in range(size-last_no_of_frames,size,1):
            frame = frames[i][ymin:ymax, xmin:xmax]
            out.write(frame)
        print("tracker_id "+str(self.id)+" saved!")
        self.index+=1
        out.release()



class TrackerManager:
    def __init__(self, srcVid, paused = False , test = True):
        self.cap = cv2.VideoCapture(srcVid)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ret, self.frame = self.cap.read()
        if not ret:
            print("ERROR: not return any feed from this src vid"+srcVid)
            return
        cv2.imshow('frame', self.frame)
        self.rect_sel = RectSelector('frame', self.select)
        self.trackers = []
        self.paused = paused
        self.frames=[]

    def select(self, rect):
        global id
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        tracker = Tracker(frame_gray,rect,self.frame_width,self.frame_height,id)
        id+=1
        # tracker = MOSSE(frame_gray, rect)
        self.trackers.append(tracker)


    def run(self):
        f = 1
        cum = 0
        global frames
        while True:
            if not self.paused:
                ret, self.frame = self.cap.read()
                if not ret:
                    break
                frames.append(self.frame.copy())
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                t = time()
                for tracker in self.trackers:
                    f+=1
                    tracker.update(frame_gray)
                    # tracker.updateTracking(frame_gray)
                    cum += time() -t
                # print(time() - t )

            vis = self.frame.copy()
            for tracker in self.trackers:
                tracker.showFrame(vis)
            if len(self.trackers) > 0:
                cv2.imshow('tracker state', self.trackers[-1].tracker.state_vis)
            self.rect_sel.draw(vis)

            cv2.imshow('frame', vis)
            ch = cv2.waitKey(10)
            if ch == 27:
                break
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == ord('c'):
                self.trackers = []
            if f%30 == 0:
                for tracker in self.trackers:
                    tracker.saveTracking()
                # print(f/cum)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '', ['pause'])
    opts = dict(opts)
    src = args[0]
    tracker_manager =TrackerManager(src, paused ='--pause' in opts)
    tracker_manager.run()