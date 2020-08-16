from __future__ import division

import torch 
import torch.nn as nn
import torch.nn.functional as F 
import numpy as np
import sys
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
class EmptyLayer(nn.Module):
    def __init__(self):
        super(EmptyLayer, self).__init__()

class DetectionLayer(nn.Module):
    def __init__(self, anchors):
        super(DetectionLayer, self).__init__()
        self.anchors = anchors






def parse_cfg(cfgfile):
    """
    Takes a configuration file
    
    Returns a list of blocks. Each blocks describes a block in the neural
    network to be built. Block is represented as a dictionary in the list
    
    """

    with open(cfgfile,'r') as f:
     lines = f.read().split('\n')                        # store the lines in a list
     lines = [x for x in lines if len(x) > 0]               # get read of the empty lines 
     lines = [x for x in lines if x[0] != '#']              # get rid of comments
     lines = [x.rstrip().lstrip() for x in lines]           # get rid of fringe whitespaces

     blocks=[]
     block={}
    for line in lines:
       if line[0]=='[':
         if len(block) != 0:          # If block is not empty, implies it is storing values of previous block.
            blocks.append(block)     # add it the blocks list
            block = {} 
         block['layer_name']=line[1:-1].rstrip().lstrip()
       else:
         key,value=line.split('=')
         block[key.rstrip().lstrip()]=value.lstrip().rstrip()
    blocks.append(block)
    return blocks



def create_layers(blocks):
  net_params=blocks[0]
  layer_list = nn.ModuleList()
  prev_filters = 3
  output_filters = []

  for index, x in enumerate(blocks[1:]):
        module = nn.Sequential()
        if(x['layer_name']=='convolutional'):
          filters=int(x['filters'])
          kernel_size=int(x['size'])
          stride=int(x['stride'])
          activation=x['activation']
          padding=x['pad']
          try:
                batch_normalize = int(x["batch_normalize"])
                bias = False
          except:
                batch_normalize = 0
                bias = True

          if padding:
                pad = (kernel_size - 1) // 2
          else:
                pad = 0
          #Add the convolutional layer
          conv = nn.Conv2d(prev_filters, filters, kernel_size, stride, pad, bias = bias)
          module.add_module("conv_{0}".format(index), conv)
          #Add batch_norm
          if batch_normalize:
                bn = nn.BatchNorm2d(filters)
                module.add_module("batch_norm_{0}".format(index), bn)
          #Check the activation. 
            #It is either Linear or a Leaky ReLU for YOLO
          if activation == "leaky":
                activn = nn.LeakyReLU(0.1, inplace = True)
                module.add_module("leaky_{0}".format(index), activn)
          elif(activation=='relu'):
            activn=nn.ReLU(inplace=False)
            module.add_module("relu_{0}".format(index), activn)
        #If it's an upsampling layer
        #We use Bilinear2dUpsampling
        elif (x["layer_name"] == "upsample"):
            stride = int(x["stride"])
            upsample = nn.Upsample(scale_factor = 2,mode='bilinear', align_corners=True)
            module.add_module("upsample_{}".format(index), upsample)
        elif(x["layer_name"]=='route'):
            layers=x["layers"]
            start=int(layers.split(',')[0])
            try:
              end=int(layers.split(',')[1])
            except:
              end=0

            if start > 0: 
                start = start - index
            if end > 0:
                end = end - index
            route = EmptyLayer()
            module.add_module("route_{0}".format(index), route)
            if end < 0:
                filters = output_filters[index + start] + output_filters[index + end]
            else:
                filters= output_filters[index + start]

        
         #shortcut corresponds to skip connection
        elif x["layer_name"] == "shortcut":
            shortcut = EmptyLayer()
            module.add_module("shortcut_{}".format(index), shortcut)
        #Yolo is the detection layer
        elif x["layer_name"] == "yolo":
            mask = x["mask"].split(",")
            mask = [int(x) for x in mask]

            anchors = x["anchors"].split(",")
            anchors = [int(a) for a in anchors]
            anchors = [(anchors[i], anchors[i+1]) for i in range(0, len(anchors),2)]
            anchors = [anchors[i] for i in mask]

            detection = DetectionLayer(anchors)
            module.add_module("Detection_{}".format(index), detection) 
        
        
        prev_filters=filters
        output_filters.append(filters)   
        layer_list.append(module)
  return (net_params,layer_list)






def predict_transform(prediction, inp_dim, anchors, num_classes, CUDA = False):
    batch_size = prediction.size(0)
    stride =  inp_dim // prediction.size(2)
    grid_size = prediction.size(2)
    bbox_attrs = 5 + num_classes
    num_anchors = len(anchors)
    scaled_anchors = [(a[0]/stride, a[1]/stride) for a in anchors]



    prediction = prediction.view(batch_size, bbox_attrs*num_anchors, grid_size*grid_size)
    prediction = prediction.transpose(1,2).contiguous()
    prediction = prediction.view(batch_size, grid_size*grid_size*num_anchors, bbox_attrs)


    #Sigmoid the  centre_X, centre_Y. and object confidencce
    prediction[:,:,0] = torch.sigmoid(prediction[:,:,0])
    prediction[:,:,1] = torch.sigmoid(prediction[:,:,1])
    prediction[:,:,4] = torch.sigmoid(prediction[:,:,4])
    

   
    #Add the center offsets
    grid_len = np.arange(grid_size)
    a,b = np.meshgrid(grid_len, grid_len)
    
    x_offset = torch.FloatTensor(a).view(-1,1)
    y_offset = torch.FloatTensor(b).view(-1,1)
    x_y_offset = torch.cat((x_offset, y_offset), 1).repeat(1,num_anchors).view(-1,2).unsqueeze(0)
    
    if CUDA:
        prediction=prediction.cuda()
        x_offset = x_offset.cuda()
        y_offset = y_offset.cuda()
        x_y_offset = x_y_offset.cuda()
   
    prediction[:,:,:2] += x_y_offset
   
    #log space transform height and the width
    anchors = torch.FloatTensor(scaled_anchors)
    
    if CUDA:
        anchors = anchors.cuda()
    
    anchors = anchors.repeat(grid_size*grid_size, 1).unsqueeze(0)
    prediction[:,:,2:4] = torch.exp(prediction[:,:,2:4])*anchors

    #Softmax the class scores
    prediction[:,:,5: 5 + num_classes] = torch.sigmoid((prediction[:,:, 5 : 5 + num_classes]))

    prediction[:,:,:4] *= stride 
    
    
    return  prediction,scaled_anchors









