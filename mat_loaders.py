import numpy as np
import scipy.io as spio
import h5py

# Helper function to load Matlab cell arrays
def load_matlab_cell_array(filepath, var_name, verbose=False):
    v = None
    try:
        with h5py.File(filepath, 'r') as matfile:
            v = matfile[var_name][()][0]
            v = [np.transpose(matfile[r][()]) for r in v]
            if verbose: print("Loaded hdf5 file")
    except:
        mat = spio.loadmat(filepath)
        v = mat[var_name]
        v = [r[0] for r in v]
        if verbose: print("Loaded mat file")
    finally:
        assert v is not None
        return v

# Helper function to load Matlab arrays
def load_matlab_array(filepath, var_name, verbose=False):
    v = None
    try:
        with h5py.File(filepath, 'r') as matfile:
            try:
                v = np.transpose(matfile[var_name][()],(2,1,0))
            except:
                v = np.transpose(matfile[var_name][()],(1,0))
            if verbose: print("Loaded hdf5 file")
    except:
        mat = spio.loadmat(filepath)
        v = mat[var_name]
        if verbose: print("Loaded mat file")
    finally:
        assert v is not None
        return v

# Helper function to load S2 images from mat-files
def get_data(dataset_name, datadir='../data/', verbose=False, rr=False, get_mtf=False):
    Yim = None
    eval_bands = [2,6]
    mtf = [0.34, 0.25, 0.27, 0.25, 0.42, 0.35, 0.35, 0.26, 0.36, 0.25, 0.20, 0.24]

    if dataset_name is 'apex':
        Yim = load_matlab_cell_array(datadir + 'apex.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'apex.mat', 'Xm_im', verbose)
    elif dataset_name is 'aviris':
        Yim = load_matlab_cell_array(datadir + 'aviris.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'aviris.mat', 'imGT', verbose)
    elif dataset_name is 'crops':
        Yim = load_matlab_cell_array(datadir + 'avirisLowCrops.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'avirisLowCrops.mat', 'Xm_im', verbose)
    elif dataset_name is 'coast':
        Yim = load_matlab_cell_array(datadir + 'avirisLowCoast.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'avirisLowCoast.mat', 'Xm_im', verbose)
    elif dataset_name is 'escondido':
        Yim = load_matlab_cell_array(datadir + 'escondido.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'escondido.mat', 'Xm_im', verbose)
    elif dataset_name is 'escondido_s2':
        Yim = load_matlab_cell_array(datadir + 'escondido.mat', 'S2', verbose)
        Xm_im = np.zeros((Yim[1].shape[0], Yim[1].shape[1], len(Yim)))*np.nan
        eval_bands = None
    elif dataset_name is 'mountain':
        Yim = load_matlab_cell_array(datadir + 'avirisLowMontain.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'avirisLowMontain.mat', 'Xm_im', verbose)
    elif dataset_name is 'rkvik':
        Yim = load_matlab_cell_array(datadir + 'rkvik_crop.mat', 'Yim', verbose)
        Xm_im = np.zeros((Yim[1].shape[0], Yim[1].shape[1], len(Yim)))*np.nan
        eval_bands = None
    elif dataset_name is 'rkvik_rr_2':
        Yim = load_matlab_cell_array(datadir + 'rkvik_crop.mat', 'Yim_rr_2', verbose)
        Xm_im = load_matlab_array(datadir + 'rkvik_crop.mat', 'Xm_im', verbose)
        eval_bands = [2]
    elif dataset_name is 'rkvik_rr_6':
        Yim = load_matlab_cell_array(datadir + 'rkvik_crop.mat', 'Yim_rr_6', verbose)
        Xm_im = load_matlab_array(datadir + 'rkvik_crop.mat', 'Xm_im', verbose)
        eval_bands = [6]
    elif dataset_name is 'urban':
        Yim = load_matlab_cell_array(datadir + 'avirisLowCity.mat', 'Yim', verbose)
        Xm_im = load_matlab_array(datadir + 'avirisLowCity.mat', 'Xm_im', verbose)

    if Yim is None:
        raise Exception("Unknown dataset: " + dataset_name)

    if rr:
        from s2synth import rr_s2_data
        Xm_im = Yim
        Yim = rr_s2_data(Xm_im, ratio=rr)
        eval_bands = [rr]

    if get_mtf:
        return (Yim, mtf, Xm_im, eval_bands)

    return (Yim, Xm_im, eval_bands)
