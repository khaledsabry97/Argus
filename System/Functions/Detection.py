import cv2
from PIL import Image

#from Car_Detection_TF.yolo import YOLO
from Mosse_Tracker.TrackerManager import Tracker
from System.Functions.FrameEncodeDecode import imgDecode


class Detection:
    def __init__(self):
        pass


    def detect(self,frames,frame_width,frame_height,read_file = None,boxes_file = None):
        # detect vehicles
        if read_file != None:
            # From files
            boxes = boxes_file
        else:
            yolo = YOLO()
            img = Image.fromarray(frames[0])
            _, boxes = yolo.detect_image(img)

        return boxes