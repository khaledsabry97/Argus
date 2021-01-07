from Car_Detection_TF.yolo import YOLO
from Mosse_Tracker.TrackerManager import *
from PIL import Image

"""
    Unit test for Tracker manager class.
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

    return trackers, cap


def test_tracker_init():
    """
        Verify that object is created successfully
    """

    trackers, cap = init_tracker()

    assert len(trackers) > 0

def test_tracker_addHistory():
    """
        Verify that tracker updates are saved
    """

    trackers, cap = init_tracker()
    tr = trackers[0]
    tr.addHistory([1, 1, 1, 1])

    assert len(tr.history) >= 1

def test_tracker_getHistory():
    """
        Verify that ability to retrieve the whole history of a tracker
    """

    trackers, cap = init_tracker()
    tr = trackers[0]
    tr.addHistory([1, 1, 1, 1])

    assert tr.getHistory()[1] == [1, 1, 1, 1]


def test_tracker_getPosition():
    """
        Verify that ability to retrieve last known position for vehicle
    """

    trackers, cap = init_tracker()
    tr = trackers[0]
    tr.addHistory([1, 1, 1, 1])

    assert tr.getTrackerPosition() == [1, 1, 1, 1]


def test_tracker_clearHistory():
    """
        Verify that ability to clear the entire history of a tracker and adjust the tracker accordingly
    """

    trackers, cap = init_tracker()
    tr = trackers[0]
    tr.clearHistory()

    assert len(tr.getHistory()) == 0


def test_tracker_getMaxSpeed():

    trackers, cap = init_tracker()
    tr = trackers[0]

    assert tr.getMaxSpeed() == 0


def test_tracker_getCarSizeCoefficient():

    trackers, cap = init_tracker()
    tr = trackers[0]

    assert tr.getCarSizeCoefficient() > 0
