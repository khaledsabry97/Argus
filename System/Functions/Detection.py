import cv2
from PIL import Image

#from Car_Detection_TF.yolo import YOLO
from Mosse_Tracker.TrackerManager import Tracker


class Detection:
    def __init__(self,yolo):
        self.yolo = yolo



    def detect(self,frames,frame_width,frame_height,read_file,boxes_file = None):
        # detect vehicles
        if read_file:
            # From files
            boxes = boxes_file
        else:
            img = Image.fromarray(frames[0])
            _, boxes = self.yolo.detect_image(img)

        return boxes