import cv2
import numpy as np
from Corner_Detection_Module.CornerDetection import ShiTomasi
class GetFeatures:

    def __init__(self):
        self.shitomasi = ShiTomasi()


    def getCorners(self,img,Opencv=False):
        if Opencv:
            feature_params = dict(maxCorners=6,
                                  qualityLevel=0.17,
                                  minDistance=10,
                                  blockSize=10)

            # using opencv function to get feature for which we are plotting flow
            return cv2.goodFeaturesToTrack(img, mask=None, **feature_params)
            # return self.shitomasi.getFeatures(img,opencv=True)

        else:
            corners = self.shitomasi.getCorners(img)
            tupledCorners = []
            for x in corners:
                xx,yy = x[0],x[1]
                tupledCorners.append((yy,xx))
            return tupledCorners

    def getFeatures(self, img, bbox, opencv= False):
        n_object = np.shape(bbox)
        bbox = bbox.astype(int)
        img = img[bbox[0][1]:bbox[3][1], bbox[0][0]:bbox[3][0]]


        features = self.getCorners(img,opencv)
        feature = np.int32(features)
        feature = np.reshape(feature, newshape=[-1, 2])
        feature[:, 0] = feature[:, 0] + bbox[0][0]
        feature[:, 1] = feature[:, 1] + bbox[0][1]


        return feature


    def run(self, img, bbox,opencv = False):
        n_object = np.shape(bbox)[0]
        N = 0
        temp = np.empty((n_object,), dtype=np.ndarray)  # temporary storage of x,y coordinates
        for i in range(n_object):
            coordinates = self.getFeatures(img, bbox[i],opencv)
            # temp[i] = self.getFeatures(img, bbox[i])
            temp[i] = coordinates

            if coordinates.shape[0] > N:
                N = coordinates.shape[0]

        x = np.full((N, n_object), -1)
        y = np.full((N, n_object), -1)
        for i in range(n_object):
            n_feature = temp[i].shape[0]
            x[0:n_feature, i] = temp[i][:, 1]
            y[0:n_feature, i] = temp[i][:, 0]

        return y, x