def filter_yolo_boxes(obj_conf,boxes,boxes_classes_probs,threshold=0.25):
    box_scores = obj_conf*boxes_classes_probs
    box_classes = torch.argmax(box_scores,-1)
    box_class_scores = torch.max(box_scores,-1)[0]
    filtering_mask = box_class_scores>threshold
    scores=box_class_scores[filtering_mask]
    classes = box_classes[filtering_mask]
    boxes=boxes[filtering_mask]
   
    return scores, boxes, classes
    #return box_scores, boxes, box_classes


def box2corner(box_xy,box_wh):
      boxes=torch.zeros(box_xy[0].shape[0],box_xy[0].shape[1],4)
      boxes[:,:,0] = (box_xy[0] - box_wh[0]/2)
      boxes[:,:,1] = (box_xy[1] - box_wh[1]/2)
      boxes[:,:,2] = (box_xy[0] + box_wh[0]/2) 
      boxes[:,:,3] = (box_xy[1] + box_wh[1]/2)
      return boxes




def scale_boxes(boxes, image_shape,CUDA=False):
    """ Scales the predicted boxes in order to be drawable on the image"""
    height = torch.tensor(image_shape[0],dtype=torch.float32)
    width = torch.tensor(image_shape[1],dtype=torch.float32)
    factor_h=height/608
    factor_w=width/608
    image_dims =torch.stack([factor_w, factor_h, factor_w , factor_h])
    if CUDA:
      image_dims=image_dims.cuda()
    image_dims = torch.reshape(image_dims, [1, 4])
    boxes = boxes* image_dims
    return boxes


def get_filtered_boxes(image_shape,predictions, score_threshold=.25, iou_threshold=0.6,CUDA=False):
    box_confidence= predictions[:,:,4]
    box_confidence=box_confidence.view(box_confidence.shape[0],box_confidence.shape[1],1)
    box_xy= (predictions[:,:,0],predictions[:,:,1]) 
    box_wh= (predictions[:,:,2],predictions[:,:,3]) 
    box_class_probs = predictions[:,:,5:]
    boxes=box2corner(box_xy,box_wh)
    if CUDA:
      boxes=boxes.cuda()
    boxes = scale_boxes(boxes, image_shape,CUDA)
    scores, boxes, classes = filter_yolo_boxes(box_confidence, boxes, box_class_probs, threshold = score_threshold)
    try:
      scores, boxes, classes =  NMS(scores, boxes, classes,score_threshold, iou_threshold,CUDA)
    except ValueError:
      pass
    return scores, boxes, classes





def iou(box1, box2):
    """Implement the intersection over union (IoU) between box1 and box2
    
    Arguments:
    box1 -- first box, list object with coordinates (x1, y1, x2, y2)
    box2 -- second box, list object with coordinates (x1, y1, x2, y2)
    """

    xi1 = max(box1[0], box2[0])
    yi1 = max(box1[1], box2[1])
    xi2 = min(box1[2], box2[2])
    yi2 = min(box1[3], box2[3])
    inter_area = (xi2 - xi1)*(yi2 - yi1)
       

    # Calculate the Union area by using Formula: Union(A,B) = A + B - Inter(A,B)
    box1_area = (box1[3] - box1[1])*(box1[2]- box1[0])
    box2_area = (box2[3] - box2[1])*(box2[2]- box2[0])
    union_area = (box1_area + box2_area) - inter_area
    
    # compute the IoU
    iou = inter_area / union_area

    return iou


    



#def NMS(scores, boxes, classes,iou_threshold,CUDA=False):
  # if len(boxes) == 0:
  #       return boxes

  # Create an empty list to hold the best bounding boxes after
  # Non-Maximal Suppression (NMS) is performed
  # if CUDA:
  #     best_boxes=best_boxes.cuda()
  #     best_classes=best_classes.cuda()
  # _,sortIds = torch.sort(scores, descending = True)
  # for i in range(0,len(boxes)):
  #   current_box=boxes[sortIds[i]]
  #   current_class=classes[sortIds[i]]
  #   if scores[sortIds[i]]>0:
  #     best_boxes=torch.cat([best_boxes,current_box.view(1,-1)],axis=0)
  #     best_classes=torch.cat([best_classes,current_class.view(1,-1)],axis=0)
  #     for j in range(i+1,len(boxes)):
  #         box_j = boxes[sortIds[j]]
  #         if iou(current_box, box_j) > iou_threshold:
  #           scores[sortIds[j]]=0
  # best_scores=scores[scores.nonzero()]
  
  #return  best_scores,best_boxes,best_classes


def NMS(scores, boxes, classes,score_threshold,iou_threshold,CUDA=False):
  if len(boxes) == 0:
        return boxes
  idx=cv2.dnn.NMSBoxes(boxes.tolist(),scores.tolist(),score_threshold,iou_threshold)
  idx=idx.flatten()
  return scores[idx],boxes[idx],classes[idx]




   
   



                          
