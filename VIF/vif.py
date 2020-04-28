import pickle

import numpy as np
import cv2

import math
import glob, os

from VIF.HornSchunck import HornSchunck


class VIF:
    def __init__(self):
        self.subSampling = 3
        self.rows = 100
        self.cols = 134
        self.hs = HornSchunck()
        self.clf = pickle.load(open("E:\Projects\GP_Crash_Saviour\VIF\model-svm1.sav", 'rb'))
        self.no_crash = 0
        self.crash = 0


    def createBlockHist(self, flow, N, M):

        height, width = flow.shape
        B_height = int(math.floor((height - 11) / N))
        B_width = int(math.floor((width - 11 ) / M))

        frame_hist = []
        #print height, B_height
        #print(np.arange(6, height - B_height - 5, B_height))

        for y in np.arange(6, height - B_height - 5, B_height):
            for x in np.arange(6, width - B_width - 5, B_width):
                block_hist = self.createHist(flow[y:y + B_height - 1, x:x + B_width - 1])
                #print(block_hist)
                frame_hist.append(block_hist)

        return np.array(frame_hist).flatten()

    def createHist(self, mini_flow):
        # print(mini_flow)
        H = np.histogram(mini_flow, np.arange(0, 1, 0.05))
        H = H[0]/float(np.sum(H[0]))
        return H

    def process(self, frames):
        #for img in frames:
            #cv2.imshow("win", img)
            #cv2.waitKey(30)
        #cv2.destroyAllWindows()
        flow = np.zeros([self.rows, self.cols]) #row, cols
        index = 0
        N = 4
        M = 4
        shape = (self.cols,self.rows)

        for i in range(0, len(frames) - self.subSampling - 5, self.subSampling * 2):

            index += 1
            # print(i + self.subSampling)
            # print(i + self.subSampling * 2)
            # print(i + self.subSampling * 3)
            prevFrame = frames[i + self.subSampling]
            currFrame = frames[i + self.subSampling * 2]
            nextFrame = frames[i + self.subSampling * 3]

            prevFrame = cv2.resize(prevFrame, shape)
            currFrame = cv2.resize(currFrame, shape)
            nextFrame = cv2.resize(nextFrame, shape)

            #process opticl flow
            #print("shapes", prev_f.shape, curr_f.shape)
            u1, v1, m1 = self.hs.process(prevFrame, currFrame)
            u2, v2, m2 = self.hs.process(currFrame, nextFrame)

            delta = abs(m1 - m2)
            flow = flow + (delta > np.mean(delta))

        flow = flow.astype(float)
        if index > 0:
            flow = flow/index

        feature_vec = self.createBlockHist(flow, N, M)


        return feature_vec



    def predict(self,frames_RGB,trackers):
        gray_frames = []
        for frame in frames_RGB:
            gray_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        print(len(frames_RGB))
        self.no_crash = 0
        self.crash = 0

        for tracker in trackers:
            tracker_frames,width,height,xmin,xmax,ymin,ymax = tracker.getFramesOfTracking(gray_frames)

            if tracker_frames == None:
                continue
            if xmax - xmin < 100:
                continue
            if ymax - ymin < 50:
                continue

            feature_vec = self.process(tracker_frames)
            result = self.clf.predict(feature_vec.reshape(1, 304))
            if result[0] == 0.0:
                self.no_crash += 1
            else:
                self.crash += 1
                tracker.saveTracking(frames_RGB)
        print(self.crash, self.no_crash)







