# S2 Super-Resolution Parameter Optimization

Parameter optimization for Sentinel-2 supe-resolution methods

Code to accompany:

Armannsson, S.E.; Ulfarsson, M.O.; Sigurdsson, J.; Nguyen, H.V.; Sveinsson, J.R. A Comparison of Optimized Sentinel-2 Super-Resolution Methods Using Wald’s Protocol and Bayesian Optimization. Remote Sens. 2021, 13, 2192. <https://doi.org/10.3390/rs13112192>

Please reference the above paper if you use this code, available from <https://www.mdpi.com/2072-4292/13/11/2192>.

## Installation

To use the code clone the repository to a suitable location and install the requirements from `requirements.txt`.
The code for S2Sharp and S2 SSC is included and wrapper functions are included for ATPRK, DSen2, MuSA, SSSS, and SupReME.
To use the wrappers the appropriate code must be installed to the corresponding directories alongside the wrappers.

- ATPRK: <https://github.com/qunmingwang/Code-for-S2-fusion>
- DSen2: <https://github.com/lanha/DSen2>
- SSSS: <https://sites.google.com/view/chiahsianglin/software>
- SupReME: <https://github.com/lanha/SupReME>

Functions for loading and processing data and evaluating results are included in `mat_loaders.py`, `s2synt.py` and `sreval.py`.

### Requirements

```
python==3.7
h5py==2.10.0
hyperopt==0.2.5
jupyter==1.0.0
matlabengineforpython==R2020a
matplotlib==3.3.4
numpy==1.19.5
pandas==1.1.1
pytables==3.6.1
scikit-image==0.18.1
scipy==1.5.2
seaborn==0.11.1
tensorflow-gpu==2.4.2
tqdm==4.59.0
```

The packages listed should be available using PyPI and/or Conda with the exception of the Matlab engine for Python which should be installed according to the instructions found on the Mathworks website <https://mathworks.com/help/matlab/matlab-engine-for-python.html>.
The Matlab package is only needed to run Matlab code and `tensorflow` or `tensorflow-gpu` packages are only needed if using DSen2 and/or S2 SSC or other Tensorflow based methods.
