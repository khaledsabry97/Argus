
import numpy as np
import cv2

import math
import glob, os

from VIF.HornSchunck import HornSchunck


class VIF:
    def __init__(self):
        self.subSampling = 3
        self.hs = HornSchunck()

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

        flow = np.zeros([100, 134]) #rows cols
        index = 0
        N = 4
        M = 4

        for i in range(0, len(frames) - self.subSampling - 5, self.subSampling * 2):

            index += 1

            prev_f = frames[i + self.subSampling]
            curr_f = frames[i + self.subSampling * 2]
            next_f = frames[i + self.subSampling * 3]

            prev_f = cv2.resize(prev_f, (134, 100)) #width height
            curr_f = cv2.resize(curr_f, (134, 100))
            next_f = cv2.resize(next_f, (134, 100))

            #process optic flow
            #print("shapes", prev_f.shape, curr_f.shape)
            u1, v1, m1 = self.hs.HornSchunck(prev_f, curr_f)
            u2, v2, m2 = self.hs.HornSchunck(curr_f, next_f)

            delta = abs(m1 - m2)
            flow = flow + (delta > np.mean(delta))

        flow = flow.astype(float)
        if index > 0:
            flow = flow/index

        feature_vec = self.createBlockHist(flow, N, M)


        return feature_vec


'''
# para obtener vif de algunos videos
data = []
for file in glob.glob("dataset/BD_no_choques/subvideos/*.avi"):
    print(file)
    cap = cv2.VideoCapture(file)
    frames = []
    max_num_frames = 60
    count = 1
    vif = ViF()

    while True:
        ret, frame = cap.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)

        else:
            break

    obj = ViF()
    feature_vec = obj.process(frames)
    # print (feature_vec)
    data.append(feature_vec)

np.savetxt("data_no_choques.csv", data, delimiter=",")
'''


'''

cap = cv2.VideoCapture('../video-test/brucelee_1.mp4')
frames = []
max_num_frames = 60
count = 1
vif = ViF()

while True:
    ret, frame = cap.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)

        if count > max_num_frames:
            vif.process(frames)
            frames=[]
            count = 1

        count += 1

    else:
        break


cap.release()
cv2.destroyAllWindows()

'''