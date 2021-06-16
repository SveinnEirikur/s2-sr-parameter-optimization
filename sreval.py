import numpy as np
from skimage.metrics import structural_similarity
from scipy.signal import convolve2d

### Performance Measures

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Universal Image Quality Index (UIQI).
#
# Interface:
#           q_index, q_map = uiqi(im1,im2,ratio)
#
# Inputs:
#           im1:            First multispectral image (ground truth);
#           im2:            Second multispectral image;
#           block_size:     Size of filter to use
#                           Pre-condition: Integer value.
#           return_map:     Whether to return the quality map
#
# Outputs:
#           q_index:        Universal image quality index.
#           q_map:          Universal image quality index map.
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def uiqi(im1, im2, block_size=8, return_map=False):
    if len(im1.shape)==3:
        return np.array([uiqi(im1[:,:,i], im2[:,:,i], block_size, return_map=return_map) for i in range(im1.shape[2])])

    N = block_size**2
    filter_window = np.ones((block_size, block_size))

    im1_sq = np.square(im1)
    im2_sq = np.square(im2)
    im1_im2 = im1*im2

    im1_sum = convolve2d(im1, filter_window, mode='valid')
    im2_sum =  convolve2d(im2, filter_window, mode='valid')
    im1_sq_sum = convolve2d(im1_sq, filter_window, mode='valid')
    im2_sq_sum = convolve2d(im2_sq, filter_window, mode='valid')
    im12_sum = convolve2d(im1_im2, filter_window, mode='valid')

    im12_sum_mul = im1_sum*im2_sum
    im12_sum_sq_sum_mul = np.square(im1_sum) + np.square(im2_sum)

    numerator = 4*(N*im12_sum - im12_sum_mul)*im12_sum_mul
    denominator1 = N*(im1_sq_sum + im2_sq_sum) - im12_sum_sq_sum_mul
    denominator = denominator1*im12_sum_sq_sum_mul

    q_map = np.ones(denominator.shape)
    index = np.logical_and((denominator1 == 0) , (im12_sum_sq_sum_mul != 0))
    q_map[index] = 2*im12_sum_mul[index]/im12_sum_sq_sum_mul[index]
    index = (denominator != 0)
    q_map[index] = numerator[index]/denominator[index]

    if return_map:
        return np.mean(q_map), q_map
    else:
        return np.mean(q_map)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Structural Similarity Index Measure (SSIM).
