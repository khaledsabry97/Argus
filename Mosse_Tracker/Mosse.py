#!/usr/bin/env python

'''
MOSSE tracking sample

This sample implements correlation-based tracking approach, described in [1].

Usage:
  mosse.py [--pause] [<video source>]

  --pause  -  Start with playback paused at the first video frame.
              Useful for tracking target selection.

  Draw rectangles around objects with a mouse to track them.

Keys:
  SPACE    - pause video
  c        - clear targets

[1] David S. Bolme et al. "Visual Object Tracking using Adaptive Correlation Filters"
    http://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf
'''

from __future__ import print_function


import numpy as np
import cv2

from Mosse_Tracker.common import draw_str


def randomRotation(cut_img):
    #get width and height of the img
    height, width = cut_img.shape[:2]
    #make transformation matrix of size 2*3
    transformation = np.zeros((2, 3))

    perentage = 0.2

    #get angle rotation from 0 to 1
    ang = (np.random.rand()-0.5)*perentage

    cos, sin = np.cos(ang), np.sin(ang)
    transformation[:2, :2] = [[cos,-sin], [sin, cos]]
    transformation[:2, :2] += (np.random.rand(2, 2) - 0.5)*perentage

    #adding the last of transformation to the last index
    transformation[:,2] = (width/2, height/2) - np.dot(transformation[:2, :2], (width/2, height/2))
    #look for that :https://www.youtube.com/watch?v=il6Z5LCykZk
    transformed_img = cv2.warpAffine(cut_img, transformation, (width, height), borderMode = cv2.BORDER_REFLECT)
    return transformed_img

def HFilter(Num, Den):
    #applying the eq in the paper to  get the hfilter
    Num_real, Num_imaginary = Num[..., 0], Num[..., 1]
    Den_real, Den_imaginary = Den[..., 0], Den[..., 1]

    h_filter = (Num_real + 1j * Num_imaginary) / (Den_real + 1j * Den_imaginary)
    h_filter = np.dstack([np.real(h_filter), np.imag(h_filter)]).copy()
    return h_filter

eps = 1e-5

