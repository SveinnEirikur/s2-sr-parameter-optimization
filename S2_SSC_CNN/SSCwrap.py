import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, UpSampling2D, Input, BatchNormalization,Activation
from tensorflow.keras.layers import LeakyReLU,Concatenate, Conv2DTranspose
from tensorflow.keras.callbacks import ModelCheckpoint
from .models.skipnet import *
from .utils.common import *
from PIL import Image
import matplotlib.pyplot as plt
from skimage.transform import rescale, resize, pyramid_reduce
import os
import scipy.io as sio
import h5py
from s2synth import rr_s2_data


def SSCwrap(Yim, d=[6,1,1,1,2,2,2,1,2,6,2,2], batch_size = 64, lr=0.0005, ndown=3, num_epochs = 500, mtf=[ .32, .26, .28, .24, .38, .34, .34, .26, .33, .26, .22, .23], mtf_down=False, verbose=True):
    tf.keras.backend.clear_session()

    Xf = np.moveaxis(np.array([Yim[i] for i,v in enumerate(d) if v == 1]),[0,1,2],[2,0,1])
    Xc = np.moveaxis(np.array([Yim[i] for i,v in enumerate(d) if v == 2]),[0,1,2],[2,0,1])
    (nl,nc,nb1) = Xf.shape
        
    Yhat = np.zeros((nl,nc,len(d)))*np.nan
    
    if mtf_down:
        nl_t1 = int(nl//4 * 4)
        nl_t2 = int(nl//4 * 2)
        nc_t1 = int(nc//4 * 4)
        nc_t2 = int(nc//4 * 2)
        Yim_trimmed = [Yim[0], 
                       Yim[1][:nl_t1,:nc_t1], 
                       Yim[2][:nl_t1,:nc_t1], 
                       Yim[3][:nl_t1,:nc_t1], 
                       Yim[4][:nl_t2,:nc_t2], 
                       Yim[5][:nl_t2,:nc_t2], 
                       Yim[6][:nl_t2,:nc_t2], 
                       Yim[7][:nl_t1,:nc_t1], 
                       Yim[8][:nl_t2,:nc_t2], 
                       Yim[9], 
                       Yim[10][:nl_t2,:nc_t2], 
                       Yim[11][:nl_t2,:nc_t2]]
        YimD = rr_s2_data(Yim_trimmed, trim=False)
        XfD = np.moveaxis(np.array([Yim_D[i] for i,v in enumerate(d) if v == 1]),[0,1,2],[2,0,1])
        XcD = np.moveaxis(np.array([Yim_D[i] for i,v in enumerate(d) if v == 2]),[0,1,2],[2,0,1])

        XcU=rescale(Xc, 2, order=0, anti_aliasing=False, preserve_range=True, multichannel=True)
        XcDU=rescale(Xc_D, 2, order=0, anti_aliasing=False, preserve_range=True, multichannel=True)
        X=Xc[:nl_t2,:nc_t2,:]

    else:
        XfD=resize(Xf,[round(Xf.shape[0]/2),round(Xf.shape[1]/2),Xf.shape[2]])
        XcD=resize(Xc,[round(Xc.shape[0]/2),round(Xc.shape[1]/2),Xc.shape[2]])
        XcU=resize(Xc,[Xf.shape[0],Xf.shape[1],Xc.shape[2]])
        XcDU=resize(XcD,[XfD.shape[0],XfD.shape[1],Xc.shape[2]])
        X=Xc

    y=np.concatenate([XcDU,XfD], axis=-1)
    y_test=np.concatenate([XcU,Xf], axis=-1)
    
    scale=np.max(X)
    x=X/scale
    y=y/scale #input
    y_test=y_test/scale
    
    Y=GenerateCube(y,stride=8) #input
    X=GenerateCube(x,stride=8) #target
    Yt=y.reshape(-1,y.shape[0],y.shape[1],y.shape[2])
    Xt=x.reshape(-1,x.shape[0],x.shape[1],x.shape[2])

    netname="skipnet"
    mymodel=skip(ndown=ndown)
    myoptimizer=tf.keras.optimizers.Adam(learning_rate=lr)
    mymodel.compile(optimizer=myoptimizer, loss="mse")
        
    modelpath=netname+"bestmodel.hdf5"
    checkpoint = ModelCheckpoint(modelpath, monitor='val_loss', verbose=verbose, save_best_only=True)
    callbacks_list = [checkpoint]

    h=mymodel.fit(x=Y,y=X,batch_size=batch_size,epochs=num_epochs,
                  validation_data=(Yt,Xt),callbacks=callbacks_list, 
                  verbose=verbose)
    bestmodel=tf.keras.models.load_model(modelpath)

    Ypr=bestmodel.predict(y_test.reshape(-1,y_test.shape[0],y_test.shape[1],y_test.shape[2]), verbose=verbose)
    
    Ypr=np.squeeze(Ypr*scale)
    Yhat[:,:,np.nonzero(np.array([2])[:, None] == d)[1]] = Ypr
    
    tf.keras.backend.clear_session()
    
    return np.squeeze(Yhat)

def SSCwrapNew(Yim, d=[6,1,1,1,2,2,2,1,2,6,2,2], batch_size = 64, lr=0.0005, ndown=3, num_epochs = 500, mtf=[ .32, .26, .28, .24, .38, .34, .34, .26, .33, .26, .22, .23], verbose=True):
    tf.keras.backend.clear_session()

    Xf = np.moveaxis(np.array([Yim[i] for i,v in enumerate(d) if v == 1]),[0,1,2],[2,0,1])
    Xc = np.moveaxis(np.array([Yim[i] for i,v in enumerate(d) if v == 2]),[0,1,2],[2,0,1])
    (nl,nc,nb1) = Xf.shape
    
    Yhat = np.zeros((nl,nc,len(d)))*np.nan

    nl_t1 = int(nl//4 * 4)
    nl_t2 = int(nl//4 * 2)
    nc_t1 = int(nc//4 * 4)
    nc_t2 = int(nc//4 * 2)
    Yim_trimmed = [Yim[0], 
                Yim[1][:nl_t1,:nc_t1], 
                Yim[2][:nl_t1,:nc_t1], 
                Yim[3][:nl_t1,:nc_t1], 
                Yim[4][:nl_t2,:nc_t2], 
                Yim[5][:nl_t2,:nc_t2], 
                Yim[6][:nl_t2,:nc_t2], 
                Yim[7][:nl_t1,:nc_t1], 
                Yim[8][:nl_t2,:nc_t2], 
                Yim[9], 
                Yim[10][:nl_t2,:nc_t2], 
                Yim[11][:nl_t2,:nc_t2]]
    
    Yim_D = rr_s2_data(Yim_trimmed, trim=False)
    Xf_D = np.moveaxis(np.array([Yim_D[i] for i,v in enumerate(d) if v == 1]),[0,1,2],[2,0,1])
    Xc_D = np.moveaxis(np.array([Yim_D[i] for i,v in enumerate(d) if v == 2]),[0,1,2],[2,0,1])
            
    Xc_U=rescale(Xc, 2, order=0, anti_aliasing=False, preserve_range=True, multichannel=True)
    Xc_DU=rescale(Xc_D, 2, order=0, anti_aliasing=False, preserve_range=True, multichannel=True)
    
    X=Xc[:nl_t2,:nc_t2,:]
    
    y=np.concatenate([Xc_DU,Xf_D], axis=-1)
    y_test=np.concatenate([Xc_U,Xf], axis=-1)
    
    scale=np.max(X)
    x=X/scale
    y=y/scale #input
    y_test=y_test/scale
    
    Y=GenerateCube(y,stride=8) #input
    X=GenerateCube(x,stride=8) #target
    Yt=y.reshape(-1,y.shape[0],y.shape[1],y.shape[2])
    Xt=x.reshape(-1,x.shape[0],x.shape[1],x.shape[2])

    netname="skipnet"
    mymodel=skip(ndown=ndown)
    myoptimizer=tf.keras.optimizers.Adam(learning_rate=lr)
    mymodel.compile(optimizer=myoptimizer, loss="mse")
        
    modelpath=netname+"bestmodel.hdf5"
    checkpoint = ModelCheckpoint(modelpath, monitor='val_loss', verbose=verbose, save_best_only=True)
    callbacks_list = [checkpoint]

    h=mymodel.fit(x=Y,y=X,batch_size=batch_size,epochs=num_epochs,
                  validation_data=(Yt,Xt),callbacks=callbacks_list, 
                  verbose=verbose)
    bestmodel=tf.keras.models.load_model(modelpath)

    Ypr=bestmodel.predict(y_test.reshape(-1,y_test.shape[0],y_test.shape[1],y_test.shape[2]), verbose=verbose)
    
    Ypr=np.squeeze(Ypr*scale)
    Yhat[:,:,np.nonzero(np.array([2])[:, None] == d)[1]] = Ypr
    
    tf.keras.backend.clear_session()
    
    return np.squeeze(Yhat)