#           Calculated using structural_similarity() from Scikit-Image.
#           Tuned to match matlabs ssim() function to three digits.
#
# Interface:
#           ssim_index, assim = ssim(im1,im2)
#
# Inputs:
#           im1:         First multispectral image;
#           im2:         Second multispectral image.
#
# Outputs:
#           ssim:       Per band Structural Similarity Index Measure.
#           assim:      Average Structural Similarity Index Measure.
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def ssim(im1, im2, sigma = 1.5, data_range=1.0, return_mean=True):
    ssim_index = np.zeros(im2.shape[-1])
    for ch in range(im2.shape[-1]):
        ssim_map = structural_similarity(im1[:,:,ch], im2[:,:,ch],
                                        multichannel=False,
                                        gaussian_weights=True,
                                        sigma=sigma,
                                        use_sample_covariance=True,
                                        data_range=data_range,
                                        full=True)[1]
        ssim_index[ch] = np.nanmean(ssim_map)
    if return_mean:
        return ssim_index, ssim_index.mean()
    else:
        return ssim_index

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Signal-to-Reconstruction Error (SRE).
#
# Interface:
#           rmse = sre(im1,im2)
#
# Inputs:
#           im1:         First multispectral image;
#           im2:         Second multispectral image.
#
# Outputs:
#           sre:       Signal-to-Reconstruction Error (dB);
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def sre(im1,im2):
    diff = im2-im1
    z = np.where(diff==0)
    diff[z] = np.finfo(im2.dtype).eps
    SRE = 10*np.log10(np.sum(im1**2, axis=(0,1)) / np.sum(diff**2, axis=(0,1)))
    return SRE

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Root Mean Square Error (RMSE).
#
# Interface:
#           rmse = RMSE(im1,im2)
#
# Inputs:
#           im1:         First multispectral image;
#           im2:         Second multispectral image.
#
# Outputs:
#           rmse:       Root mean square error;
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def rmse(im1,im2):
    im1 = im1.reshape(-1,im1.shape[-1])
    im2 = im2.reshape(-1,im1.shape[-1])
    RMSE = np.linalg.norm(im1 - im2)/np.sqrt(im2.size)
    return RMSE

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Spectral Angle Mapper (SAM).
#
# Interface:
#           [sam_index,sam_map] = sam(im1,im2)
#
# Inputs:
#           im1:         First multispectral image;
#           im2:         Second multispectral image.
#
# Outputs:
#           sam_index:  SAM index;
#           sam_map:    Image of SAM values.
#
# References:
#           [Yuhas92]   R. H. Yuhas, A. F. H. Goetz, and J. W. Boardman, "Discrimination among semi-arid landscape endmembers using the Spectral Angle Mapper (SAM) algorithm,"
#                       in Proceeding Summaries 3rd Annual JPL Airborne Geoscience Workshop, 1992, pp. 147-149.
#           [Vivone14]  G. Vivone, L. Alparone, J. Chanussot, M. Dalla Mura, A. Garzelli, G. Licciardi, R. Restaino, and L. Wald, "A Critical Comparison Among Pansharpening Algorithms",
#                       IEEE Transaction on Geoscience and Remote Sensing, 2014. (Accepted)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def sam(im1,im2, return_map=False):
    prod_scal = np.einsum('ijk,ijk->ij', im1, im2)
    norm_orig = np.einsum('ijk,ijk->ij', im1, im1)
    norm_fusa = np.einsum('ijk,ijk->ij', im2, im2)

    prod_norm = np.sqrt(norm_orig*norm_fusa)
    prod_map = prod_norm
    z = np.where(prod_norm==0)
    prod_map[z] = np.finfo(im2.dtype).eps
    sam_map = np.arccos(np.divide(prod_scal,prod_map))

    prod_scal = np.delete(prod_scal,z).flatten()
    prod_norm = np.delete(prod_norm,z).flatten()
    ang = np.sum(np.arccos(prod_scal/prod_norm))/prod_norm.shape[0]
    sam_index = np.nan_to_num(ang)*180/np.pi

    if return_map:
        return sam_index, sam_map
    else:
        return sam_index


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Erreur Relative Globale Adimensionnelle de Synthèse (ERGAS).
#
# Interface:
#           ergas_index = ergas(im1,im2,ratio)
#
# Inputs:
#           im1:             First multispectral image;
#           im2:             Second multispectral image;
#           ratio:           Scale ratio between MS and PAN.
#                            Pre-condition: Integer value.
#
# Outputs:
#           ergas_index:    ERGAS index.
# References:
#           [Ranchin00]     T. Ranchin and L. Wald, "Fusion of high spatial and spectral resolution images: the ARSIS concept and its implementation,"
#                           Photogrammetric Engineering and Remote Sensing, vol. 66, no. 1, pp. 49-61, January 2000.
#           [Vivone14]      G. Vivone, L. Alparone, J. Chanussot, M. Dalla Mura, A. Garzelli, G. Licciardi, R. Restaino, and L. Wald, "A Critical Comparison Among Pansharpening Algorithms",
#                           IEEE Transaction on Geoscience and Remote Sensing, 2014. (Accepted)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def ergas(im1, im2, ratio):
    im1 = np.double(im1)
    im2 = np.double(im2)

    err = im1-im2
    ergas_index = np.divide(np.mean(np.square(err), axis=(0,1)),np.mean(im1, axis=(0,1))**2)
    ergas_index = (100/ratio) * np.sqrt((1/err.shape[-1]) * np.sum(ergas_index))

    return ergas_index

### Helper functions

def normalise_data(im, return_av=True):
    im = np.squeeze(im)
    if len(im.shape) == 1:
        y_im = []
        av = []
        for b in im:
            av.append(np.mean(np.square(b), axis=(0,1)))
            y_im.append(np.sqrt(np.square(b)/av[-1]))
        if return_av:
            return np.array(y_im), np.array(av)
        else:
            return np.array(y_im)
    else:
        av = np.mean(np.square(im), axis=(0,1))
        y_im = np.sqrt(np.square(im)/av)
        if return_av:
            return y_im, av
        else:
            return y_im

