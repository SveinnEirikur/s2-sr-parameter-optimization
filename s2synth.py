import numpy as np


def gaussian_filter(N=3,sigma=0.5):
    n = (N-1)/2.0
    y,x = np.ogrid[-n:n+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2*sigma**2) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def create_conv_kernel(sdf, nl, nc, d=[6, 1, 1, 1, 2, 2, 2, 1, 2, 6, 2, 2], N=12):
    middlel = nl//2
    middlec = nc//2
    L = len(d)
    B = np.zeros([L,nl, nc])
    for i in range(L):
        if d[i] == 1:
            B[i,0,0] = 1
            FBM = np.fft.fft2(B)
        else:
            h = gaussian_filter(N,sdf[i])
            #B[i, int(nl%2+1+(nl - N-d[i])//2):int(nl%2+1+(nl + N-d[i])//2), int(nc%2+1+(nc - N-d[i])//2):int(nc%2+1+(nc + N-d[i])//2)] = h
            B[i, int(nl%2+(nl - N)//2):int(nl%2+(nl + N)//2), int(nc%2+(nc - N)//2):int(nc%2+(nc + N)//2)] = h 
            
            B[i,:,:] = np.fft.fftshift(B[i,:,:])
            B[i,:,:] = np.divide(B[i,:,:],np.sum(B[i,:,:]))
            FBM = np.fft.fft2(B)

    return  FBM

def rr_s2_data(Yim, ratio = 2, 
               mtf = [ .32, .26, .28, .24, .38, .34, .34, .26, .33, .26, .22, .23],
               d = np.array([6, 1, 1, 1, 2, 2, 2, 1, 2, 6, 2, 2]), trim=True):

    Yim_c = np.array(Yim)

    idx1 = np.nonzero(np.array([1])[:, None] == d)[1]
    nl1,nc1 = Yim[idx1[0]].shape
    
    idx2 = np.nonzero(np.array([2])[:, None] == d)[1]
    nl2,nc2 = Yim[idx2[0]].shape
    
    idx6 = np.nonzero(np.array([6])[:, None] == d)[1]
    nl6,nc6 = Yim[idx6[0]].shape

    l_trim1_l = int(6 * (np.floor(nl6 % 6/2))) if trim else 0
    l_trim1_r = int(6 * np.ceil(nl6 % 6/2)) if trim else 0
    c_trim1_l = int(6 * (np.floor(nc6 % 6/2))) if trim else 0
    c_trim1_r = int(6 * np.ceil(nc6 % 6/2)) if trim else 0
        
    l_trim2_l = l_trim1_l // 2
    l_trim2_r = l_trim1_r // 2
    c_trim2_l = c_trim1_l // 2
    c_trim2_r = c_trim1_r // 2
    l_trim6_l = l_trim1_l // 6
    l_trim6_r = l_trim1_r // 6
    c_trim6_l = c_trim1_l // 6
    c_trim6_r = c_trim1_r // 6
    
    sdf = ratio*np.sqrt(-2*np.log(mtf)/np.pi**2)

    nl1 = int(nl1 - l_trim1_r - l_trim1_l)
    nc1 = int(nc1 - c_trim1_r - c_trim1_l)
    d1 = ratio*d[idx1]/1
    fbm1 = create_conv_kernel(sdf[idx1], nl1, nc1, d1)
    
    nl2 = int(nl2 - l_trim2_r - l_trim2_l)
    nc2 = int(nc2 - c_trim2_r - c_trim2_l)
    d2 = ratio*d[idx2]/2
    fbm2 = create_conv_kernel(sdf[idx2], nl2, nc2, d2)

    nl6 = int(nl6 - l_trim6_r - l_trim6_l)
    nc6 = int(nc6 - c_trim6_r - c_trim6_l)
    d6 = ratio*d[idx6]/6
    fbm6 = create_conv_kernel(sdf[idx6], nl6, nc6, d6)

    Yim_rr = np.empty((len(mtf),))
    Yim_rr1 = np.real(np.fft.ifft2(np.fft.fft2(np.stack(Yim_c[idx1])[:,l_trim1_l:None if l_trim1_r == 0 else -l_trim1_r,c_trim1_l:None if c_trim1_r == 0 else -c_trim1_r])*fbm1))
    Yim_rr2 = np.real(np.fft.ifft2(np.fft.fft2(np.stack(Yim_c[idx2])[:,l_trim2_l:None if l_trim2_r == 0 else -l_trim2_r,c_trim2_l:None if c_trim2_r == 0 else -c_trim2_r])*fbm2))
    Yim_rr6 = np.real(np.fft.ifft2(np.fft.fft2(np.stack(Yim_c[idx6])[:,l_trim6_l:None if l_trim6_r == 0 else -l_trim6_r,c_trim6_l:None if c_trim6_r == 0 else -c_trim6_r])*fbm6))
    
    Yim_rr = {}
    for i in range(len(d)):
        if i in idx1:
            Yim_rr[i] = Yim_rr1[np.where(idx1==i),::ratio,::ratio]
        if i in idx2:
            Yim_rr[i] = Yim_rr2[np.where(idx2==i),::ratio,::ratio]
        if i in idx6:
            Yim_rr[i] = Yim_rr6[np.where(idx6==i),::ratio,::ratio]

    return [np.squeeze(Yim_rr[key]) for key in Yim_rr.keys()]
    
def mod_6_crop_s2_data(Yim, d = np.array([6, 1, 1, 1, 2, 2, 2, 1, 2, 6, 2, 2])):
    Yim_c = np.array(Yim)

    nl1,nc1 = Yim[d.tolist().index(1)].shape
    nl2,nc2 = Yim[d.tolist().index(2)].shape
    nl6,nc6 = Yim[d.tolist().index(6)].shape
        
    l_trim1_l = int(6 * (np.floor(nl6 % 6/2)))
    l_trim1_r = int(6 * np.ceil(nl6 % 6/2))
    c_trim1_l = int(6 * (np.floor(nc6 % 6/2)))
    c_trim1_r = int(6 * np.ceil(nc6 % 6/2))
    l_trim2_l = l_trim1_l // 2
    l_trim2_r = l_trim1_r // 2
    c_trim2_l = c_trim1_l // 2
    c_trim2_r = c_trim1_r // 2
    l_trim6_l = l_trim1_l // 6
    l_trim6_r = l_trim1_r // 6
    c_trim6_l = c_trim1_l // 6
    c_trim6_r = c_trim1_r // 6
    
    Yim_cc = {}
    for i in range(len(d)):
        if d[i] == 1:
            Yim_cc[i] = Yim_c[i][l_trim1_l:None if l_trim1_r == 0 else -l_trim1_r,c_trim1_l:None if c_trim1_r == 0 else -c_trim1_r]
        elif d[i] == 2:
            Yim_cc[i] = Yim_c[i][l_trim2_l:None if l_trim2_r == 0 else -l_trim2_r,c_trim2_l:None if c_trim2_r == 0 else -c_trim2_r]
        elif d[i] == 6:
            Yim_cc[i] = Yim_c[i][l_trim6_l:None if l_trim6_r == 0 else -l_trim6_r,c_trim6_l:None if c_trim6_r == 0 else -c_trim6_r]

    return [np.squeeze(Yim_cc[key]) for key in Yim_cc.keys()]
        
def pad_to_size(Yim, pad_size=(432, 432), band_scales=np.array([6, 1, 1, 1, 2, 2, 2, 1, 2, 6, 2, 2])):
    padding = np.maximum(np.subtract(pad_size, Yim[1].shape),0)//6 * 3
    Ypad = np.copy(Yim)
    
    if any(padding > 0):
        for idx in range(len(band_scales)):
            Ypad[idx] = np.pad(Ypad[idx],((padding[0], padding[0])//band_scales[idx], (padding[1], padding[1])//band_scales[idx]),'reflect')
            
    return Ypad, padding

def unpad_from_size(Xpad, padding=(0, 0)):
    Xim = np.copy(Xpad)
    
    if padding[0] > 0:
        Xim = Xim[padding[0]:-padding[0],:,:]
    if padding[1] > 0:
        Xim = Xim[:,padding[1]:-padding[1],:]
            
    return Xim
