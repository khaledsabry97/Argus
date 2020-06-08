import threading
from threading import Thread
from time import sleep, time

import cv2
import math
import numpy as np

from CrashingEstimation import process
from Mosse_Tracker.TrackerManager import Tracker
from PIL import Image
#from Car_Detection_TF.yolo import YOLO
#from Car_Detection.detect import Yolo_image
from Mosse_Tracker.utils import draw_str
from yoloFiles import loadFile
import pickle
from VIF.vif import VIF

pi=22/7
# clf = pickle.load(open('VIF/model-svm1.sav', 'rb'))
total_frames = []
counter_sub_video = 1
data = []



class MainFlow:
    def __init__(self, yolo, fromFile=True, select=False):
        self.yolo = yolo
        self.frameCount = 0
        self.readFile = fromFile
        # if select == False then use TF else use PYTORCH
        self.selectYOLO = select
        self.trackerId = 0

    def run(self, path):
        global total_frames
        last_30_frames = []
        last_delayed_30_frames = []
        fileBoxes = []
        new_frame = None
        if self.readFile:
            fileBoxes = loadFile(path)
		
		# model = ''
        # if self.selectYOLO:
        #     model = Darknet("Car_Detection/config/yolov3.cfg", CUDA=False)
        #     model.load_weight("Car_Detection/config/yolov3.weights")
			
        cap = cv2.VideoCapture(path)
        #frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        #frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = 480
        frame_height = 360
        trackers = []
        delayed_trackers = []

        # run yolo every fps frames
        fps = 30
        hfps = 15
        no_of_frames = 0
        paused = False
        cum_time = 0
        while True:
            if not paused:
                t = time()
                # read new frame
                ret, frame = cap.read()
                # if ret and no_of_frames <120:
                #     no_of_frames+=1
                #     continue
                if ret:
                    dim = (480, 360)
                    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    #frame = cv2.GaussianBlur(frame, (-1, -1), 1.0)  # 2.0
                    new_frame = frame.copy()
                    total_frames.append(new_frame)
                # failed to get new frame
                else:
                    break

                # run ViF
                if self.frameCount > 0 and (self.frameCount % fps == 0 or self.frameCount == fps - 1):
                     #print("FRAME " + str(self.frameCount) + " VIF")
                     #thread = Thread(target=predict(last_30_frames,trackers))
                     #thread.start()
                     #print("error")
                     #vif(trackers, frame_width, frame_height, frame)
                     t = time()
                     # thread = Thread(target=process(trackers,last_30_frames))
                     # thread.start()

                     process(trackers,last_30_frames)
                     print(time() - t)

                if self.frameCount > 16 and self.frameCount % hfps == 0 and self.frameCount % fps != 0:
                     # print("FRAME " + str(self.frameCount) + " VIF")
                     # thread = Thread(target=predict(last_30_frames,trackers))
                     # thread.start()
                     # print("error")
                     # vif(trackers, frame_width, frame_height, frame)
                     t = time()
                     # thread = Thread(target=process(delayed_trackers, last_delayed_30_frames))
                     # thread.start()
                     #
                     process(delayed_trackers, last_delayed_30_frames)
                     print(time() - t)

                if self.frameCount > 0 and self.frameCount % hfps == 0 and self.frameCount % fps != 0:
                    # print("YOLO CALLED in frame no. " + str(self.frameCount))
                    # clear earlier trackers
                    delayed_trackers = []
                    bboxes = []
                    last_delayed_30_frames = []
                    img = Image.fromarray(frame)

                    # detect vehicles
                    if self.readFile:
                        # From files
                        bboxes = fileBoxes[self.frameCount]

                    elif not self.selectYOLO:
                        # Khaled
                        img, bboxes = self.yolo.detect_image(img)
                    else:
                        # Roba
                        bboxes = Yolo_image(np.float32(img), model)

                    for i, bbox in enumerate(bboxes):
                        label = bbox[0]
                        # accuracy = bbox[5]

                        xmin = int(bbox[1])
                        xmax = int(bbox[2])
                        ymin = int(bbox[3])
                        ymax = int(bbox[4])

                        # can limit this part to cars and trucks only later
                        # cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255))
                        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.trackerId += 1
                        # no need for frame_width and frame_height
                        if xmax < frame_width and ymax < frame_height:
                            tr = Tracker(frame_gray, (xmin, ymin, xmax, ymax), frame_width, frame_height,
                                         self.trackerId)
                            delayed_trackers.append(tr)
                        elif xmax < frame_width and ymax >= frame_height:
                            tr = Tracker(frame_gray, (xmin, ymin, xmax, frame_height - 1), frame_width, frame_height,
                                         self.trackerId)
                            delayed_trackers.append(tr)
                        elif xmax >= frame_width and ymax < frame_height:
                            tr = Tracker(frame_gray, (xmin, ymin, frame_width - 1, ymax), frame_width, frame_height,
                                         self.trackerId)
                            delayed_trackers.append(tr)
                        else:
                            tr = Tracker(frame_gray, (xmin, ymin, frame_width - 1, frame_height - 1), frame_width,
                                         frame_height, self.trackerId)
                            delayed_trackers.append(tr)
                else:
                    #print("updating trackers, frame no. " + str(self.frameCount) + "...")
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    #print(len(trackers))
                    # updating trackers
                    for i, tracker in enumerate(delayed_trackers):
                        left, top, right, bottom = tracker.update(frame_gray)
                        # radian = tracker.getCarAngle() * (pi / 180)
                        # radian = 0
                        #
                        # #left = left * math.cos(radian) - top * math.sin(radian)
                        # #right = right * math.cos(radian) - bottom * math.sin(radian)
                        # #top = left * math.sin(radian) + top * math.cos(radian)
                        # #bottom = right * math.sin(radian) + bottom * math.cos(radian)
                        #
                        left_future, top_future, right_future, bottom_future = tracker.futureFramePosition()
                        #
                        # if left > 0 and top > 0 and right < frame_width and bottom < frame_height:
                        #     if tracker.isAboveSpeedLimit():
                        #         cv2.rectangle(frame, (int(left), int(top)),(int(right), int(bottom)), (0, 0, 255)) #B G R
                        #     else:
                        #         cv2.rectangle(frame, (int(left), int(top)),(int(right), int(bottom)), (255, 0, 0))
                        #
                        #
                        #
                        #
                        #     #draw_str(frame, (left, bottom + 64), 'Max Speed: %.2f' % tracker.getMaxSpeed())
                        #     #draw_str(frame, (left, bottom + 16), 'Avg Speed: %.2f' % tracker.getAvgSpeed())
                        #     #draw_str(frame, (left, bottom + 96), 'Cur Speed: %.2f' % tracker.getCurrentSpeed())
                        #     #draw_str(frame, (left, bottom + 112), 'Area Size: %.2f' % tracker.getCarSizeCoefficient())
                        #     #draw_str(frame, (left, bottom + 32), 'Moving Angle: %.2f' % tracker.getCarAngle())
                        #
                        # if left_future > 0 and top_future > 0 and right_future < frame_width and bottom_future < frame_height:
                        #     cv2.rectangle(frame, (int(left_future), int(top_future)), (int(right_future), int(bottom_future)), (0, 255, 0))

                # Call YOLO
                if self.frameCount % fps == 0 or self.frameCount == 0:
                    #print("YOLO CALLED in frame no. " + str(self.frameCount))
                    # clear earlier trackers
                    trackers = []
                    bboxes = []
                    last_30_frames = []
                    img = Image.fromarray(frame)

                    # detect vehicles
                    if self.readFile:
                        # From files
                        bboxes = fileBoxes[self.frameCount]

                    elif not self.selectYOLO:
                        # Khaled
                        img, bboxes = self.yolo.detect_image(img)
                    else:
                        # Roba
                        bboxes = Yolo_image(np.float32(img), model)


                    for i, bbox in enumerate(bboxes):
                        label = bbox[0]
                        # accuracy = bbox[5]

                        xmin = int(bbox[1])
                        xmax = int(bbox[2])
                        ymin = int(bbox[3])
                        ymax = int(bbox[4])

                        # can limit this part to cars and trucks only later
                        # cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255))
                        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.trackerId +=1
                        # no need for frame_width and frame_height
                        if xmax < frame_width and ymax < frame_height:
                            tr = Tracker(frame_gray, (xmin, ymin, xmax, ymax), frame_width, frame_height,self.trackerId)
                            trackers.append(tr)
                        elif xmax < frame_width and ymax >= frame_height:
                            tr = Tracker(frame_gray, (xmin, ymin, xmax, frame_height - 1), frame_width, frame_height,self.trackerId)
                            trackers.append(tr)
                        elif xmax >= frame_width and ymax < frame_height:
                            tr = Tracker(frame_gray, (xmin, ymin, frame_width - 1, ymax), frame_width, frame_height,self.trackerId)
                            trackers.append(tr)
                        else:
                            tr = Tracker(frame_gray, (xmin, ymin, frame_width - 1, frame_height - 1), frame_width, frame_height,self.trackerId)
                            trackers.append(tr)
                else:
                    #print("updating trackers, frame no. " + str(self.frameCount) + "...")
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    #print(len(trackers))
                    # updating trackers
                    for i, tracker in enumerate(trackers):
                        left, top, right, bottom = tracker.update(frame_gray)
                        radian = tracker.getCarAngle() * (pi / 180)
                        radian = 0

                        #left = left * math.cos(radian) - top * math.sin(radian)
                        #right = right * math.cos(radian) - bottom * math.sin(radian)
                        #top = left * math.sin(radian) + top * math.cos(radian)
                        #bottom = right * math.sin(radian) + bottom * math.cos(radian)

                        left_future, top_future, right_future, bottom_future = tracker.futureFramePosition()

                        if left > 0 and top > 0 and right < frame_width and bottom < frame_height:
                            if tracker.isAboveSpeedLimit():
                                cv2.rectangle(frame, (int(left), int(top)),(int(right), int(bottom)), (0, 0, 255)) #B G R
                            else:
                                cv2.rectangle(frame, (int(left), int(top)),(int(right), int(bottom)), (255, 0, 0))




                            #draw_str(frame, (left, bottom + 64), 'Max Speed: %.2f' % tracker.getMaxSpeed())
                            draw_str(frame, (left, bottom + 16), 'Avg Speed: %.2f' % tracker.getAvgSpeed())
                            #draw_str(frame, (left, bottom + 96), 'Cur Speed: %.2f' % tracker.getCurrentSpeed())
                            #draw_str(frame, (left, bottom + 112), 'Area Size: %.2f' % tracker.getCarSizeCoefficient())
                            #draw_str(frame, (left, bottom + 32), 'Moving Angle: %.2f' % tracker.getCarAngle())

                        if left_future > 0 and top_future > 0 and right_future < frame_width and bottom_future < frame_height:
                            cv2.rectangle(frame, (int(left_future), int(top_future)), (int(right_future), int(bottom_future)), (0, 255, 0))
                # sleep(0.02)
                #cv2.namedWindow("result", cv2.WINDOW_NORMAL)
                cum_time += time() - t
                cv2.imshow("result", frame)
                last_30_frames.append(new_frame)
                last_delayed_30_frames.append(new_frame)
                if self.frameCount %fps == 0:
                    print(self.frameCount/cum_time)
                # increment number of frames
                self.frameCount += 1
            ch = cv2.waitKey(10)
            if ch == ord(' '):
                paused = not paused
        print(self.trackerId)




if __name__ == '__main__':


    # m = MainFlow(None, select=False)
    # m.run('videos/1500.mp4')
    m = MainFlow(None, select=False)
    m.run('videos/1508.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1516.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1521.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1528.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1529.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1533.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1534.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/Easy.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1559.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1563.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1566.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1537.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1506.mp4')

    # m = MainFlow(None, select=False) #but have issue in the yolo file
    # m.run('videos/1513.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1518.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1544.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1543.mp4')





    # m = MainFlow(None, select=False)
    # m.run('videos/1503.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1517.mp4')
    #
    # m = MainFlow(None, select=False)
    # m.run('videos/1541.mp4')


    # m = MainFlow(None, select=False)
    # m.run('videos/1561.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1562.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1564.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/1565.mp4')
    # m = MainFlow(None, select=False)
    # m.run('videos/normal1.mp4')

    # for i in range(1543,1545):
    #     print("F")
    #     m = MainFlow(None, select=False)
    #     m.run('videos/'+str(i)+'.mp4')






