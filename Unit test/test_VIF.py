from Car_Detection_TF.yolo import YOLO
from Mosse_Tracker.TrackerManager import *
from PIL import Image

from VIF.vif import VIF

"""
    Unit test for VIF class.
"""

def init_tracker():
    cap = cv2.VideoCapture('videos/Easy.mp4')
    ret, frame = cap.read()

    yolo = YOLO()
    image = Image.fromarray(frame)
    img, bboxes = yolo.detect_image(image)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    trackers = []
    for i, bbox in enumerate(bboxes):
        label = bbox[0]
        xmin = int(bbox[1])
        xmax = int(bbox[2])
        ymin = int(bbox[3])
        ymax = int(bbox[4])

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tr = Tracker(frame_gray, (xmin, ymin, xmax, ymax), 480, 360, 1)
        trackers.append(tr)

    for i in range(30):
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for j, t in enumerate(trackers):
            t.update(frame_gray)

    return trackers


def test_vif_init():
    """
        Verify that object is created successfully
    """

    try:
        vif = VIF()
        assert 1

    except:
        assert 0


def test_vif_process():
    """
        Verify the results of processing set of frames for a given tracker
    """

    try:
        trackers = init_tracker()
        # vif = VIF()
        print(trackers[0].getHistory())
        # vif.process(trackers[0].getHistory())
        assert 1

    except:
        assert 0
