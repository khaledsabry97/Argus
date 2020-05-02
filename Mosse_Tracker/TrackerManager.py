from threading import Thread
from time import time
import math

import cv2
from copy import deepcopy

from Mosse_Tracker.Mosse import MOSSE
from Mosse_Tracker.utils import draw_str
from Mosse_Tracker.utils import RectSelector

import sys, getopt
pi=22/7

global id
id = 0
global frames
frames = []

class Tracker:
    def __init__(self, frame, cut_size, frame_width, frame_height, tracker_id =0):
        self.history = []
        self.tracker = MOSSE(frame, cut_size,learning_rate=0.225,psrGoodness=5)
        self.addHistory(self.tracker.getCutFramePosition())
        self.frame_width =frame_width
        self.frame_height= frame_height
        self.tracker_id =tracker_id
        self.index = 0
        self.estimationFutureCenter = [-1]*30

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
    def getTrackedFramesBoxed(self,last_no_of_frame = 0,after_no_of_frames = 1):
        xmin = self.history[-after_no_of_frames][0]
        ymin = self.history[-after_no_of_frames][1]
        xmax = self.history[-after_no_of_frames][2]
        ymax = self.history[-after_no_of_frames][3]
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
        #draw_str(frame, (xmin, ymax + 16), 'Id: %i' % self.tracker_id)
        #draw_str(frame, (xmin, ymax + 32), 'PSR: %.2f' % self.tracker.getPsr())
        draw_str(frame, (xmin, ymax + 64), 'Max Speed: %.2f' % self.getMaxSpeed())
        draw_str(frame, (xmin, ymax + 80), 'Avg Speed: %.2f' % self.getAvgSpeed())
        draw_str(frame, (xmin, ymax + 96), 'Cur Speed: %.2f' % self.getCurrentSpeed())
        draw_str(frame, (xmin, ymax + 112), 'Area Size: %.2f' % self.getCarSizeCoefficient())
        draw_str(frame, (xmin, ymax + 128), 'Moving Angle: %.2f' % self.getCarAngle())

    def clearHistory(self):
        self.history = []

    def saveTracking(self,frames):
        new_frames,width,height,_,_,_,_ = self.getFramesOfTracking(frames)
        if new_frames == None:
            return
        out = cv2.VideoWriter('./track_videos/' + str(self.tracker_id) + ") " + str(self.index) + '.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (width, height))

        size = len(new_frames)
        for i in range(size):
            out.write(new_frames[i])
        print("tracker_id " + str(self.tracker_id) + " saved!")
        self.index+=1
        out.release()



    def getMaxSpeed(self):
        x = max(self.tracker.dx)
        y = max(self.tracker.dy)
        r = pow(pow(x,2)+pow(y,2),0.5)
        r_coefficient = r * self.getCarSizeCoefficient()
        return r_coefficient
    def getAvgSpeed(self):
        x = sum(self.tracker.dx)/len(self.tracker.dx)
        y = sum(self.tracker.dy)/len(self.tracker.dy)
        r = pow(pow(x, 2) + pow(y, 2), 0.5)
        r_coefficient = r * self.getCarSizeCoefficient()
        return r_coefficient

    def getCurrentSpeed(self):
        no_of_last_frames = min(len(self.tracker.dx),3)
        x = sum(self.tracker.dx[-no_of_last_frames:]) / no_of_last_frames
        y = sum(self.tracker.dy[-no_of_last_frames:]) / no_of_last_frames
        r = pow(pow(x, 2) + pow(y, 2), 0.5)
        r_coefficient = r * self.getCarSizeCoefficient()
        return r_coefficient

    def getCarSizeCoefficient(self):
        area = 0.5 * self.tracker.width * self.tracker.height
        coefficient = 25000/area
        return coefficient


    def getCarAngle(self):
        max_index_to_measure = min(1000,len(self.tracker.dx))
        dx = sum(self.tracker.dx[:max_index_to_measure])
        dy = sum(self.tracker.dy[:max_index_to_measure])
        is_dx_sign_pos = True
        if dx < 0:
            is_dx_sign_pos = False

        is_dy_sign_pos = True
        if dy < 0:
            is_dy_sign_pos = False
        if dx == 0:
            if dy > 0:
                return 270
            elif dy < 0:
                return 90
            else:
                return -1

        degree = math.degrees(math.atan(abs(dy/dx)))
        #remember the y coordinate min at the left up corner so flip the graph
        if dx < 0 and dy >=0:
            return 180 + degree
        elif dx <0 and dy <= 0:
            return 180 - degree
        elif dx > 0 and dy <= 0:
            return  degree
        else:
            return 360 - degree


    def futureFramePosition(self, ):
        if len(self.tracker.dx) <5 or len(self.tracker.dx) > 18 :
            self.estimationFutureCenter.append(self.tracker.center)
            return -1,-1,-1,-1
        measure = min(len(self.tracker.dx),10)
        expectedPositionNo = len(self.tracker.dx)+10
        x,y = self.tracker.center
        dx = sum(self.tracker.dx[-measure:]) / len(self.tracker.dx[-measure:])
        dy = sum(self.tracker.dy[-measure:]) / len(self.tracker.dy[-measure:])
        x_new = x + dx*measure
        y_new = y + dy*measure
        self.estimationFutureCenter[expectedPositionNo] = (x_new,y_new)
        return self.tracker.getCutFramePosition((x_new,y_new))




    #get frames of box to enter it to vif descriptor or save it
    def getFramesOfTracking(self,frames,last_no_of_frames = 30):
        if len(self.history) < last_no_of_frames:
            return None,-1,-1,-1,-1,-1,-1
        xmin, ymin, xmax, ymax = self.getTrackedFramesBoxed(last_no_of_frames)

        width, height = xmax - xmin, ymax - ymin
        new_frames = []

        size = len(frames)
        for i in range(size - last_no_of_frames, size, 1):
            new_frames.append(frames[i][ymin:ymax, xmin:xmax])
        return new_frames,width,height,xmin,xmax,ymin,ymax

    def isAboveSpeedLimit(self):
        if self.getAvgSpeed() > 70:
            return True
        return False



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

    def saveTrackers(self,trackers):
        for tracker in self.trackers:
            tracker.saveTracking(frames)
    def run(self):
        f = 1
        cum = 0
        global frames
        while True:
            if not self.paused:
                ret, self.frame = self.cap.read()
                if not ret:
                    break
                dim = (480, 360)
                self.frame = cv2.resize(self.frame, dim, interpolation=cv2.INTER_AREA)
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
                #cv2.imshow('tracker state', self.trackers[-1].tracker.state_vis)
                pass
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
                thread = Thread(target=self.saveTrackers(self.trackers))
                thread.start()
                print(f/cum)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '', ['pause'])
    opts = dict(opts)
    src = args[0]
    tracker_manager =TrackerManager(src, paused ='--pause' in opts)
    tracker_manager.run()
