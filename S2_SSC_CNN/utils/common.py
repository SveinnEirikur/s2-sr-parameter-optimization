import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import tensorflow as tf

def GenerateCube(X,size=16, stride=4):
    """Create hsi cube patches from single cube X
    input: X is his cube
           stride is number that each small cube strides
           size is the cube size, i.e. size x size x size
    output: HSI cubes"""
    (row,col,dep) = X.shape
    cube=[]
    for r in range(0,row-size+1,stride):
        for c in range(0,col-size+1,stride):
            patch = X[r:r+size,c:c+size,:]
            cube.append(patch)

    return np.asarray(cube)

def sreCal(Xref,X):
    '''Calculate signal to reconstructed error (SRE) between reference image and reconstructed image
    Input: Xref, X: reference and reconstructed images in shape [h,w,d]
    Output: aSRE average SRE in dB
            SRE_vec: SRE of each band'''
    mSRE=0
    if len(Xref.shape)==3:
        Xref=Xref.reshape(Xref.shape[0]*Xref.shape[1],Xref.shape[2])
        X=X.reshape(X.shape[0]*X.shape[1],X.shape[2])
        SRE_vec=np.zeros((X.shape[1]))
        for i in range(X.shape[1]):
            SRE_vec[i]=10*np.log(np.sum(Xref[:,i]**2)/np.sum((Xref[:,i]-X[:,i])**2))/np.log(10)
        mSRE=np.mean(SRE_vec)
    else:
        pass
    return mSRE,SRE_vec

def PSNR(img1, img2):
    """"Calculating peak signal-to-noise ratio (PSNR) between two images."""
    max_value=np.max(img1)
    mse = np.mean((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32)) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(max_value / (np.sqrt(mse)))
