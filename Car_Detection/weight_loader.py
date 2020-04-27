from __future__ import division

import torch 
import torch.nn as nn
import torch.nn.functional as F 
from torch.autograd import Variable
import numpy as np
import Car_Detection.util as util


def load_weight(file,module_list,blocks):
  with open(file,'rb') as f:
    #The first 5 values are header information 
    # 1. Major version number
    # 2. Minor Version Number
    # 3. Subversion number 
    # 4,5. Images seen by the network (during training)
    header = np.fromfile(f, dtype = np.int32, count = 5)
    header = torch.from_numpy(header)
    seen = header[3]
    weights = np.fromfile(f, dtype = np.float32)
    ptr = 0
    for i in range(len(module_list)):
        module_type = blocks[i + 1]["layer_name"]

        #If module_type is convolutional load weights
        #Otherwise ignore.
        if module_type == "convolutional":
            model = module_list[i]
            try:
                batch_normalize = int(blocks[i+1]["batch_normalize"])
            except:
                batch_normalize = 0

            conv = model[0]
            if (batch_normalize):
              bn = model[1]

              #Get the number of weights of Batch Norm Layer
              num_bn_biases = bn.bias.numel()

              #Load the weights
              bn_biases = torch.from_numpy(weights[ptr:ptr + num_bn_biases])
              ptr += num_bn_biases

              bn_weights = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
              ptr  += num_bn_biases
              bn_running_mean = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
              ptr  += num_bn_biases

              bn_running_var = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
              ptr  += num_bn_biases

              #Cast the loaded weights into dims of model weights. 
              bn_biases = bn_biases.view_as(bn.bias.data)
              bn_weights = bn_weights.view_as(bn.weight.data)
              bn_running_mean = bn_running_mean.view_as(bn.running_mean)
              bn_running_var = bn_running_var.view_as(bn.running_var)

              #Copy the data to model
              bn.bias.data.copy_(bn_biases)
              bn.weight.data.copy_(bn_weights)
              bn.running_mean.copy_(bn_running_mean)
              bn.running_var.copy_(bn_running_var)
            else:
              #Number of biases
              num_biases = conv.bias.numel()

              #Load the weights
              conv_biases = torch.from_numpy(weights[ptr: ptr + num_biases])
              ptr = ptr + num_biases

              #reshape the loaded weights according to the dims of the model weights
              conv_biases = conv_biases.view_as(conv.bias.data)

              #Finally copy the data
              conv.bias.data.copy_(conv_biases)
            #Let us load the weights for the Convolutional layers
            num_weights = conv.weight.numel()

            #Do the same as above for weights
            conv_weights = torch.from_numpy(weights[ptr:ptr+num_weights])
            ptr = ptr + num_weights

            conv_weights = conv_weights.view_as(conv.weight.data)
            conv.weight.data.copy_(conv_weights)
