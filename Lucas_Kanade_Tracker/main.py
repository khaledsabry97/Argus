from time import time

import numpy as np
import cv2
import Estimate_trasnlation as eT
import Apply_geometric_transformation as aGT
import getFeatures as gF


def main(rawVideo, draw_bb=False, play_realtime=False, save_to_file=False, useCV=True):
    # Create instances
    estimateTrans = eT.EstimateTranslation()
    getFeatures = gF.GetFeatures()
    applyGeometricTrans = aGT.ApplyGeometricTransformation()

    # initilize
    n_frame = 400
    frames = np.empty((n_frame,), dtype=np.ndarray)
    frames_draw = np.empty((n_frame,), dtype=np.ndarray)
    bboxs = np.empty((n_frame,), dtype=np.ndarray)
    for frame_idx in range(n_frame):
        _, frames[frame_idx] = rawVideo.read()

    # draw rectangle roi for target objects, or use default objects initilization
    if draw_bb:
        n_object = int(input("Number of objects to track:"))
        bboxs[0] = np.empty((n_object, 4, 2), dtype=float)
        for i in range(n_object):
            (xmin, ymin, boxw, boxh) = cv2.selectROI("Select Object %d" % (i), frames[0])
            cv2.destroyWindow("Select Object %d" % (i))
            bboxs[0][i, :, :] = np.array(
                [[xmin, ymin], [xmin + boxw, ymin], [xmin, ymin + boxh], [xmin + boxw, ymin + boxh]]).astype(float)
    else:
        i = 0
        n_object = 1
        bboxs[0] = np.array([[[291, 187], [405, 187], [291, 267], [405, 267]]]).astype(float)

    if save_to_file:
        out = cv2.VideoWriter('Tracking_Demo.avi', 0, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0,
                              (frames[i].shape[1], frames[i].shape[0]))

    # Start from the first frame, do optical flow for every two consecutive frames.

    startXs, startYs = getFeatures.run(cv2.cvtColor(frames[0], cv2.COLOR_RGB2GRAY), bboxs[0], opencv = useCV)
    t = time()
    for i in range(1, n_frame):
        # print('Processing Frame', i)
        newXs, newYs = estimateTrans.estimateAllTranslation(startXs, startYs, frames[i - 1], frames[i])
        # print(startXs, startYs, newXs, newYs, bboxs[i - 1])
        Xs, Ys, bboxs[i] = applyGeometricTrans.run(startXs, startYs, newXs, newYs, bboxs[i - 1])

        # update coordinates
        startXs = Xs
        startYs = Ys

        # update feature points as required
        n_features_left = np.sum(Xs != -1)
        # print('# of Features: %d' % n_features_left)
        # if n_features_left < 15:
        #     print('Generate New Features')
        #     if useCV:
        #         startXs, startYs = getFeatures.getFeatures_cv(cv2.cvtColor(frames[0], cv2.COLOR_RGB2GRAY), bboxs[0])
        #      KHALED
        #     else:
        #         startXs, startYs = getFeatures.getFeatures_cv(cv2.cvtColor(frames[0], cv2.COLOR_RGB2GRAY), bboxs[0], use_shi=False)

        # draw bounding box and visualize feature point for each object
        frames_draw[i] = frames[i].copy()
        for j in range(n_object):
            (xmin, ymin, boxw, boxh) = cv2.boundingRect(bboxs[i][j, :, :].astype(int))
            frames_draw[i] = cv2.rectangle(frames_draw[i], (xmin, ymin), (xmin + boxw, ymin + boxh), (255, 0, 0), 2)
            # print(startXs.shape[0])
            for k in range(startXs.shape[0]):
                frames_draw[i] = cv2.circle(frames_draw[i], (int(startXs[k, j]), int(startYs[k, j])), 3, (0, 0, 255),
                                            thickness=2)

        # imshow if to play the result in real time
        if play_realtime:
            cv2.imshow("win", frames_draw[i])
            cv2.waitKey(10)
        if save_to_file:
            out.write(frames_draw[i])
        if i == 90:
            print(90/(time()-t))

    if save_to_file:
        out.release()


if __name__ == "__main__":
    cap = cv2.VideoCapture("Easy.mp4")
    main(cap, draw_bb=True, play_realtime=True, save_to_file=True, useCV=False)
    cap.release()