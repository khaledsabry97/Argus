import cv2
import numpy as np
from Mosse_Tracker.TrackerManager import Tracker
from PIL import Image
from Car_Detection_TF.yolo import YOLO
from Car_Detection.detect import Yolo_image
from yoloFiles import loadFile
import pickle
from VIF.vif import VIF

# clf = pickle.load(open('models/model-svm.sav', 'rb'))
total_frames = []
counter_sub_video = 1
data = []

#process ViF for each tracker
# def vif(trackers,  frame_width, frame_height, frame):
#     global sub_sampling
#     print ("processing ViF on each tracker")
#     global counter_sub_video
#     for i, tracker in enumerate(trackers):
#         print("processing ViF on tracker " + str(tracker.name), tracker.get_position().right() - tracker.get_position().left(), tracker.get_position().bottom() - tracker.get_position().top())
#
#         box = tracker.get_box_from_history(frame_width, frame_height)
#         #for each tracker, we extract the subframes
#
#         if box[2] - box[0] < 100:
#             print("dimensions of the tracker are so small, is ignored")
#             continue
#
#
#
#         print("tracker frame_index:", tracker.frame_index, "len history:", len(tracker.history))
#         if len(tracker.history) < sub_sampling:
#             print("tracker with few frames in there history, is ignored")
#         else:
#             print("the video will be saved", str(counter_sub_video), (box[2] - box[0], box[3] - box[1]))
#
#             counter_sub_video += 1
#             tracker_frames = []
#
#
#             for j in range(tracker.frame_index, tracker.frame_index + len(tracker.history)):
#
#                 img = total_frames[j]
#                 sub_image = img[box[1]:box[3], box[0]:box[2]]
#                 gray_image = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
#                 tracker_frames.append(gray_image)
#
#                 cv2.imshow("sub_image", sub_image)
#                 cv2.waitKey(0)
#
#
#             print ("the tracker has " + str(len(tracker_frames)) + " frames")
#             # procesing vif
#             obj = VIF()
#             feature_vec = obj.process(tracker_frames)
#             data.append(feature_vec)
#
#             # to evaluate vif on an already trained model
#             feature_vec = feature_vec.reshape(1, 304)
#             print(feature_vec.shape)
#             result = clf.predict(feature_vec)
#             print("SVM RESULT", result)
#             font = cv2.FONT_HERSHEY_SIMPLEX
#             print("RESULT ", result[0])
#             if result[0] == 0.0:
#                 print(0)
#                 title = "normal"
#             else:
#                 print(1)
#                 title = "car-crash"
#                 overlay = frame.copy()
#                 cv2.rectangle(overlay, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), -1)
#                 opacity = 0.4
#                 cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
#
#             cv2.imshow("win", frame)
#             cv2.waitKey(0)


class MainFlow:
    def __init__(self, yolo, fromFile=False, select=False):
        self.yolo = yolo
        self.frameCount = 0
        self.readFile = fromFile
        # if select == False then use TF else use PYTORCH
        self.selectYOLO = select


    def run(self, path):
        global total_frames
        fileBoxes = []
        if self.readFile:
            fileBoxes = loadFile(path)

        cap = cv2.VideoCapture(path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        trackers = []

        # run yolo every fps frames
        fps = 30
        while True:
            # read new frame
            ret, frame = cap.read()
            if ret:
                new_frame = frame.copy()
                total_frames.append(new_frame)
            # failed to get new frame
            else:
                break

            # run ViF
            # if self.frameCount > 0 and (self.frameCount % fps == 0 or self.frameCount == fps - 1):
            #     print("FRAME " + str(self.frameCount) + " VIF")
            #     vif(trackers, frame_width, frame_height, frame)

            # Call YOLO
            if self.frameCount % fps == 0 or self.frameCount == 0:
                print("YOLO CALLED in frame no. " + str(self.frameCount))
                # clear earlier trackers
                trackers = []
                bboxes = []
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
                    bboxes = Yolo_image(np.float32(img))


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

                    # no need for frame_width and frame_height
                    if xmax < frame_width and ymax < frame_height:
                        tr = Tracker(frame_gray, (xmin, ymin, xmax, ymax), frame_width, frame_height)
                        trackers.append(tr)
                    elif xmax < frame_width and ymax >= frame_height:
                        tr = Tracker(frame_gray, (xmin, ymin, xmax, frame_height - 1), frame_width, frame_height)
                        trackers.append(tr)
                    elif xmax >= frame_width and ymax < frame_height:
                        tr = Tracker(frame_gray, (xmin, ymin, frame_width - 1, ymax), frame_width, frame_height)
                        trackers.append(tr)
                    else:
                        tr = Tracker(frame_gray, (xmin, ymin, frame_width - 1, frame_height - 1), frame_width, frame_height)
                        trackers.append(tr)
            else:
                print("updating trackers, frame no. " + str(self.frameCount) + "...")
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # updating trackers
                for i, tracker in enumerate(trackers):
                    left, top, right, bottom = tracker.update(frame_gray)
                    if left > 0 and top > 0 and right < frame_width and bottom < frame_height:
                        cv2.rectangle(frame, (int(left), int(top)),
                                      (int(right), int(bottom)), (0, 0, 255))
            cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            cv2.imshow("result", frame)
            ch = cv2.waitKey(10)

            # increment number of frames
            self.frameCount += 1


if __name__ == '__main__':
    m = MainFlow(YOLO(), select=False)
    m.run('videos/Easy.mp4')
