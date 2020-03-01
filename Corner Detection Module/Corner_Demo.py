
from time import time

import cv2
import numpy as np

from corner.ShiTomasi import ShiTomasi


def getFeaturesMine(img,xmin,ymin):

    shiTomasi = ShiTomasi()
    corners = shiTomasi.getCorners(img)
    corners[:,1] += xmin
    corners[:,0] += ymin

    return corners[:,1],corners[:,0]

def getFeaturesOpencv(img,xmin,ymin):
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
    for i in corners:
        xx, yy = i.ravel()
        yy +=ymin
        xx +=xmin
        x.append(xx)
        y.append(yy)
    return x,y

def show(image,x,y,windowName):
    for i in range(len(x)):
        xx, yy = x[i],y[i]
        cv2.circle(image, (xx, yy), 3, (0,0,255), -1)
    cv2.imshow(windowName, image)


if __name__ == "__main__":
    cap = cv2.VideoCapture("2.mkv")
    i =0
    while(i < 330):
        ret, frame = cap.read()  # get first frame
        i+=1

    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    bbox = cv2.selectROI("select window",frame_gray)
    cv2.destroyAllWindows()
    xmin,ymin = bbox[0],bbox[1]
    img = frame_gray[bbox[1]:bbox[1]+bbox[3] , bbox[0]:bbox[0] + bbox[2]]

    tMine = time()
    x,y = getFeaturesMine(img,xmin,ymin)
    tMine = time() -tMine
    show(frame.copy(),x,y,"Mine")

    tOpencv = time()
    x,y = getFeaturesOpencv(img,xmin,ymin)
    tOpencv = time() - tOpencv
    show(frame.copy(),x,y,"Opencv")


    print("Mine: "+str(tMine))
    print("Opencv: "+str(tOpencv))
    print("Opencv/Mine: "+str(tOpencv/tMine))
    print("Percentage of Speedup: " + str(((tMine - tOpencv) / tMine)*100)+" %")


    cv2.waitKey(0)
    cv2.destroyAllWindows()

