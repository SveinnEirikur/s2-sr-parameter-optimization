import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, UpSampling2D, Input, BatchNormalization,Activation,Conv3D
from tensorflow.keras.layers import LeakyReLU,Concatenate, Conv2DTranspose
from ..models.common import *

def skip(ndown=5,channelin=10,channelout=6):
    #down side
    input_layer = Input((None,None,channelin))
    out = input_layer
    skips=[]

    for i in range(ndown):
        out = convbn(out,dilation_rate=1)
        skips.append(convbn(out,filters=25,kernel_size=1))
    skips.reverse()
    for i in range(ndown):
        if i==0:
            out=convbn(out)
        else:
            out = convbn(Concatenate()([out,skips[i]]))

    out = Conv2D(channelout,1)(out)
    # out=convbn(out,filters=channelout,kernel_size=1)
    out_layer = Add()([input_layer[:, :, :, 0:channelout], out])

    mymodel=Model(input_layer,out)
    return mymodel


