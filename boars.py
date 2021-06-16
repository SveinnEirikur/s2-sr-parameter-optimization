from tqdm import tqdm
from scipy import io as spio
import os
import sys
import numpy as np
import random as rnd

import h5py
import matlab
import matlab.engine

import time
from datetime import timedelta

from hyperopt import fmin, tpe, hp, STATUS_OK, STATUS_FAIL, Trials
from hyperopt.pyll import scope
from hyperopt.fmin import generate_trials_to_calculate
from functools import reduce

sys.path.append("./")
from s2synth import rr_s2_data, mod_6_crop_s2_data, pad_to_size, unpad_from_size
from sreval import rmse, sre, uiqi, ergas, sam, ssim
from mat_loaders import get_data

seed = 42
np.random.seed(seed)
rnd.seed(seed)
os.environ['PYTHONHASHSEED']=str(seed)

# Paramters that have already been found
best_pars = {
    "apex": {
        "ATPRK": {
            "H": 11.0,
            "L_range": 17.0,
            "L_sill": 13.0,
            "Range_min": 0.9295475471200471,
            "Sill_min": 2.0,
            "rate": 1.1093648601650439
        },
        "MuSA": {
            "lam": 0.0005075231839284101,
            "mu": 0.21136587946368565
        },
        "S2Sharp": {
            "lam": 1.9341127858603557,
            "q1": 0.006073349262165454,
            "q10": 0.47647853130518464,
            "q2": 7.208822829845069e-05,
            "q3": 0.10893797078726071,
            "q4": 1.135516401017811,
            "q5": 14.103620956839348,
            "q6": 25.39252883568256,
            "q7": 0.9735978109673542,
            "q8": 66.43736365056141,
            "q9": 3.2947729421976493,
            "r": 9.0
        },
        "SSC": {
            "batch_size": 63,
            "lr": 0.0005153685695537464,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 0.16738800822718586,
            "mu": 24.9673461256305
        },
        "SupReME": {
            "lam": 0.0048653715844209616
        }
    },
    "aviris": {
        "ATPRK": {
            "H": 10.0,
            "L_range": 11.0,
            "L_sill": 25.0,
            "Range_min": 1.718972117535988,
            "Sill_min": 2.0,
            "rate": 2.483758771351466
        },
        "MuSA": {
            "lam": 18.58323542944518,
            "mu": 0.04384833806846039
        },
        "S2Sharp": {
            "lam": 15.602375101896984,
            "q1": 0.16189748106078408,
            "q10": 3.210142085847263,
            "q2": 0.08230034421305701,
            "q3": 0.6204556442261103,
            "q4": 1.1473841691370497,
            "q5": 0.3064198526603584,
            "q6": 2116.1399683180684,
            "q7": 11.796399561713402,
            "q8": 1.43347084163833,
            "q9": 28.661405699198124,
            "r": 9.0
        },
        "SSSS": {
            "lam": 2.9728318714583404,
            "mu": 12.903416818119323
        },
        "SupReME": {
            "lam": 0.0069191684407407155
        }
    },
    "coast": {
        "ATPRK": {
            "H": 10.0,
            "L_range": 29.0,
            "L_sill": 10.0,
            "Range_min": 1.4899073378189869,
            "Sill_min": 3.0,
            "rate": 0.8509611100645519
        },
        "MuSA": {
            "lam": 0.003070160927798489,
            "mu": 0.2677622798201873
        },
        "S2Sharp": {
            "lam": 61.06887402154388,
            "q1": 0.0017896762309261782,
            "q10": 0.5658297574376101,
            "q2": 0.0576967385834128,
            "q3": 0.07811016190942806,
            "q4": 0.4232511467802861,
            "q5": 5273.467594808693,
            "q6": 3.4654060793452914,
            "q7": 0.5736390247371966,
            "q8": 1.0989055603914524,
            "q9": 0.05347902023306669,
            "r": 8.0
        },
        "SSC": {
            "batch_size": 63,
            "lr": 0.0005153685695537464,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 354.1840305048178,
            "mu": 2614.163272319029
        },
        "SupReME": {
            "lam": 0.008359413765089602
        }
    },
    "crops": {
        "ATPRK": {
            "H": 10.0,
            "L_range": 11.0,
            "L_sill": 25.0,
            "Range_min": 1.718972117535988,
            "Sill_min": 2.0,
            "rate": 2.483758771351466
        },
        "MuSA": {
            "lam": 4.525702694704195,
            "mu": 0.1089370068057253
        },
        "S2Sharp": {
            "lam": 13.992261791161758,
            "q1": 0.011301489582144816,
            "q10": 0.12476202310790242,
            "q2": 0.002611181207262643,
            "q3": 0.41765924153895523,
            "q4": 81.80757436489843,
            "q5": 1.6408639954737678,
            "q6": 5.108972180131146,
            "q7": 21.89439729045958,
            "q8": 1.5563918734642455,
            "q9": 0.05319608639536076,
            "r": 8.0
        },
        "SSC": {
            "batch_size": 17,
            "lr": 0.0002464350897256471,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 10.997244596883432,
            "mu": 10.504266627092434
        },
        "SupReME": {
            "lam": 0.01012396399532167
        }
    },
    "default": {
        "ATPRK": {
            "H": 20,
            "L_range": 20,
            "L_sill": 20,
            "Range_min": 0.5,
            "Sill_min": 1,
            "rate": 0.1
        },
        "DSen2": {},
        "MuSA": {
            "lam": 0.005,
            "mu": 0.6,
        },
        "S2Sharp": {
            "lam": 0.00018998,
            "q1": 1,
            "q10": 1,
            "q2": 0.3851,
            "q3": 6.9039,
            "q4": 19.9581,
            "q5": 47.8967,
            "q6": 27.5518,
            "q7": 2.71,
            "q8": 34.8689,
            "q9": 1,
            "r": 8
        },
        "SSC": {
            "batch_size": 64,
            "lr": 0.0005,
            "ndown": 3,
            "num_epochs": 500,
            "mtf_down": False
        },
        "SSSS": {
            "ksize": 13,
            "lam": 0.1,
            "mu": 0.1
        },
        "SupReME": {
            "lam": 0.005,
            "p": 7
        }
    },
    "escondido": {
        "ATPRK": {
            "H": 10.0,
            "L_range": 12.0,
            "L_sill": 22.0,
            "Range_min": 1.2999237311657745,
            "Sill_min": 3.0,
            "rate": 0.32624542784882965
        },
        "MuSA": {
            "lam": 6.749723141559358,
            "mu": 1.1232718690037486
        },
        "S2Sharp": {
            "lam": 2.5161416208114624,
            "q1": 0.15933231239414453,
            "q10": 0.3905405999585421,
            "q2": 0.0027674109226805558,
            "q3": 0.8075354103001672,
            "q4": 2.025895992618407,
            "q5": 1007.1752582787667,
            "q6": 7349.730041849893,
            "q7": 0.3297598938644552,
            "q8": 1.1245744755321347,
            "q9": 332.719141769486,
            "r": 5.0
        },
        "SSC": {
            "batch_size": 16,
            "lr": 0.0006232930119819039,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 3.6755574345202326,
            "mu": 13.536454891599432
        },
        "SupReME": {
            "lam": 0.007326490511635219
        }
    },
    "escondido_s2": {
        "ATPRK": {
            "H": 11.0,
            "L_range": 10.0,
            "L_sill": 25.0,
            "Range_min": 1.1426393097183176,
            "Sill_min": 2.0,
            "rate": 0.38118563113034903
        },
        "MuSA": {
            "lam": 0.0006274677008391014,
            "mu": 0.02363444671432028
        },
        "S2Sharp": {
            "lam": 63.966522357122145,
            "q1": 0.05377734798309607,
            "q10": 3.4277403706757323,
            "q2": 0.029749221706835912,
            "q3": 1.0013241709298804,
            "q4": 7.296525793589869,
            "q5": 128.42383112424366,
            "q6": 113.99721155880002,
            "q7": 15.328765995152523,
            "q8": 0.26358829429560404,
            "q9": 1.2745762522831428,
            "r": 7.0
        },
        "SSC": {
            "batch_size": 21,
            "lr": 0.0004430836475802122,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 0.1308087572047968,
            "mu": 12.35800530027153
        },
        "SupReME": {
            "lam": 0.0073213185804962486
        }
    },
    "mountain": {
        "ATPRK": {
            "H": 10.0,
            "L_range": 18.0,
            "L_sill": 14.0,
            "Range_min": 1.3320449383413182,
            "Sill_min": 2.0,
            "rate": 1.0838347876174879
        },
        "MuSA": {
            "lam": 0.2815817835390236,
            "mu": 0.20680762741962738
        },
        "S2Sharp": {
            "lam": 1.6175102853916246,
            "q1": 0.00044542449399612676,
            "q10": 0.07491354626104034,
            "q2": 0.5682812411052716,
            "q3": 0.16578861665770028,
            "q4": 6.514133055574779,
            "q5": 61.79935545392391,
            "q6": 0.003379729596540834,
            "q7": 0.4634602396399483,
            "q8": 0.04589068253671385,
            "q9": 0.029990190605755463,
            "r": 5.0
        },
        "SSC": {
            "batch_size": 53,
            "lr": 0.0013452632885245465,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 0.09389232450175844,
            "mu": 601.3630308156096
        },
        "SupReME": {
            "lam": 0.008592020381430298
        }
    },
    "rkvik": {
        "ATPRK": {
            "H": 11.0,
            "L_range": 17.0,
            "L_sill": 13.0,
            "Range_min": 0.9295475471200471,
            "Sill_min": 2.0,
            "rate": 1.1093648601650439
        },
        "MuSA": {
            "lam": 66.83743856132301,
            "mu": 0.08911647178056135
        },
        "S2Sharp": {
            "lam": 1.4594340307449114,
            "q1": 0.00031478443572017546,
            "q10": 284.1445895177555,
            "q2": 0.09183799632938361,
            "q3": 0.6082154131484651,
            "q4": 0.5144111481319413,
            "q5": 2.9562324837078515,
            "q6": 66232.56042883813,
            "q7": 0.3862007199373696,
            "q8": 0.7222515544399222,
            "q9": 5525.7524502811475,
            "r": 9.0
        },
        "SSC": {
            "batch_size": 47,
            "lr": 0.0005854814665428689,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 20.064800454745807,
            "mu": 31.91482736104121
        },
        "SupReME": {
            "lam": 0.0058862649909480055
        }
    },
    "rkvik_rr_2": {
        "ATPRK": {
            "H": 10,
            "L_range": 11,
            "L_sill": 25,
            "Range_min": 1.718972117535988,
            "Sill_min": 2.0,
            "rate": 2.483758771351466
        },
        "MuSA": {
            "lam": 0.514587104720504,
            "mu": 0.04244875639644929
        },
        "S2Sharp": {
            "lam": 4.5019455648670235,
            "q1": 0.002461808675174749,
            "q2": 0.016534706198494616,
            "q3": 1.292647600704406,
            "q4": 0.10625035457565266,
            "q5": 1.968949146998428,
            "q6": 0.6977322625060097,
            "q7": 0.7180468895554312,
            "q8": 0.20895162340937157,
            "q9": 104.29845167329778,
            "r": 9.0
        },
        "SSC": {
            "batch_size": 18,
            "lr": 0.0006070133672749907,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 7014907.554849592,
            "mu": 100542.80730468447
        },
        "SupReME": {
            "lam": 0.0028813232785892405
        }
    },
    "rkvik_rr_6": {
        "ATPRK": {
            "H": 10.0,
            "L_range": 29.0,
            "L_sill": 10.0,
            "Range_min": 1.4899073378189869,
            "Sill_min": 3.0,
            "rate": 0.8509611100645519
        },
        "MuSA": {
            "lam": 1.8387602483563992,
            "mu": 0.0718138948489673
        },
        "S2Sharp": {
            "lam": 2.603050366741197,
            "q1": 0.00021861310683879556,
            "q10": 356.64630184004375,
            "q2": 0.00015066900528206697,
            "q3": 33289.84315589906,
            "q4": 0.1357216355551269,
            "q5": 33096.16139625704,
            "q6": 532941.4456555274,
            "q7": 5031.195549141296,
            "q8": 536279.7540579621,
            "q9": 0.3961545856726707,
            "r": 8.0
        },
        "SSSS": {
            "lam": 958.1508213653774,
            "mu": 103.36836331141293
        },
        "SupReME": {
            "lam": 0.01753077055392142
        }
    },
    "urban": {
        "ATPRK": {
            "H": 11.0,
            "L_range": 17.0,
            "L_sill": 13.0,
            "Range_min": 0.9295475471200471,
            "Sill_min": 2.0,
            "rate": 1.1093648601650439
        },
        "MuSA": {
            "lam": 66.6423594393631,
            "mu": 0.21909754096434964
        },
        "S2Sharp": {
            "lam": 977.1951026420713,
            "q1": 0.0003150958539615096,
            "q10": 0.6745077320163843,
            "q2": 0.0213591523862052,
            "q3": 0.11412706896122957,
            "q4": 2.4051833845129598,
            "q5": 18.57270432406506,
            "q6": 28.690647455909016,
            "q7": 0.7384861464045973,
            "q8": 13.28136851923011,
            "q9": 2.713963760462423,
            "r": 8.0
        },
        "SSC": {
            "batch_size": 26,
            "lr": 0.0014705228068054906,
            "mtf_down": True
        },
        "SSSS": {
            "lam": 0.831794922202297,
            "mu": 92.77161774683216
        },
        "SupReME": {
            "lam": 0.0064823718887722015
        }
    }
}

