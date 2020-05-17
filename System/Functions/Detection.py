import cv2
from PIL import Image

#from Car_Detection_TF.yolo import YOLO
from Mosse_Tracker.TrackerManager import Tracker


class Detection:
    def __init__(self):
        pass


    def detect(self,frames,frame_width,frame_height,read_file = None,boxes_file = None):
            trackers = []
            trackerId = 0
            frame = frames[0]
            # detect vehicles
            if read_file != None:
                # From files
                boxes = boxes_file
            else:
                yolo = YOLO()
                img = Image.fromarray(frames[0])
                _, boxes = yolo.detect_image(img)


            for _, box in enumerate(boxes):

                xmin = int(box[1])
                xmax = int(box[2])
                ymin = int(box[3])
                ymax = int(box[4])

                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                trackerId += 1
                # no need for frame_width and frame_height
                xmax = min(xmax,frame_width-1)
                ymax = min(ymax,frame_height-1)

                trackers.append(Tracker(frame_gray, (xmin, ymin, xmax, ymax), frame_width, frame_height, trackerId))
            return trackers