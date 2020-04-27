# this uses yolo3, the weights of the COCO trained network must have been downloaded before

import darknet as yolo
import numpy as np
import cv2
import random
from vif import ViF
import pickle
from tracker import Tracker

clf = pickle.load(open('models/model-svm.sav', 'rb'))
total_frames = []
sub_sampling = 29
# path
net = yolo.load_net("/home/vicente/projects/object-detection/yolo/yolo3/darknet/cfg/yolov3.cfg",
              "/home/vicente/projects/object-detection/yolo/yolo3/darknet/cfg/yolov3.weights", 0)
meta = yolo.load_meta("/home/vicente/projects/object-detection/yolo/yolo3/darknet/data/coco.data")
counter_sub_video = 1
data = []


#process ViF for each tracker
def vif(trackers,  frame_width, frame_height, frame):
    global sub_sampling
    print ("processing ViF on each tracker")
    global counter_sub_video
    for i, tracker in enumerate(trackers):
        print("processing ViF on tracker " + str(tracker.name), tracker.get_position().right() - tracker.get_position().left(), tracker.get_position().bottom() - tracker.get_position().top())

        box = tracker.get_box_from_history(frame_width, frame_height)
        #for each tracker, we extract the subframes

        if box[2] - box[0] < 100:
            print("dimensions of the tracker are so small, is ignored")
            continue



        print("tracker frame_index:", tracker.frame_index, "len history:", len(tracker.history))
        if len(tracker.history) < sub_sampling:
            print("tracker with few frames in there history, is ignored")
        else:
            print("the video will be saved", str(counter_sub_video), (box[2] - box[0], box[3] - box[1]))

            counter_sub_video += 1
            tracker_frames = []


            for j in range(tracker.frame_index, tracker.frame_index + len(tracker.history)):

                img = total_frames[j]
                sub_image = img[box[1]:box[3], box[0]:box[2]]
                gray_image = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
                tracker_frames.append(gray_image)

                cv2.imshow("sub_image", sub_image)
                cv2.waitKey(0)


            print ("the tracker has " + str(len(tracker_frames)) + " frames")
            # procesing vif
            obj = ViF()
            feature_vec = obj.process(tracker_frames)
            data.append(feature_vec)

            # to evaluate vif on an already trained model
            ###################################################################
            ###################################################################

            feature_vec = feature_vec.reshape(1, 304)
            print(feature_vec.shape)
            result = clf.predict(feature_vec)
            print("SVM RESULT", result)
            font = cv2.FONT_HERSHEY_SIMPLEX
            print("RESULT ", result[0])
            if result[0] == 0.0:
                print(0)
                title = "normal"
            else:
                print(1)
                title = "car-crash"
                overlay = frame.copy()
                cv2.rectangle(overlay, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), -1)
                opacity = 0.4
                cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

            cv2.imshow("win", frame)
            cv2.waitKey(0)

            ###################################################################
            ###################################################################


def start_process(path, net, meta):
    global total_frames
    print("reading video " + path)
    total_frames = []

    cap = cv2.VideoCapture(path)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(str(frame_count) + " frames y " + str(fps) + " as frame rate")

    index = 0

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detections = 0
    trackers = []


    while True:
        ret, frame = cap.read()

        if ret:
            new_frame = frame.copy()
            total_frames.append(new_frame)

            # run ViF
            if index > 0 and (index % sub_sampling == 0 or index == frame_count - 1):
                print("FRAME " + str(index) + " VIF")
                vif(trackers, frame_width, frame_height, frame)

            # run yolo
            if index % sub_sampling == 0 or index == 0 :
                print ("FRAME " + str(index) + " YOLO")
                trackers = []

                cv2.imwrite("tmp/img.jpg", frame)
                # path
                detections = yolo.detect(net, meta, "/home/vicente/projects/violence/car-crash/tmp/img.jpg")
                print(detections)
                for det in detections:
                    label = det[0]
                    accuracy = det[1]
                    box = det[2]

                    width = int(box[2])
                    height = int(box[3])
                    xmin = int(box[0]) - width / 2
                    ymin = int(box[1]) - height / 2

                    if label == 'car':
                        cv2.rectangle(frame, (xmin, ymin), (xmin + width, ymin + height), (0, 0, 255))

                        # we only add the tracker if it is within the frame limits, no we don't do this
                        # the tracker does not work well

                        if xmin + width < frame_width and ymin + height < frame_height:
                            tr = Tracker(frame, (xmin, ymin, xmin + width, ymin + height), random.randrange(100), index)
                            trackers.append(tr)
                        else:
                            if xmin + width < frame_width and ymin + height >= frame_height:
                                tr = Tracker(frame, (xmin, ymin, xmin + width, frame_height - 1), random.randrange(100),
                                             index)
                            elif xmin + width >= frame_width and ymin + height < frame_height:
                                tr = Tracker(frame, (xmin, ymin, frame_width - 1, ymin + height), random.randrange(100),
                                             index)
                            else:
                                tr = Tracker(frame, (xmin, ymin, frame_width - 1, frame_height - 1),
                                             random.randrange(100), index)
                            trackers.append(tr)

            else:
                print("FRAME " + str(index) + " UPDATE TRACKER")
                # out.write(frame)
                # we process the optical flow with Lucas-Kanade


                # update trackers
                for i, tracker in enumerate(trackers):
                    tr_pos = tracker.update(frame)
                    if tr_pos.left() > 0 and tr_pos.top() > 0 and tr_pos.right() < frame_width and tr_pos.bottom() < frame_height:
                        cv2.rectangle(frame, (int(tr_pos.left()), int(tr_pos.top())),
                                      (int(tr_pos.right()), int(tr_pos.bottom())), (0, 0, 255))
                        tracker.add_history(tr_pos)

                        # apparently does not work well, there are usually intersections between the vectors of the same car,
                        #  also need to correct which are the trackers that intersect
                        # check_intersection(lines, frame, trackers)

            cv2.imshow("win", frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

            index += 1

        else:
            break

    cv2.destroyAllWindows()


# we look for if there are intersecting optical flow vectors, brute force
def check_intersection(lines, frame, trackers):
    print("assigning vector for each tracker")
    print("in total " + str(len(lines)) + " vectors and" + str(len(trackers)) + " trackers")
    print("vectors", lines)
    # we assign the flow vectors to each tracker according to their position
    for tr in trackers:
        tr.clean_flow_vector()
        i = 0
        while True:
            if i >= len(lines):
                break
            if tr.is_inside(lines[i]):
                tr.add_vector(lines[i])
                lines.pop(i)
            i = i + 1

        print(str(len(tr.flow_vectors)) + " assigned to the tracker")
        print(tr.flow_vectors)

    # we look for tracker that are intercepted
    for i in range(len(trackers)):
        for j in range(len(trackers)):
            if i != j:
                tr_a = trackers[i].get_position()
                tr_b = trackers[j].get_position()

                if tr_a.left() > tr_b.right() or tr_b.left() > tr_a.right():
                    print("no overlapping")
                elif tr_a.top() < tr_b.bottom() or tr_b.top() > tr_a.bottom():
                    print("no overlapping")
                else:
                    if trackers[i].intersect_with(trackers[j], frame):
                        print("POSSIBLE CAR CRASH")



start_process("choque10.mp4", net, meta)
