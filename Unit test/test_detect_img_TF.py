from Car_Detection_TF.yolo import YOLO
from PIL import Image
import cv2

"""
    Unit test for detect_img using TF.
    args: cv image
    return: list of boxes bounding detected vehicles
"""

def test_detect_img_invalid_input():
    """
        Verify type consistency of the function
    """
    yolo = YOLO()
    img, bboxes = yolo.detect_image(None)

    assert img == None and bboxes == None


def test_detect_img_valid_input():
    """
        Verify the method works as expected
    """

    yolo = YOLO()
    frame = cv2.imread('Car_Detection/test.png')
    image = Image.fromarray(frame)
    img, bboxes = yolo.detect_image(image)

    assert len(bboxes) != 0 and len(bboxes) >= 2

