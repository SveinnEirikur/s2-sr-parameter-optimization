import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Input,Add,LeakyReLU
from models.common import *

def residualnet(K=24,channelin=10,channelout=6):
    input_layer = Input((None,None,channelin))
    out = input_layer
    out=Conv2D(64,3,padding="same")(out)
    out=LeakyReLU(alpha=0.01)(out)
    first_out=out
    for i in range(K):
        out=resblock(out)

    out=Conv2D(64,3,padding="same")(out)
    out=LeakyReLU(alpha=0.01)(out)
    out=Conv2D(64,3,padding="same")(out)
    out=Add()([first_out,out])
    out=Conv2D(128,3,padding="same")(out)
    out=LeakyReLU(alpha=0.01)(out)
    out=Conv2D(256,3,padding="same")(out)
    out=LeakyReLU(alpha=0.01)(out)
    out=Conv2D(filters=channelout,kernel_size=3,padding="same")(out)
    out_layer=Add()([input_layer[:,:,:,0:6],out])
    # out_layer=Conv2D(channelout,1)(out_layer)

    model=Model(input_layer,out_layer)
    return model

