import cv2
import numpy as np
from skimage.feature.util import _prepare_grayscale_input_2D as toFloat
from scipy import ndimage as nImg

class ShiTomasi:

    minDistance = 10
    numPeaks = 6
    thresholdAbs = 0.10
    excludeBorder = 2


    def __int__(self):
      pass

    def getCorners(self,img):
        self.xx, self.xy, self.yy = self.correlationMatrix(img) #get the derivitives of dxdx,dydy and dxdy

        corners = self.minEigenValue(self.xx,self.yy,self.xy) #calc minimum eigenvalue

        coordinates = self.peakLocalMax(corners) #get the coordinates
        return coordinates

    def correlationMatrix(self,image):
        image = toFloat(image)
        # self.yy = nImg.sobel(image, axis=0, mode='constant', cval=0)
        # self.xx = nImg.sobel(image, axis=1, mode='constant', cval=0)
        self.xx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        self.yy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)


        x2x = self.xx * self.xx
        y2y = self.yy * self.yy
        x2y = self.xx * self.yy

        kernel = np.ones((9, 9), np.float32) / 81
        self.Dxx = cv2.filter2D(x2x, -1, kernel)
        self.Dxy = cv2.filter2D(x2y, -1, kernel)
        self.Dyy = cv2.filter2D(y2y, -1, kernel)

        # self.Dxx = cv2.GaussianBlur(x2x,(9,9),0)
        # self.Dxy = cv2.GaussianBlur(x2y,(9,9),0)
        # self.Dyy = cv2.GaussianBlur(y2y,(9,9),0)

        # self.Dxx = nImg.gaussian_filter(x2x, 1, mode='constant', cval=0)
        # self.Dxy = nImg.gaussian_filter(x2y, 1, mode='constant', cval=0)
        # self.Dyy = nImg.gaussian_filter(y2y, 1, mode='constant', cval=0)

        return self.Dxx, self.Dxy, self.Dyy


    # return minimum eigenvalue of A
    def minEigenValue(self,xx,yy,xy):
        return ((xx + yy) - np.sqrt((xx - yy) ** 2 + 4 * xy ** 2)) / 2

    #Find peaks in img
    #minDistance is the distance between one pixel and another making it the local maxima
    #return coordinates of the peaks
    def peakLocalMax(self,image):

        # Non maximum filter
        size = 2 * self.minDistance + 1
        image_max = nImg.maximum_filter(image, size=size, mode='constant')
        mask = image == image_max

        # zero out the image borders
        for i in range(mask.ndim):
            mask = mask.swapaxes(0, i)
            remove =  self.excludeBorder
            mask[:remove] = 0
            mask[-remove:] = 0
            mask = mask.swapaxes(0, i)

        # find top peak candidates above a threshold
        aboveThresholdCorners = image > self.thresholdAbs
        mask &= aboveThresholdCorners

        # get coordinates of peaks
        coordinates = np.nonzero(mask)
        # select num_peaks peaks
        if len(coordinates[0]) > self.numPeaks:
            intensities = image[coordinates]
            idx_maxsort = np.argsort(intensities)
            coTp = np.transpose(coordinates)
            coordinates = coTp[idx_maxsort][-self.numPeaks:]
        else:
            coordinates = np.column_stack(coordinates)
        # Highest peak first
        coordinates =  coordinates[::-1]

        return coordinates


    def getFeatures(self,img,xmin=0,ymin=0,opencv=False):
        if opencv:
            return self.getFeaturesOpencv(img,xmin,ymin)
        else:
            return self.getFeaturesMine(img,xmin,ymin)

    def getFeaturesMine(self,img,xmin =0,ymin =0):

        corners = self.getCorners(img)
        corners[:,1] += xmin
        corners[:,0] += ymin

        return corners[:,1],corners[:,0]

    def getFeaturesOpencv(self,img,xmin = 0,ymin = 0):
        maxCorners = 6
        qualityLevel = 0.17
        minDistance = 10
        blockSize = 10

        corners = cv2.goodFeaturesToTrack(img, mask=None, maxCorners=maxCorners,
                              qualityLevel=qualityLevel,
                              minDistance=minDistance,
                              blockSize=blockSize)
        corners = np.int0(corners)

        x,y = [],[]
        ind = []
        for i in corners:
            xx, yy = i.ravel()
            yy +=ymin
            xx +=xmin
            x.append(xx)
            y.append(yy)
            # ind.append((xx,yy))
        return x,y
        # return ind