def unnormalise_data(im, av):
    im = np.squeeze(im)
    if len(im.shape) == 1:
        y_im = []
        for b, a in zip(im,av):
            y_im.append(np.sqrt(np.square(b)*a))
        return np.array(y_im)
    else:
        y_im = np.sqrt(np.square(im)*av)
        return y_im

def dataframe_from_res_list(res_list, method_names, band_names, multi_run=False):
    import pandas as pd
    res_dict = {method: result for method, result in zip(method_names, res_list)}
    reform = {}
    for outer_k, outer_v in res_dict.items():
        for inner_k, inner_v in outer_v.items():
            for innest_k, innest_v in inner_v.items():
                if innest_k == 'Bands':
                    for b, idx in band_names.items():
                        if multi_run == True:
                            reform[(outer_k, inner_k, b, 'Average')] = innest_v['Average'][idx]
                            reform[(outer_k, inner_k, b, 'STD')] = innest_v['STD'][idx]
                        else:
                            reform[(outer_k, inner_k, b)] = innest_v[idx]
                else:
                    if multi_run == True:
                        reform[(outer_k, inner_k, innest_k, 'Average')] = innest_v['Average']
                        reform[(outer_k, inner_k, innest_k, 'STD')] = innest_v['STD']
                    else:
                        reform[(outer_k, inner_k, innest_k)] = innest_v
    srevals_df = pd.DataFrame(reform, index=[0]).T.unstack(level=0)[0].sort_index()
    return srevals_df

