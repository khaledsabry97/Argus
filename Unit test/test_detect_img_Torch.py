from Car_Detection.detect import detect_image
from Car_Detection.darknet import Darknet
import cv2

"""
    Unit test for detect_img using Pytorch.
    args: cv image
    return: list of boxes bounding detected vehicles
"""

def test_detect_img_invalid_input():
    """
        Verify type consistency of the function
    """
    model = Darknet("Car_Detection/config/yolov3.cfg", CUDA=False)
    model.load_weight("Car_Detection/config/yolov3.weights")
    bboxes = detect_image(None, model, CUDA=False)

    assert bboxes == None


def test_detect_img_valid_input():
    """
        Verify the method works as expected
    """
    model = Darknet("Car_Detection/config/yolov3.cfg", CUDA=False)
    model.load_weight("Car_Detection/config/yolov3.weights")
    image = cv2.imread('Car_Detection/test.png')
    bboxes = detect_image(image, model, CUDA=False)

    assert len(bboxes) != 0 and len(bboxes) >= 2