class MOSSE:
    def __init__(self, frame, cut_size,num_of_traning_imgs = 10,learning_rate = 0.225,psrGoodness = 10):
        #get the xmin and .... for all the corners in the cut_Size
        xmin, ymin, xmax, ymax = cut_size

        # w, h = map(cv2.getOptimalDFTSize, [xmax - xmin, ymax - ymin])
        self.learning_rate = learning_rate
        self.num_of_traning_imgs = num_of_traning_imgs
        self.psrGoodness = psrGoodness
        #get width and height of the cut_size
        self.width = xmax - xmin
        self.height = ymax - ymin


        # xmin, ymin = (xmin+xmax-width)//2, (ymin+ymax-height)//2
        self.center = x, y = xmin + 0.5 * (self.width - 1), ymin + 0.5 * (self.height - 1)
        self.size = self.width, self.height

        #take a capture of the frame
        img = cv2.getRectSubPix(frame, (self.width, self.height), (x, y))

        #creating window of the cut_size
        self.win = cv2.createHanningWindow((self.width, self.height), cv2.CV_32F)
        g = np.zeros((self.height, self.width), np.float32)

        g[int(self.height/2), int(self.width/2)] = 1
        g = cv2.GaussianBlur(g, (-1, -1), 3.0) #2.0
        g = g / g.max()

        self.G = cv2.dft(g, flags=cv2.DFT_COMPLEX_OUTPUT)
        # c = self.preprocess(rnd_warp(img))


        self.prepareInitialTracking(frame,img)


    def prepareInitialTracking(self, frame, cut_image):
        self.H1 = np.zeros_like(self.G)
        self.H2 = np.zeros_like(self.G)
        cut_image= cv2.GaussianBlur(cut_image,(3,3),3)

        for _i in range(self.num_of_traning_imgs):
            random_rotation = randomRotation(cut_image)
            H1, H2 = self.computeNumAndDen(random_rotation)
            self.H1 += H1
            self.H2 += H2


        self.updateFilter()
        self.updateTracking(frame)
    def updateTracking(self, frame):
        (x, y), (w, h) = self.center, self.size
        self.last_img = img = cv2.getRectSubPix(frame, (w, h), (x, y))
        img= cv2.GaussianBlur(img,(3,3),3)

        img = self.preprocess(img)
        self.psr, self.last_resp, (dx, dy) = self.correlateNewImg(img)
        self.good = self.psr > self.psrGoodness
        if not self.good:
            return
            # self.prepareInitialTracking(frame,self.last_img)
            # return

        else:
            # self.learning_rate = max(min(abs(100-self.good)/100)  -0.8 , 0.125)


            #this is the new center
            self.center = x + dx, y + dy
            #cut same width and height for the new img
            self.last_img = img = cv2.getRectSubPix(frame, (w, h), self.center)
            #calcultate num and denumentator for the new image
            H1,H2 = self.computeNumAndDen(img)
            #update the num and den with learning rate to decay old one
            self.H1 = self.H1 * (1.0-self.learning_rate) + H1 * self.learning_rate
            self.H2 = self.H2 * (1.0-self.learning_rate) + H2 * self.learning_rate
            #update the kernal
            self.updateFilter()

    @property
    def state_vis(self):
        f = cv2.idft(self.H, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
        h, w = f.shape
        f = np.roll(f, -h//2, 0)
        f = np.roll(f, -w//2, 1)
        kernel = np.uint8( (f-f.min()) / f.ptp()*255 )
        resp = self.last_resp
        resp = np.uint8(np.clip(resp/resp.max(), 0, 1)*255)
        vis = np.hstack([self.last_img, kernel, resp])
        return vis





    def preprocess(self, img):
        #to get good results with low contrast imgs
        img = np.log(np.float32(img)+1.0)
        mean = img.mean()
        std_deviation = img.std()
        img = (img-mean) / (std_deviation+eps)

        #to gradually reduces the pixel values near the edge to zero
        #and focus more on the center
        preprocessed_img = img*self.win
        return preprocessed_img

    def correlateNewImg(self, img):
        F = cv2.dft(img, flags=cv2.DFT_COMPLEX_OUTPUT)
        C = cv2.mulSpectrums(F, self.H, 0, conjB=True)
        response = cv2.idft(C, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
        h, w = response.shape
        _, max_peak_value, _, max_peak_location = cv2.minMaxLoc(response)
        mx,my = max_peak_location

        #calculate dx and dy
        dx = mx - int(w/2)
        dy = my - int(h / 2)

        side_resp = response.copy()
        # side_resp = cv2.rectangle(side_resp, (mx - 5, my - 5), (mx + 5, my + 5), 0, -1)
        mean = side_resp.mean()
        standard_deviation =side_resp.std()
        psr = (max_peak_value-mean) / (standard_deviation+eps)


        return psr,response, (dx,dy)

    def updateFilter(self):
        self.H = HFilter(self.H1, self.H2)
        self.H[...,1] *= -1

    def computeNumAndDen(self,img):
        f = self.preprocess(img)
        F = cv2.dft(f, flags=cv2.DFT_COMPLEX_OUTPUT)
        H1 = cv2.mulSpectrums(self.G, F, 0, conjB=True)
        H2 = cv2.mulSpectrums(F, F, 0, conjB=True)
        return H1,H2
    def getCutFramePosition(self):
        x = self.center[0]
        y = self.center[1]
        xmin = int(x - 0.5*(self.width-1))
        ymin = int(y - 0.5*(self.height-1))
        xmax = int(self.width+xmin)
        ymax = int(self.height+ymin)
        cut_size = [xmin,ymin,xmax,ymax]
        return cut_size

    def getSizeOfTracker(self):
        return self.width,self.height

    def getCenterOfTracker(self):
        return self.center
    def getLearningRate(self):
        return self.learning_rate
    def getPsr(self):
        return self.psr
    def isGood(self):
        return self.good

