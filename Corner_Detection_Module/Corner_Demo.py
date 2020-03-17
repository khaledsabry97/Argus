from time import time
import cv2
from Corner_Detection_Module.CornerDetection import ShiTomasi



def show(image,x,y,windowName):
    for i in range(len(x)):
        xx, yy = x[i],y[i]
        cv2.circle(image, (xx, yy), 3, (0,0,255), -1)
    cv2.imshow(windowName, image)


if __name__ == "__main__":
    cap = cv2.VideoCapture("Easy.mp4")
    i =0
    while(i < 1):
        ret, frame = cap.read()  # get first frame
        i+=1

    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    bbox = cv2.selectROI("select window",frame_gray)
    cv2.destroyAllWindows()
    xmin,ymin = bbox[0],bbox[1]
    img = frame_gray[bbox[1]:bbox[1]+bbox[3] , bbox[0]:bbox[0] + bbox[2]]

    shiTomasi = ShiTomasi()

    tMine = time()
    x,y = shiTomasi.getFeatures(img,xmin,ymin,False)
    tMine = time() -tMine
    show(frame.copy(),x,y,"Mine")

    tOpencv = time()
    x,y = shiTomasi.getFeatures(img,xmin,ymin,True)
    tOpencv = time() - tOpencv
    show(frame.copy(),x,y,"Opencv")


    print("Mine: "+str(tMine))
    print("Opencv: "+str(tOpencv))
    print("Opencv/Mine: "+str(tOpencv/tMine))
    print("Percentage of Speedup: " + str(((tMine - tOpencv) / tMine)*100)+" %")


    cv2.waitKey(0)
    cv2.destroyAllWindows()

