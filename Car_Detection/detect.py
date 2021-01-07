import time 
import sys
from Car_Detection.visualize import visualize_result
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')##remove this line 
import cv2
from Car_Detection.darknet import Darknet
import Car_Detection.util as util
import torch 
from torch.autograd import Variable
import numpy as np

def detect_image(Frame, model, CUDA=False):##set to true to enable GPU
    img_shape=Frame.shape
    img_=cv2.dnn.blobFromImage(Frame, 1 / 255.0, (608, 608),
		swapRB=True, crop=False)
    img_ = torch.from_numpy(img_).float()     #Convert to float
    img_ = Variable(img_)                     # Convert to Variable
 

    # model = Darknet("./config/yolov3.cfg",CUDA=CUDA)
    # model.load_weight("./config/yolov3.weights")
    if CUDA:
        model=model.cuda()
        img_=img_.cuda()
    start=time.time()
    preds,_ = model(img_)
    out_scores, out_boxes, out_classes=util.get_filtered_boxes(img_shape,preds,CUDA=CUDA)
    end=time.time()
    elapsed=end-start
    print('time taken: ', elapsed,'secs')
    objs_list=[]
    for box,class_id,score in zip(out_boxes,out_classes,out_scores):
        x1=box[0].item()
        y1=box[1].item()
        x2=box[2].item()
        y2=box[3].item()
        if(class_id.item()in[2,3,5,7]):
          obj=[class_id.item(),x1,x2,y1,y2,score.item()]
        else:
          continue
        objs_list.append(obj)
        print([c[0] for c in objs_list])
   
    return objs_list ##list of detected object each object is a list in the form [label,x1,y1,x2,y2,confidence]
if __name__ == "__main__":
        image_file=sys.argv[1]
        Frame=cv2.imread(image_file)
        obj_list=detect_image(Frame,CUDA=False)
        visualize_result(image_file)

