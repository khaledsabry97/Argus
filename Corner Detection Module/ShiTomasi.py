import cv2
import numpy as np
from skimage.feature.util import _prepare_grayscale_input_2D as toFloat
from scipy import ndimage as nImg

class ShiTomasi:

    minDistance = 10
    numPeaks = 6
    thresholdAbs = 0.2
    excludeBorder = 2


    def __int__(self):
      pass

    def getCorners(self,img):
        self.xx, self.xy, self.yy = self.correlationMatrix(img) #get the derivitives of dxdx,dydy and dxdy

        corners = self.minEigenValue(self.xx,self.yy,self.xy) #calc minimum eigenvalue

        coordinates = self.peakLocalMax(corners) #get the coordinates
        return coordinates

    # return minimum eigenvalue of A
    def minEigenValue(self,xx,yy,xy):
        return ((xx + yy) - np.sqrt((xx - yy) ** 2 + 4 * xy ** 2)) / 2


    def correlationMatrix(self,image):
        image = toFloat(image)

        # self.yy = nImg.sobel(image, axis=0, mode='constant', cval=0)
        # self.xx = nImg.sobel(image, axis=1, mode='constant', cval=0)
        self.xx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        self.yy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

        kernel = np.ones((9, 9), np.float32) / 81
        self.Dxx = cv2.filter2D(self.xx * self.xx, -1, kernel)
        self.Dxy = cv2.filter2D(self.xx * self.yy, -1, kernel)
        self.Dyy = cv2.filter2D(self.yy * self.yy, -1, kernel)

        # self.Dxx = cv2.GaussianBlur(self.xx * self.xx,(9,9),0)
        # self.Dxy = cv2.GaussianBlur(self.xx * self.yy,(9,9),0)
        # self.Dyy = cv2.GaussianBlur(self.yy * self.yy,(9,9),0)

        # self.Dxx = nImg.gaussian_filter(self.xx * self.xx, 1, mode='constant', cval=0)
        # self.Dxy = nImg.gaussian_filter(self.xx * self.yy, 1, mode='constant', cval=0)
        # self.Dyy = nImg.gaussian_filter(self.yy * self.yy, 1, mode='constant', cval=0)

        return self.Dxx, self.Dxy, self.Dyy


    #Find peaks in img
    #minDistance is the distance between one pixel and another making it the local maxima
    #return coordinates of the peaks
    def peakLocalMax(self,image):
        out = np.zeros_like(image, dtype=np.bool)

        # Non maximum filter
        size = 2 * self.minDistance + 1
        image_max = nImg.maximum_filter(image, size=size, mode='constant')
        mask = image == image_max

        if self.excludeBorder:
            # zero out the image borders
            for i in range(mask.ndim):
                mask = mask.swapaxes(0, i)
                remove =  2 * self.excludeBorder
                mask[:remove // 2] = mask[-remove // 2:] = False
                mask = mask.swapaxes(0, i)

        # find top peak candidates above a threshold
        mask &= image > self.thresholdAbs

        # Select highest intensities (num_peaks)

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

