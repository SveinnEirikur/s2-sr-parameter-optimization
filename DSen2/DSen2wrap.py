import numpy as np
from tensorflow.keras import backend as K
from DSen2.testing.supres import DSen2_60, DSen2_20

def DSen2wrap(Yim, band_scales=[6,1,1,1,2,2,2,1,2,6,2,2], mtf=None, verbose=False):
    d60 = np.moveaxis(np.array([Yim[i] for i,v in enumerate(band_scales) if v == 6]),[0,1,2],[2,0,1])
    d20 = np.moveaxis(np.array([Yim[i] for i,v in enumerate(band_scales) if v == 2]),[0,1,2],[2,0,1])
    d10 = np.moveaxis(np.array([Yim[i] for i,v in enumerate(band_scales) if v == 1]),[0,1,2],[2,0,1])
    
    (nl,nc,nb1) = d10.shape
    
    pad_size = [0,0]
    if d10.shape[1]<192:
        pad_size[1] = (192-d10.shape[1])//2
        d10=np.pad(d10,((0,0),(pad_size[1],pad_size[1]),(0,0)),'reflect')
        d20=np.pad(d20,((0,0),(pad_size[1]//2,pad_size[1]//2),(0,0)),'reflect')
        d60=np.pad(d60,((0,0),(pad_size[1]//6,pad_size[1]//6),(0,0)),'reflect')
    if d10.shape[0]<192:
        pad_size[0] = (192-d10.shape[2])//2
        d10=np.pad(d10,((pad_size[0],pad_size[0]), (0,0), (0,0)),'reflect')
        d20=np.pad(d20,((pad_size[0]//2,pad_size[0]//2), (0,0), (0,0)),'reflect')
        d60=np.pad(d60,((pad_size[0]//6,pad_size[0]//6), (0,0), (0,0)),'reflect')
    
    K.clear_session()

    if verbose: print('Processing 60 m bands')
    sr60 = DSen2_60(d10, d20, d60, deep=False)
    
    K.clear_session()

    if verbose: print('Processing 20 m bands')
    sr20 = DSen2_20(d10, d20, deep=False)
    
    K.clear_session()

    if pad_size[0] > 0:
        d10 = d10[pad_size[0]:-pad_size[0],:,:]
        sr20 = sr20[pad_size[0]:-pad_size[0],:,:]
        sr60 = sr60[pad_size[0]:-pad_size[0],:,:]
    if pad_size[1] > 0:
        d10 = d10[:,pad_size[1]:-pad_size[1],:]
        sr20 = sr20[:,pad_size[1]:-pad_size[1],:]
        sr60 = sr60[:,pad_size[1]:-pad_size[1],:]

    Xhat = np.zeros((nl,nc,len(band_scales)))*np.nan
    Xhat[:,:,np.nonzero(np.array([1])[:, None] == band_scales)[1]] = d10
    Xhat[:,:,np.nonzero(np.array([2])[:, None] == band_scales)[1]] = sr20
    Xhat[:,:,np.nonzero(np.array([6])[:, None] == band_scales)[1]] = sr60
    
    return Xhat