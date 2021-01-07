import cv2
from VIF.HornSchunck import HornSchunck

"""
    Unit test for Horn Schunk class.
"""


def test_hs_init():
    """
        Verify that object is created successfully
    """

    try:
        hs = HornSchunck()
        assert 1

    except:
        assert 0


def test_hs_derivatives():
    """
        Verify the results of differentiating two frames
    """

    try:
       frame1 = cv2.imread('Unit test/f0.jpg')
       frame2 = cv2.imread('Unit test/f1.jpg')
       shape = (134, 100)
       frame1 = cv2.resize(frame1, shape)
       frame2 = cv2.resize(frame2, shape)
       frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
       frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
       hs = HornSchunck()
       x, y, t = hs.derivatives(frame1, frame2)

       assert x.any() != 0 and y.any() != 0 and t.any() != 0

    except:
        assert 0


def test_hs_process():
    """
        Verify the results of processing two frames
    """

    try:
       frame1 = cv2.imread('Unit test/f0.jpg')
       frame2 = cv2.imread('Unit test/f1.jpg')
       shape = (134, 100)
       frame1 = cv2.resize(frame1, shape)
       frame2 = cv2.resize(frame2, shape)
       frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
       frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
       hs = HornSchunck()
       H, V, M = hs.process(frame1, frame2)

       assert H.any() != 0 and V.any() != 0 and M.any() != 0

    except:
        assert 0
