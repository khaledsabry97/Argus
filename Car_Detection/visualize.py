import colorsys
import imghdr
import os
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import Car_Detection.util as util
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import torch 
from torch.autograd import Variable

from Car_Detection.darknet import Darknet
def read_classes(classes_path):
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names

def read_anchors(anchors_path):
    with open(anchors_path) as f:
        anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        anchors = np.array(anchors).reshape(-1, 2)
    return anchors

def generate_colors(class_names):
    hsv_tuples = [(x / len(class_names), 1., 1.) for x in range(len(class_names))]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    random.seed(10101)  # Fixed seed for consistent colors across runs.
    random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
    random.seed(None)  # Reset seed to default.
    return colors



def preprocess_image(img_path, model_image_size):
    image_type = imghdr.what(img_path)
    image = Image.open(img_path)
    resized_image = image.resize(tuple(reversed(model_image_size)), Image.BICUBIC)
    image_data = np.array(resized_image, dtype='float32')
    image_data /= 255.
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    return image , image_data

def preprocess_img(image, model_image_size):
    image= Image.fromarray(np.uint8(image)*255)
    resized_image = image.resize(tuple(reversed(model_image_size)), Image.BICUBIC)
    image_data = np.array(resized_image, dtype='float32')
    image_data /= 255.
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    return image , image_data



def draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors):
    
    #font = ImageFont.truetype(font='font/FiraMono-Medium.otf',size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    thickness = (image.size[0] + image.size[1]) // 1000
    for i, c in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[c]
        box = out_boxes[i]
        score = out_scores[i]

        #label = '{} {:.2f}'.format(predicted_class, score.item())
        label = '{} '.format(predicted_class)

        draw = ImageDraw.Draw(image)
        label_size = draw.textsize(label)

        left,top, right, bottom  = box.cpu()
        left=left.item()
        top=top.item()
        right=right.item()
        bottom=bottom.item()
    
       
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
        #print(label, (left, top), (right, bottom))

        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        # My kingdom for a good redistributable image drawing library.
        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline=colors[c])
        draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=colors[c])
        draw.text(tuple(text_origin), label, fill=(0, 0, 0))
        del draw

















def visualize_result(image_file):  
    img = cv2.imread(image_file)
    img_shape=img.shape
    img = cv2.resize(img, (608,608))          #Resize to the input dimension
    img_ =  img[:,:,::-1].transpose((2,0,1))  # BGR -> RGB | H X W C -> C X H X W 
    img_ = img_[np.newaxis,:,:,:]/255.0       #Add a channel at 0 (for batch) | Normalise
    img_ = torch.from_numpy(img_).float()     #Convert to float
    img_ = Variable(img_)                     # Convert to Variable
 

    
    model = Darknet("./config/yolov3.cfg",CUDA=False)
    model.load_weight("./config/yolov3.weights")
    preds,_ = model(img_)
    out_scores, out_boxes, out_classes=util.get_filtered_boxes(img_shape,preds,CUDA=False)
    out_classes=[c for c in out_classes if c in [2,3,5,7]]
    print("from vis",out_classes)
    class_names = read_classes("./config/coco.names")
    # Preprocess your image
    image, image_data = preprocess_image(image_file, model_image_size = (608, 608))
   
    # Print predictions info
    print('Found {} boxes for {}'.format(len(out_boxes), image_file))
    # Generate colors for drawing bounding boxes.
    colors = generate_colors(class_names)
    # Draw bounding boxes on the image file
    draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)
    # Save the predicted bounding box on the image
    image.save(os.path.join("./out", image_file), quality=90)
    # Display the results in the notebook
    output_image = cv2.imread(os.path.join("./out", image_file))
    cv2.imshow("out",output_image)
    cv2.waitKey(0)
    
    return out_scores, out_boxes, out_classes




def visualize_video(Frame,CUDA=False):  
    img_shape=Frame.shape
    img_=cv2.dnn.blobFromImage(Frame, 1 / 255.0, (608, 608),
		swapRB=True, crop=False)
    img_ = torch.from_numpy(img_).float()     #Convert to float
    img_ = Variable(img_)                     # Convert to Variable
 

    
    model = Darknet("./config/yolov3.cfg",CUDA=CUDA)
    model.load_weight("./config/yolov3.weights")
    if CUDA:
        model=model.cuda()
        img_=img_.cuda()
    
    preds,_ = model(img_)
    out_scores, out_boxes, out_classes=util.get_filtered_boxes(img_shape,preds,CUDA=CUDA)
    class_names = read_classes("./config/coco.names")
    # Preprocess your image
    image, image_data = preprocess_img(Frame, model_image_size = (608, 608))
    # Generate colors for drawing bounding boxes.
    colors = generate_colors(class_names)
    # Draw bounding boxes on the image file
    draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)
    
    return image


def annotate(image_file,path):  
    img = cv2.imread(image_file)
    img_shape=img.shape
    img = cv2.resize(img, (608,608))          #Resize to the input dimension
    img_ =  img[:,:,::-1].transpose((2,0,1))  # BGR -> RGB | H X W C -> C X H X W 
    img_ = img_[np.newaxis,:,:,:]/255.0       #Add a channel at 0 (for batch) | Normalise
    img_ = torch.from_numpy(img_).float()     #Convert to float
    img_ = Variable(img_)                     # Convert to Variable
 

    
    model = Darknet("./config/yolov3.cfg",CUDA=False)
    model.load_weight("./config/yolov3.weights")
    preds,_ = model(img_)
    out_scores, out_boxes, out_classes=util.get_filtered_boxes(img_shape,preds,CUDA=False)
    class_names = read_classes("./config/coco.names")
    # Preprocess your image
    image, image_data = preprocess_image(image_file, model_image_size = (608, 608))
    # Generate colors for drawing bounding boxes.
    colors = generate_colors(class_names)
    # Draw bounding boxes on the image file
    draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)
    # Save the predicted bounding box on the image
    image.save(os.path.join("../"+"annotated", image_file[5:].replace('/','_')), quality=90)
    




if __name__ == "__main__":
    image_file=sys.argv[1]
    visualize_result(image_file)
    
        
