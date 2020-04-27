from __future__ import division

import torch 
import torch.nn as nn
import torch.nn.functional as F 
from torch.autograd import Variable
import numpy as np
import Car_Detection.util as util
import Car_Detection.weight_loader as loader


class Darknet(nn.Module):
    def __init__(self, cfgfile, CUDA):
        self.CUDA = CUDA
        super(Darknet, self).__init__()
        self.blocks = util.parse_cfg(cfgfile)
        self.net_param, self.layer_list = util.create_layers(self.blocks)

    def load_weight(self, file):
        loader.load_weight(file, self.layer_list, self.blocks)

    def forward(self, x):
        blocks = self.blocks[1:]
        outputs = {}  # We cache the outputs for the route layer
        empty = 1
        for i, block in enumerate(blocks):
            layer_type = block['layer_name']
            if (layer_type == 'convolutional' or layer_type == "upsample"):
                x = self.layer_list[i](x)
            elif (layer_type == 'route'):
                layers = block["layers"]
                layers = layers.split(',')
                layers = [int(a) for a in layers]
                if (layers[0]) > 0:
                    layers[0] = layers[0] - i

                if (len(layers) == 1):
                    x = outputs[i + (layers[0])]
                else:
                    if (layers[1]) > 0:
                        layers[1] = layers[1] - i

                    map1 = outputs[i + layers[0]]
                    map2 = outputs[i + layers[1]]

                    x = torch.cat((map1, map2), 1)

            elif layer_type == "shortcut":
                from_ = int(block["from"])
                x = outputs[i - 1] + outputs[i + from_]


            elif layer_type == "yolo":
                anchors = self.layer_list[i][0].anchors
                # Get the input dimensions
                inp_dim = int(self.net_param["height"])

                # Get the number of classes
                num_classes = int(block["classes"])
                # Transform
                x = x.data
                x_exp, scaled_anchors = util.predict_transform(x, inp_dim, anchors, num_classes, self.CUDA)
                if empty:  # if no collector has been intialised.
                    empty = 0
                    detections = x_exp

                else:
                    detections = torch.cat([detections, x_exp], axis=1)

            outputs[i] = x
        return detections, scaled_anchors
