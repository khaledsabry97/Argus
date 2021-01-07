import cv2
from PIL import Image
from Car_Detection.detect import detect_image
from Car_Detection.darknet import Darknet
import numpy as np
#from Car_Detection_TF.yolo import YOLO
from Mosse_Tracker.TrackerManager import Tracker


class Detection:
    def __init__(self,yolo):
        self.yolo = yolo

        self.model = Darknet("M:/Argus/Car_Detection/config/yolov3.cfg", CUDA=False)
        self.model.load_weight("M:/Argus/Car_Detection/config/yolov3.weights")


    def detect(self,frames,frame_width,frame_height,read_file,boxes_file = None, read_file_self=False, tf=True):
        boxes = []
        # detect vehicles
        if read_file_self:
            # From files
            boxes = boxes_file
        elif tf:
            img = Image.fromarray(frames[0])
            _, boxes = self.yolo.detect_image(img)
        else:
            boxes = detect_image(frames[0], self.model)

        return boxes