### Main functions

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Evalute Super Resolution for single multiband image
#
# Interface:
#           SSIM, SRE, RMSE, ERGAS, SAM = sreval(Xm_im, Xhat_im, limsub, ...
#                                                   data_range, d, bands)
#
# Inputs:
#           Xm_im:          Ground truth image;
#           Xhat_im:        Estimated image or list of images;
#           limsub:         Number of edge pixels to ignore;
#           data_range:     Dynamic range of images;
#           d:              Scale of image bands;
#           bands:          Scales to evaluate.
#
# Outputs:
#           SSIM:           Structural Similarity Index Measure
#           SRE:            Signal-to-Reconstruction Error
#           ERGAS:          Erreur Relative Globale Adimensionnelle de Synthèse
#           SAM:            Spectral Angle Mapper
#
#                           Each result is a dictionarie containing scores for
#                           different bands and/or scales with keywords:
#                           '20m', '30m', 'All', and/or 'Bands' as applicable.
#                           If the input is a list of images the returned
#                           values are average and standard deviation accross
#                           the inner list.
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def evaluate_performance(Xm_im, Xhat_im, limsub=0, data_range=1.0, d=[6, 1, 1, 1, 2, 2, 2, 1, 2, 6, 2, 2], bands=[2,6]):
    try:
        Xhat_im.shape
        average = False
    except:
        average = True

    if average:
        SSIM = {'20m': [], '60m': [], 'All': [], 'Bands': []}
        SRE = {'20m': [], '60m': [], 'All': [], 'Bands': []}
        UIQI = {'20m': [], '60m': [], 'All': [], 'Bands': []}
        RMSE = {'20m': [], '60m': [], 'All': []}
        ERGAS = {'20m': [], '60m': []}
        SAM = {'20m': [], 'All': []}
        metrics = [SSIM, SRE, RMSE, ERGAS, SAM, UIQI]

        for k in range(len(Xhat_im)):
            res = evaluate_performance(Xm_im, Xhat_im[k], limsub=limsub, data_range=data_range, bands=bands)
            for metric, result in zip(metrics, res):
                for key, value in result.items():
                    metric[key].append(value)
        for metric in metrics:
            for key, value in metric.items():
                if key == 'Bands':
                    metric[key] = {'Average': np.mean(np.array(value),axis=0), 'STD': np.std(np.array(value),axis=0)}
                else:
                    metric[key] = {'Average': np.mean(value), 'STD':np.std(value)}
        return metrics

    else:
        X = Xm_im[limsub:-max(limsub,1), limsub:-max(limsub,1), :]
        Xhat = Xhat_im[limsub:-max(limsub,1), limsub:-max(limsub,1), :]
        d = np.array(d)
        idx = np.nonzero(np.array(bands)[:, None] == d)[1]
        

        ERGAS = {}
        RMSE = {}
        SAM = {}
        SRE = {}
        SSIM = {}
        UIQI = {}

        SSIM['Bands'] = np.ones(len(d))*np.nan
        SSIM['Bands'][idx], SSIM['All'] = ssim(X[:,:,idx], Xhat[:,:,idx])

        SRE['Bands'] = np.ones(len(d))*np.nan
        SRE['Bands'][idx] = sre(X[:,:,idx], Xhat[:,:,idx])

        UIQI['Bands'] = np.ones(len(d))*np.nan
        UIQI['Bands'][idx] = uiqi(X[:,:,idx], Xhat[:,:,idx])

        if 2 in bands:
            idx2 = np.squeeze(np.where(d == 2))
            ERGAS['20m'] = ergas(X[:,:,idx2], Xhat[:,:,idx2], 2)
            RMSE['20m'] = rmse(X[:,:,idx2], Xhat[:,:,idx2])
            SAM['20m'] = sam(X[:,:,idx2], Xhat[:,:,idx2])
            SSIM['20m'] = SSIM['Bands'][idx2].mean()
            SRE['20m'] = SRE['Bands'][idx2].mean()
            UIQI['20m'] = UIQI['Bands'][idx2].mean()

        if 6 in bands:
            idx6 = np.squeeze(np.where(d == 6))
            ERGAS['60m'] = ergas(X[:,:,idx6], Xhat[:,:,idx6],6)
            RMSE['60m'] = rmse(X[:,:,idx6], Xhat[:,:,idx6])
            SSIM['60m'] = SSIM['Bands'][idx6].mean()
            SRE['60m'] = SRE['Bands'][idx6].mean()
            UIQI['60m'] = UIQI['Bands'][idx6].mean()

        if 6 in bands and 2 in bands:
            RMSE['All'] = rmse(X[:,:,idx], Xhat[:,:,idx])
            SAM['All'] = sam(X[:,:,idx], Xhat[:,:,idx])
            SRE['All'] = SRE['Bands'][idx].mean()
            UIQI['All'] = UIQI['Bands'][idx].mean()

        return SSIM, SRE, RMSE, ERGAS, SAM, UIQI

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Description:
#           Evalute Super Resolution for multiple multiband images
#
# Interface:
#           res_list = sreval(Xm_im, Xhat_ims, limsub, data_range, d, bands)
#
# Inputs:
#           Xm_im:          Ground truth image;
#           Xhat_ims:       List of (lists of) estimated images;
#           limsub:         Number of edge pixels to ignore;
#           data_range:     Dynamic range of images;
#           d:              Scale of image bands;
#           bands:          Scales to evaluate
#
# Outputs:
#           res_list:       List of dictionaries containing results for each
#                           image (or list of) images.
#                           Dictionaries include SSIM, SRE, ERGAS, SAM and UIQI
#                           scores for the bands chosen.
#                           If list of lists the returned values are average
#                           and standard deviation accross the inner list.
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def sreval(Xm_im, Xhat_ims, limsub=0, data_range=1.0,
           d=[6, 1, 1, 1, 2, 2, 2, 1, 2, 6, 2, 2], bands=[2,6]):
    try:
        Xhat_ims.shape
        Xhat_ims = [Xhat_ims]
    except:
        pass
    res_list = [{} for i in range(len(Xhat_ims))]
    for res_dict, Xhat in zip(res_list, Xhat_ims):
        res_dict['SSIM'], res_dict['SRE'], res_dict['RMSE'], res_dict['ERGAS'], res_dict['SAM'], res_dict['UIQI'] = evaluate_performance(Xm_im, Xhat, limsub=limsub, data_range=data_range, d=d, bands=bands)
    return res_list
