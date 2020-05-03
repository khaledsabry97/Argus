import cv2

from VIF.vif import VIF

vif = VIF()


def intersectionOverUnion(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = abs((boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou




def predict(frames_RGB,trackers):
    gray_frames = []
    for frame in frames_RGB:
        gray_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    print(len(frames_RGB))
    no_crash = 0
    crash = 0

    for tracker in trackers:
        tracker_frames,width,height,xmin,xmax,ymin,ymax = tracker.getFramesOfTracking(gray_frames)

        if tracker_frames == None:
            continue

        # if xmax - xmin < 100:
        #     continue

        if xmax - xmin < 50:
             continue
        if ymax - ymin <= 35:
            continue

        if (ymax- ymin) / (xmax - xmin) <0.35:
            continue

        feature_vec = vif.process(tracker_frames)
        result = vif.clf.predict(feature_vec.reshape(1, 304))
        if result[0] == 0.0:
            no_crash += 1
        else:
            crash += 1
            # trackers[0].saveTracking(frames_RGB)
            # trackers[1].saveTracking(frames_RGB)
            tracker.saveTracking(frames_RGB)
            print(crash, no_crash)

def checkDistance(frames,tracker_A,tracker_B,frame_no):
    if not tracker_A.isAboveSpeedLimit(frame_no-10,frame_no) and not tracker_B.isAboveSpeedLimit(frame_no-10,frame_no) :
        return False

    xa, ya = tracker_A.estimationFutureCenter[frame_no]
    xb, yb = tracker_B.estimationFutureCenter[frame_no]
    r = pow(pow(xa - xb, 2) + pow(ya - yb, 2), 0.5)
    tracker_A_area = 0.5 * tracker_A.tracker.width * tracker_A.tracker.height
    tracler_B_area = 0.5 * tracker_B.tracker.width * tracker_B.tracker.height
    iou = intersectionOverUnion(tracker_A.tracker.getCutFramePosition((xa,ya)),tracker_B.tracker.getCutFramePosition((xb,yb)))
    iou2 = intersectionOverUnion(tracker_B.tracker.getCutFramePosition((xa, ya)),
                                tracker_A.tracker.getCutFramePosition(tracker_A.tracker.center))

    xa_actual,ya_actual = tracker_A.tracker.centers[frame_no]
    xb_actual,yb_actual = tracker_B.tracker.centers[frame_no]
    difference_trackerA_actual_to_estimate = pow(pow(xa_actual - xa, 2) + pow(ya_actual - ya, 2), 0.5)
    difference_trackerB_actual_to_estimate = pow(pow(xb_actual - xb, 2) + pow(yb_actual - yb, 2), 0.5)
    max_difference = max(difference_trackerA_actual_to_estimate,difference_trackerB_actual_to_estimate)
    #print(r,difference_trackerA_actual_to_estimate,difference_trackerB_actual_to_estimate,max_difference/r)
    if r == 0:
        return True

    if r < 40 and max_difference/r > 0.5:
        print(r,difference_trackerA_actual_to_estimate,difference_trackerB_actual_to_estimate,max_difference/r)
        return True
    return False



def process(trackers,frames):
    # predict(frames, trackers)

    new_trackers = trackers
    # for tracker in trackers:
    #     if tracker.isAboveSpeedLimit():
    #         new_trackers.append(tracker)
    for i in range(len(new_trackers)):
        for j in range(i+1,len(trackers)):
            if i == j:
                continue
            tracker_A = trackers[i]
            tracker_B = trackers[j]

            if checkDistance(frames,tracker_A,tracker_B,16)or checkDistance(frames,tracker_A,tracker_B,19)or checkDistance(frames,tracker_A,tracker_B,22) or checkDistance(frames,tracker_A,tracker_B,25) or checkDistance(frames,tracker_A,tracker_B,28):
                # tracker_A.saveTracking(frames)
                #print("accident has occured!")
                predict(frames, [tracker_B,tracker_A])