# Lists of installed methods and datasets
meth_list = ['S2Sharp', 'SSC'] #['ATPRK', 'DSen2', 'MuSA', 'S2Sharp', 'SSC', 'SSSS', 'SupReME']
data_list = ['rkvik', 'escondido', 'aviris'] #['apex', 'aviris', 'crops', 'coast', 'coastal', 'mountain', 'rkvik', 'escondido', 'urban']

# Objective function to evaluate
def objective_func(method, train_params, types, mYim_2, mYim_6, Xm_im, metric, limsub=6,
                   mtf=[ .32, .26, .28, .24, .38, .34, .34, .26, .33, .26, .22, .23],
                   d=[6,1,1,1,2,2,2,1,2,6,2,2], eval_bands=[2,6], matlab_func = True, verbose=False,
                   padding=(0,0)):

    if matlab_func:
        par_list = [(key, matlab.int16([value]) if types[key] is 'int' else matlab.double([value])) for key, value in train_params.items()]
        par_list = [item for subtuple in par_list for item in subtuple]
        par_list.append('mtf')
        par_list.append(matlab.double(mtf))

        Xhat = np.copy(Xm_im)
        if 2 in eval_bands:
            try:
                Xhat_2 = np.array(method(mYim_2,*par_list,nargout=2)[0])
            except:
                return {'loss': np.nan, 'status': STATUS_FAIL}
            idx_2 = np.nonzero(np.array([2])[:, None] == d)[1]
            Xhat_2 = unpad_from_size(Xhat_2,padding=padding//2)
            for i in idx_2:
                Xhat[i] = Xhat_2[:,:,i]
        if 6 in eval_bands:
            try:
                Xhat_6 = np.array(method(mYim_6,*par_list,nargout=2)[0])
            except:
                return {'loss': np.nan, 'status': STATUS_FAIL}
            idx_6 = np.nonzero(np.array([6])[:, None] == d)[1]
            Xhat_6 = unpad_from_size(Xhat_6,padding=padding//6)

            for i in idx_6:
                Xhat[i] = Xhat_6[:,:,i]
    else:
        train_params['mtf'] = mtf
        Xhat = np.copy(Xm_im)
        if 2 in eval_bands:
            Xhat_2 = method([np.array(im) for im in mYim_2],**train_params)
            idx_2 = np.nonzero(np.array([2])[:, None] == d)[1]
            Xhat_2 = unpad_from_size(Xhat_2,padding=padding//2)

            for i in idx_2:
                Xhat[i] = Xhat_2[:,:,i]
        if 6 in eval_bands:
            Xhat_6 = method([np.array(im) for im in mYim_6],**train_params)
            idx_6 = np.nonzero(np.array([6])[:, None] == d)[1]
            Xhat_6 = unpad_from_size(Xhat_6,padding=padding//6)
            for i in idx_6:
                Xhat[i] = Xhat_6[:,:,i]


    opt_loss = 0
    idx = np.nonzero(np.array(eval_bands)[:, None] == d)[1]
    for i in idx:
        if metric is 'sre': # Bigger is better
            SRE = sre(Xm_im[i][limsub:-limsub,limsub:-limsub], Xhat[i][limsub:-limsub,limsub:-limsub])
            opt_loss -= SRE
        elif metric is 'rmse': # Smaller is better
            RMSE = rmse(Xm_im[i][limsub:-limsub,limsub:-limsub], Xhat[i][limsub:-limsub,limsub:-limsub])
            opt_loss += RMSE
        elif metric is 'uiqi': # Bigger is better
            UIQI = uiqi(Xm_im[i][limsub:-limsub,limsub:-limsub], Xhat[i][limsub:-limsub,limsub:-limsub])
            opt_loss -= UIQI
        elif metric is 'ergas': # Smaller is better
            ERGAS = ergas(Xm_im[i][limsub:-limsub,limsub:-limsub], Xhat[i][limsub:-limsub,limsub:-limsub], d[i])
            opt_loss += ERGAS
        elif metric is 'ssim': # Bigger is better
            SSIM = ssim(Xm_im[i][limsub:-limsub,limsub:-limsub, np.newaxis], Xhat[i][limsub:-limsub,limsub:-limsub, np.newaxis],data_range=10000)[1]
            opt_loss -= SSIM
        else:
            Exception("Unknown metric: " + metric)
            opt_loss = np.nan

    if np.isnan(opt_loss):
        status = STATUS_FAIL
    else:
        status = STATUS_OK

    return {'loss': opt_loss/len(idx), 'status': status}

# Function to optimize parameters of single method
def opt_method(method, parameters, max_evals, dataset='rkvik', datadir='./data/', metric='sre', eval_bands=[2,6], matlab_func = True, verbose=False, savefile='./results/'+time.strftime("%Y%m%d%H%M")):

    par_space = {}
    for key, values in parameters.items():
        if values[2][0] is 'uniform_int':
            par_space[key] = scope.int(hp.quniform(key, values[2][1], values[2][2], 1))
        elif values[2][0] is 'lognormal':
            par_space[key] = hp.lognormal(key, values[2][1], values[2][2])
        elif values[2][0] is 'choice':
            par_space[key] = hp.choice(key, [values[2][1], values[2][2]])
        else:
            par_space[key] = values[1]

    par_types = {key: values[0] for key, values in parameters.items()}

    default_pars = [{key: values[1] for key, values in parameters.items()}]
    trials = generate_trials_to_calculate(default_pars)

    (Yim, mtf) = get_data(dataset, datadir=datadir, get_mtf=True)[:2]
    Xm_im = mod_6_crop_s2_data(Yim)
    mXm_im = [matlab.double(b.tolist()) for b in Xm_im]

    (mYim_2, mYim_6) = (None, None)
    Xm_pad, padding = pad_to_size(Xm_im)
    if 2 in eval_bands:
        Yim_2 = rr_s2_data(Xm_pad, 2, mtf=mtf)
        mYim_2 = [matlab.double(b.tolist()) for b in Yim_2]
    if 6 in eval_bands:
        Yim_6 = rr_s2_data(Xm_pad, 6, mtf=mtf)
        mYim_6 = [matlab.double(b.tolist()) for b in Yim_6]



    pars = fmin(lambda s_pars: objective_func(method, s_pars, par_types, mYim_2, mYim_6, Xm_im, metric, mtf=mtf, eval_bands=eval_bands, matlab_func=matlab_func, verbose=verbose, padding=padding),
                space=par_space,
                trials=trials,
                algo=tpe.suggest,
                max_evals=max_evals,
                rstate=np.random.RandomState(seed))

    improvements = reduce(improvement_only, trials.losses(), [])

    np.savez(savefile+'_'+dataset+'_'+metric, metric=metric, improvements=improvements, pars=pars, trials=trials)
    if verbose:
        print('pars:\n', pars)
        print('best', metric, ':', np.nanmin(improvements))
    return pars

# Helper functions

# Trim results to improvements only
def improvement_only(a, b):
    try:
        if np.nanmin([np.nanmin(a), b]) == np.nanmin(a):
            return a + [np.nanmin(a)]
        else:
            return a + [b]
    except ValueError:
        return a + [b]

# Convert parameter dictionary to Matlab list for Matlab method wrappers
def pardict_to_matlist(pardict, mat_types = {}):
    par_list = [(key, matlab.int16([value]) if mat_types.get(key, 'double')  is 'int' else matlab.double([value])) for key, value in pardict.items()]
    par_list = [item for subtuple in par_list for item in subtuple]
    return par_list

# Get handle for method (and parameters)
def get_method(meth_name, meth_path_prefix='./', matlab_handle=matlab.engine.start_matlab(), get_pars=False):
    if meth_name is 'ATPRK':
        matlab_handle.addpath(meth_path_prefix + meth_name)
        method = matlab_handle.ATPRKwrap
    elif meth_name is 'DSen2':
        from DSen2.DSen2wrap import DSen2wrap
        method = DSen2wrap
    elif meth_name is 'MuSA':
        matlab_handle.addpath(meth_path_prefix + 'MusaCode')
        method = matlab_handle.MuSAwrap
    elif meth_name is 'S2Sharp':
        matlab_handle.addpath(meth_path_prefix + meth_name)
        method = matlab_handle.S2sharpwrap
    elif meth_name is 'SSC':
        from S2_SSC_CNN.SSCwrap import SSCwrap
        method = SSCwrap
    elif meth_name is 'SSCnew':
        from S2_SSC_CNN.SSCwrap import SSCwrapNew
        method = SSCwrapNew
    elif meth_name is 'SSSS':
        matlab_handle.addpath(meth_path_prefix + meth_name)
        method = matlab_handle.SSSSwrap
    elif meth_name is 'SupReME':
        matlab_handle.addpath(meth_path_prefix + meth_name)
        method = matlab_handle.SupReMEwrap

    matlab_meths = ['ATPRK', 'MuSA', 'S2Sharp', 'SSSS', 'SupReME']
    if get_pars:
        pars = best_pars.get(get_pars, best_pars['default']).get(meth_name, {})
        if meth_name in matlab_meths:
            pars = pardict_to_matlist(pars)
        return method, pars

    return method
