import time 
import sys
import cv2
from Car_Detection.darknet import Darknet
import Car_Detection.util as util
from  Car_Detection.visualize import visualize_result
import torch 
from torch.autograd import Variable
import numpy as np


def Yolo_image(Frame, model, CUDA=False):  ##set to true to enable GPU
    img_shape = Frame.shape
    img_ = cv2.dnn.blobFromImage(Frame, 1 / 255.0, (608, 608),
                                 swapRB=True, crop=False)
    img_ = torch.from_numpy(img_).float()  # Convert to float
    img_ = Variable(img_)  # Convert to Variable

    if CUDA:
        model = model.cuda()
        img_ = img_.cuda()
    start = time.time()
    preds, _ = model(img_)
    out_scores, out_boxes, out_classes = util.get_filtered_boxes(img_shape, preds, CUDA=CUDA)
    end = time.time()
    elapsed = end - start
    print('time taken: ', elapsed, 'secs')
    objs_list = []
    for box, class_id, score in zip(out_boxes, out_classes, out_scores):
        x1 = box[0].item()
        y1 = box[1].item()
        x2 = box[2].item()
        y2 = box[3].item()
        obj = [class_id.item(), x1, x2, y1, y2, score.item()]
        objs_list.append(obj)

    return objs_list  ##list of detected object each object is a list in the form [label,x1,y1,x2,y2,confidence]


if __name__ == "__main__":
    image_file = sys.argv[1]
    Frame = cv2.imread(image_file)
    model = Darknet("./config/yolov3.cfg", CUDA=False)
    model.load_weight("./config/yolov3.weights")
    obj_list = Yolo_image(Frame, CUDA=False)
    visualize_result(image_file)

