import matlab

def get_params(dataset, optimization='rr_sre'):
    q  = matlab.double([1, 1.5, 4, 8, 15, 15, 20 ]) # lam_i = lam*qi
    ni = 10
    lam = 0.005
    if dataset=='apex':
        if optimization == 'ideal':
            lam = 0.00200508
            q = matlab.double([
            0.349182,
            0.954079,
            0.590972,
            0.687843,
            1.0075,
            1.46371,
            14.0941,
            10.089,
            ])
            r = 8
        elif optimization == 'ideal_n':
            lam = 0.00101607
            q = matlab.double([
            0.243101,
            0.931128,
            0.410796,
            1.13898,
            1.55145,
            1.13888,
            56.3397,
            ])
            r = 7
        elif optimization == 'GCV':
            lam = 0.000422043
            q = matlab.double([
                0.0703752,
                0.0273479,
                1.24559,
                9.78088,
                2.9625,
                27.2933,
                7.7959,
                1.07775,
                4.73929])
        elif optimization == 'GCV_n':
            lam = 0.0007546
            q = matlab.double([
            0.563744,
            0.653244,
            1.27014,
            0.586244,
            5.3383,
            1.71693,
            3.52951,
            0.405118,
            0.32013,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.000319623
            q = matlab.double([
            0.577739,
            1.04806,
            0.970213,
            0.365041,
            0.74398,
            0.834376,
            0.864461,
            4.93977,
            ])
            r = 8
        elif optimization == 'rr_sre_o':
            lam = 0.000196609
            q = matlab.double([
            0.107726,
            0.0432871,
            14.201,
            52.0878,
            215.535,
            164.86,
            ])
            r = 6
        elif optimization == 'rr_sre':
            lam = 0.000316304
            q = matlab.double([
            1.41549,
            0.108337,
            7.15475,
            26.6617,
            212.759,
            168.022,
            ])
            r = 6
        elif optimization == 'rr_sre_n':
            lam = 0.000198549
            q = matlab.double([
            0.878607,
            0.0553979,
            2.57351,
            8.98945,
            1335.44,
            180.353,
            1.25072,
            ])
            r = 7
        elif optimization == 'rr_sre_nn':
            lam = 0.000177115
            q = matlab.double([
            0.0907143,
            0.0297594,
            17.0042,
            43.9227,
            178.068,
            97.1123,
            ])
            r = 6
        elif optimization == 'rr_ergas_n':
            lam = 0.000331137
            q = matlab.double([
            3.29268,
            0.155855,
            10.7045,
            20.6277,
            1275.51,
            45.0961,
            0.293486,
            130.048,
            ])
            r = 8
        elif optimization == 'rr_ergas':
            lam = 0.000355903
            q = matlab.double([
            1.06179,
            0.00268791,
            3.96938,
            20.8726,
            108.041,
            56.8316,
            2.47369,
            ])
            r = 7
        elif optimization == 'rr_rmse':
            lam = 0.00016025
            q = matlab.double([
            0.757044,
            0.0331049,
            1.30751,
            5.59124,
            17287.2,
            167.189,
            15.8525,
            ])
            r = 7
        elif optimization == 'rr_uiqi':
            lam = 0.00134095
            q = matlab.double([
            0.617633,
            0.00676373,
            2.38342,
            6.61837,
            41.3486,
            41.2792,
            1.07916,
            ])
            r = 7
        elif optimization == 'rr_ssim':
            lam = 0.000759664
            q = matlab.double([
            1.59185,
            0.00719586,
            4.31588,
            6.2966,
            237.933,
            33.0332,
            10.9489,
            ])
            r = 7
    elif dataset=='aviris':
        if optimization == 'ideal':
            lam = 0.00060065
            q = matlab.double([
            0.000587661,
            7.28885e-06,
            1.50232,
            5.44054,
            10.6879,
            26.5834,
            6.95047,
            53.0524,
            1347.47,
            ])
            r = 9
        elif optimization == 'ideal_n':
            lam = 0.00215518
            q = matlab.double([
            0.00134254,
            3.58072e-05,
            0.627093,
            2.00977,
            6.67952,
            37.6147,
            3.40915,
            ])
            r = 7
        elif optimization == 'GCV':
            lam = 1.8998e-04
            matlab.double([1, 0.3851, 6.9039, 19.9581, 47.8967, 27.5518, 2.7100, 34.8689])
            r = 8
        elif optimization == 'GCV_n':
            lam = 0.000383248
            q = matlab.double([
            1.58846,
            0.969825,
            9.49955,
            0.133879,
            3.51395,
            10.3264,
            3.31159,
            1.1153,
            36.8282,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.000239401
            q = matlab.double([
            2.29628,
            1.11686,
            2.90024,
            0.0124843,
            11.3806,
            29.4766,
            5.19364,
            127.877,
            0.461376,
            ])
            r = 9
        elif optimization == 'rr_sre':
            lam = 0.000123405
            q = matlab.double([
            0.0037392,
            0.00207446,
            15.2475,
            116.283,
            70.4591,
            4455.2,
            177.036,
            224.716,
            ])
            r = 8
        elif optimization == 'rr_sre_n':
            lam = 0.00038307
            q = matlab.double([
            0.0925057,
            0.0723276,
            1.87213,
            23.5976,
            32.1346,
            94.2771,
            1667.55,
            0.129296,
            ])
            r = 8
        elif optimization == 'rr_sre_nn':
            lam = 0.000143452
            q = matlab.double([
            0.036531,
            0.0110786,
            0.827969,
            43.9915,
            312.211,
            220.972,
            306.414,
            0.65975,
            ])
            r = 8
        elif optimization == 'rr_ergas_n':
            lam = 0.000405849
            q = matlab.double([
            0.845603,
            0.0669185,
            2.85743,
            34.4657,
            8.99974,
            196.618,
            62.0514,
            0.32674,
            ])
            r = 8
        elif optimization == 'rr_ergas':
            lam = 0.000340829
            q = matlab.double([
            1.60503,
            0.116466,
            10.5806,
            36.3803,
            28.1822,
            73.3435,
            146.935,
            0.801697,
            ])
            r = 8
        elif optimization == 'rr_rmse':
            lam = 0.000425428
            q = matlab.double([
            0.44327,
            0.0244926,
            5.18908,
            14.8288,
            26.2355,
            157.396,
            63.4081,
            0.962616,
            ])
            r = 8
    elif dataset=='coast':
        if optimization == 'ideal':
            lam = 0.000667277
            q = matlab.double([
            1.93035e-05,
            0.268439,
            0.046365,
            1.66796,
            14.4589,
            24.7991,
            38.9282,
            73.8204,
            14194.1,
            ])
            r = 9
        elif optimization == 'ideal_n':
            lam = 3.49407e-05
            q = matlab.double([
            0.503074,
            25.8306,
            1.37668,
            70.244,
            0.954912,
            ])
            r = 5
        elif optimization == 'GCV':
            lam = 0.00118222
            q = matlab.double([
                0.153525,
                0.414878,
                0.0957268,
                0.414652,
                0.54091,
                2.95721,
                5.69541,
                23.1437,
                31.6689])
        elif optimization == 'GCV_n':
            lam = 0.000314764
            q = matlab.double([
            6.50838,
            1.05766,
            0.607766,
            3.0301,
            1.18626,
            0.456872,
            1.46935,
            0.498346,
            42.9818,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 5.22837e-05
            q = matlab.double([
            1.02454,
            1.57314,
            2.91213,
            2.56047,
            0.497597,
            1.89246,
            1.57905,
            0.986129,
            1.73245,
            ])
            r = 9
        elif optimization == 'rr_sre':
            lam = 0.000362058
            q = matlab.double([
            0.0387799,
            0.800832,
            0.0944872,
            12.7957,
            1293.54,
            0.139943,
            ])
            r = 6
        elif optimization == 'rr_sre_n':
            lam = 0.000428011
            q = matlab.double([
            0.0214902,
            0.108617,
            2.29038,
            9.89639,
            107.256,
            36.559,
            47.4116,
            222.087,
            0.0303276,
            ])
            r = 9
        elif optimization == 'rr_sre_nn':
            lam = 0.000405314
            q = matlab.double([
            0.0624643,
            0.908117,
            0.149118,
            10.5585,
            802.878,
            0.207455,
            ])
            r = 6
        elif optimization == 'rr_ergas_n':
            lam = 0.000835689
            q = matlab.double([
            0.0763826,
            1.22396,
            0.00268051,
            5.45043,
            21.9537,
            12.4578,
            3840.23,
            ])
            r = 7
        elif optimization == 'rr_ergas':
            lam = 0.000656979
            q = matlab.double([
            0.0873805,
            0.667744,
            0.00426095,
            4.46316,
            93.3861,
            18.2929,
            4872.35,
            ])
            r = 7
        elif optimization == 'rr_rmse':
            lam = 0.000172283
            q = matlab.double([
            0.989857,
            1.58359,
            9.16708,
            21.6536,
            2072.18,
            92.5462,
            ])
            r = 6
    elif dataset=='coastal':
        if optimization == 'rr_sre':
            lam = 0.000122257
            q = matlab.double([
            1.02369,
            0.466235,
            1.21828,
            17.8233,
            120.821,
            30.0021,
            79.1595,
            172.937,
            ])
            r = 8
        elif optimization == 'rr_ergas':
            lam = 0.00014971
            q = matlab.double([
            0.145933,
            0.398848,
            1.807,
            16.1427,
            68.4505,
            0.180518,
            138.938,
            ])
            r = 7
        elif optimization == 'rr_rmse':
            lam = 5.67017e-05
            q = matlab.double([
            1.1424,
            1.63236,
            1.15852,
            29.6844,
            355.718,
            1.49547,
            0.143685,
            300.493,
            ])
            r = 8
        elif optimization == 'GCV':
            lam = 0.000542074
            q = matlab.double([
            0.00506106,
            3.21738,
            3.87999,
            1.21818,
            1.07205,
            26.6719,
            31.7038,
            142.212,
            90.8413,
            ])
            r = 9
    elif dataset=='crops':
        if optimization == 'ideal':
            lam = 2.13433e-05
            q = matlab.double([
            264.548,
            78.83,
            1023.67,
            956.246,
            0.734589,
            5341.17,
            ])
            r = 6
        elif optimization == 'ideal_n':
            lam = 3.85041e-05
            q = matlab.double([
            191.75,
            8.55122,
            635.33,
            823.868,
            0.197727,
            2851.47,
            ])
            r = 6
        elif optimization == 'GCV':
            lam = 0.00173809
            q = matlab.double([
                0.583104,
                0.360554,
                3.14759,
                2.19579,
                2.33035,
                4.0836,
                3.6046,
                6.95779,
                10.5312])
            r = 9
        elif optimization == 'GCV_n':
            lam = 0.000227522
            q = matlab.double([
            8.73709,
            1.06094,
            0.0985048,
            66.2204,
            318.118,
            177.319,
            8.06276,
            213.238,
            0.370881,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 5.66434e-05
            q = matlab.double([
            3.04518,
            0.489115,
            1.18262,
            2.02312,
            2.13435,
            0.312664,
            ])
            r = 6
        elif optimization == 'rr_sre':
            lam = 0.00130781
            q = matlab.double([
            1.07453,
            0.000851113,
            2.98939,
            25.135,
            130.249,
            752.311,
            85.1652,
            340.902,
            ])
            r = 8
        elif optimization == 'rr_sre_n':
            lam = 0.0051785
            q = matlab.double([
            0.0366183,
            0.0663601,
            2.16235,
            31.8246,
            0.0858453,
            3.73527,
            9.41605,
            17.846,
            8.07157,
            ])
            r = 9
        elif optimization == 'rr_sre_nn':
            lam = 0.00259568
            q = matlab.double([
            0.370585,
            0.109582,
            4.63852,
            23.7728,
            58.2265,
            44.9012,
            12.3277,
            ])
            r = 7
        elif optimization == 'rr_ergas_n':
            lam = 0.000907303
            q = matlab.double([
            2.66523,
            0.296735,
            7.60186,
            32.6587,
            199.949,
            257.579,
            20.8458,
            ])
            r = 7
        elif optimization == 'rr_ergas':
            lam = 0.00276235
            q = matlab.double([
            1.27065,
            0.242294,
            9.42551,
            41.4522,
            117.478,
            48.8806,
            31.7021,
            59.2358,
            ])
            r = 8
        elif optimization == 'rr_rmse':
            lam = 0.00370537
            q = matlab.double([
            0.313314,
            3.05725e-05,
            1.16657,
            12.1722,
            88.9834,
            3.53121,
            5.63353,
            ])
            r = 7
    elif dataset=='escondido':
        if optimization == 'rr_sre':
            lam = 0.000457591
            q = matlab.double([
            1.50696,
            0.185075,
            5.14426,
            22.3091,
            513.232,
            230.892,
            ])
            r = 6
    elif dataset=='escondido_s2':
        if optimization == 'rr_sre':
            lam = 0.00065093
            q = matlab.double([
            0.345442,
            0.621202,
            25.8803,
            19.2608,
            0.906405,
            87.7983,
            0.175561,
            12.2923,
            ])
            r = 8
    elif dataset=='iceland':
        if optimization == 'rr_sre':
            lam = 0.00137709
            q = matlab.double([
            0.21914,
            0.113781,
            0.999692,
            4390.07,
            0.333209,
            1.02565,
            2.86649,
            1.93228,
            2.97514,
            ])
            r = 9
    elif dataset=='iceland_rr':
        if optimization == 'rr_sre':
            lam = 0.000206763
            q = matlab.double([
            0.0543664,
            0.580227,
            18.6279,
            186.472,
            3132.53,
            129.879,
            26.5783,
            168.931,
            ])
            r = 8
    elif dataset=='iceland_rr_2':
        if optimization == 'rr_sre':
            lam = 0.000109267
            q = matlab.double([
            1.07015,
            0.262242,
            37.7314,
            78.8234,
            1501.64,
            79.7164,
            17.8193,
            1100.59,
            ])
            r = 8
    elif dataset=='mountain':
        if optimization == 'ideal':
            lam = 0.00216969
            q = matlab.double([
            0.346479,
            0.305817,
            0.266932,
            2.67051,
            196.512,
            55.2132,
            38.2488,
            12.6415,
            ])
            r = 8
        elif optimization == 'ideal_n':
            lam = 9.46636e-05
            q = matlab.double([
            5.55081,
            9.02829,
            12.5886,
            64.4299,
            31.0462,
            ])
            r = 5
        elif optimization == 'GCV_o':
            lam = 0.00015977
            q = matlab.double([
            7.02729,
            0.840853,
            2.60173,
            0.237542,
            6.19887,
            0.187936,
            1.22626,
            0.288377,
            0.270397,
            0.816101,
            ])
            r = 10
        elif optimization == 'GCV':
            lam = 0.000392969
            q = matlab.double([
            0.567815,
            0.398023,
            0.404379,
            2.46062,
            19.8845,
            8.25248,
            2.69655,
            2.3237,
            34.6953,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.00011767
            q = matlab.double([
            0.674463,
            0.781058,
            1.20851,
            0.476037,
            0.494999,
            1.19641,
            3.19563,
            2.59724,
            ])
            r = 8
        elif optimization == 'rr_sre':
            lam = 0.000363916
            q = matlab.double([
            0.0810021,
            1.95113,
            1.146,
            19.7159,
            677.394,
            318.375,
            ])
            r = 6
        elif optimization == 'rr_sre_n':
            lam = 9.44389e-05
            q = matlab.double([
            3.20926,
            0.305962,
            0.0650915,
            51.9234,
            564897,
            3598.64,
            ])
            r = 6
        elif optimization == 'rr_sre_nn':
            lam = 0.000307629
            q = matlab.double([
            0.079841,
            2.0765,
            0.200203,
            22.6748,
            417.805,
            262.887,
            ])
            r = 6
        elif optimization == 'rr_ergas_n':
            lam = 8.50362e-05
            q = matlab.double([
            0.953303,
            1.43366,
            0.134723,
            54.6782,
            1718.7,
            4209.68,
            ])
            r = 6
        elif optimization == 'rr_ergas':
            lam = 7.28534e-05
            q = matlab.double([
            0.145834,
            0.105566,
            0.268845,
            75.1024,
            693.566,
            485.944,
            ])
            r = 6
        elif optimization == 'rr_rmse':
            lam = 0.00156272
            q = matlab.double([
            0.0128446,
            0.0050835,
            0.324106,
            2.19083,
            189.088,
            ])
            r = 5
    elif dataset=='rkvik':
        if optimization == 'rr_sre':
            lam = 8.52703e-05
            q = matlab.double([
            0.078945,
            0.28956,
            52.7382,
            171.481,
            1535.54,
            95.2223,
            ])
            r = 6
    elif dataset=='rkvik_rr_2':
        if optimization == 'rr_sre':
            lam = 7.7549e-05
            q = matlab.double([
            1.19622,
            0.0148103,
            5.05158,
            1208.75,
            0.724338,
            18.7021,
            74.2194,
            0.118337,
            ])
            r = 8
    elif dataset=='rkvik_rr_6':
        if optimization == 'rr_sre':
            lam = 9.76673e-05
            q = matlab.double([
            0.0416697,
            0.505222,
            43.2462,
            165.932,
            692.62,
            1.03513,
            ])
            r = 6
    elif dataset=='rkvik_old':
        if optimization == 'rr_sre':
            lam = 0.000772894
            q = matlab.double([
            0.0409162,
            0.000192297,
            327.276,
            6.47861,
            22.9646,
            50.1356,
            71.0892,
            0.254077,
            ])
            r = 8
        elif optimization == 'rr_ergas':
            lam = 0.001539
            q = matlab.double([
            0.00768493,
            0.18832,
            11.2963,
            0.760008,
            32.8554,
            1.15487,
            15.3614,
            1.45788,
            31.3659,
            ])
            r = 9
        elif optimization == 'rr_rmse':
            lam = 0.000197475
            q = matlab.double([
            0.0453412,
            0.744764,
            20.0924,
            88.5051,
            216.706,
            5.82764,
            29.8226,
            362.916,
            0.2677,
            ])
            r = 9
        elif optimization == 'GCV':
            lam = 0.000388563
            q = matlab.double([
            0.495476,
            0.952489,
            0.937399,
            9.75678,
            1.65842,
            24.4969,
            288.216,
            1551.32,
            2.52611,
            ])
            r = 9
    elif dataset=='rkvik_mtf2':
        if optimization == 'GCV':
            lam = 2.09881e-05
            q = matlab.double([
            0.594128,
            2.86391,
            16.5566,
            0.294926,
            0.868962,
            1.09047,
            4.36971,
            1.03218,
            0.43639,
            2.99028,
            ])
            r = 10
        elif optimization == 'ideal':
            lam = 0.0541667
            q = matlab.double([
            3.4702e-05,
            5.61888e-05,
            0.0174434,
            0.203976,
            0.00979765,
            193.862,
            0.0769602,
            ])
            r = 7
        elif optimization == 'GCVr':
            lam = 7.77287e-05
            q = matlab.double([
            1.35043,
            0.809975,
            0.598486,
            1.20245,
            0.369638,
            1.49738,
            1.37401,
            ])
            r = 7
        elif optimization == 'rr_sre':
            lam = 0.000186157
            q = matlab.double([
            0.928564,
            0.0281045,
            6.90699,
            611.329,
            809.966,
            45.9128,
            40.8958,
            0.282592,
            ])
            r = 8
    elif dataset=='rkvik_mtf6':
        if optimization == 'GCV':
            lam = 5.97214e-05
            q = matlab.double([
            0.0396601,
            12.2224,
            2.08637,
            56.6904,
            0.683954,
            0.00410711,
            0.000331719,
            0.00448156,
            0.754593,
            1.44611,
            ])
            r = 10
        elif optimization == 'ideal':
            lam = 0.00281641
            q = matlab.double([
            0.000440019,
            8.31548e-05,
            0.00181697,
            9.04222,
            910.446,
            2.21256,
            ])
            r = 6
        elif optimization == 'GCVr':
            lam = 0.000257053
            q = matlab.double([
            1.82319,
            0.25905,
            1.21221,
            1.24811,
            1.1536,
            14.0727,
            ])
            r = 6
        elif optimization == 'rr_sre':
            lam = 0.000815527
            q = matlab.double([
            0.486738,
            2.01729,
            0.764502,
            41.791,
            2.01672,
            2407.24,
            33.196,
            1.12339,
            ])
            r = 8
    elif dataset=='rkvik_s2':
        if optimization == 'GCV':
            lam = 7.17796e-05
            q = matlab.double([
            0.011821,
            68.7652,
            9.90415,
            0.687125,
            0.0296841,
            0.104504,
            20.1618,
            24.2052,
            0.766529,
            231.228,
            ])
            r = 10
        elif optimization == 'ideal':
            lam = 0.00131566
            q = matlab.double([
            5.34194,
            10.1528,
            27.2088,
            5535.34,
            189.268,
            ])
            r = 5
        elif optimization == 'GCVr':
            lam = 0.000237039
            q = matlab.double([
            0.916466,
            0.826833,
            1.01623,
            0.846052,
            1.39309,
            ])
            r = 5
    elif dataset=='rkvik_s6':
        if optimization == 'GCV':
            lam = 7.45075e-06
            q = matlab.double([
            0.235705,
            88.5079,
            0.0616234,
            0.502528,
            11.8195,
            0.558297,
            7.00039,
            0.251121,
            1.71036,
            1334.2,
            ])
            r = 10
        elif optimization == 'ideal':
            lam = 0.00603578
            q = matlab.double([
            0.000105691,
            0.0002413,
            10.488,
            0.167993,
            13694.9,
            0.28188,
            0.142059,
            8.10269e-05,
            0.0923875,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.00032615
            q = matlab.double([
            2.10504,
            1.02636,
            1.24889,
            0.140307,
            4.66208,
            0.415485,
            0.902378,
            0.342764,
            49.7376,
            ])
            r = 9
    elif dataset=='safrica':
        if optimization == 'ideal':
            lam = 0.0032514
            q = matlab.double([
            1.17629,
            0.854442,
            1.81954,
            12.4208,
            30.6231,
            263.42,
            8.60412,
            1.56509,
            593.951,
            ])
            r = 9
        elif optimization == 'ideal_n':
            lam = 0.00909727
            q = matlab.double([
            0.56833,
            0.0914207,
            1.67737,
            3.09647,
            19.8982,
            2.18898,
            13.3274,
            ])
            r = 7
        elif optimization == 'GCV':
            lam = 2.54952e-06
            q = matlab.double([
                9.29524,
                1.7426,
                2.80949,
                1.03988,
                0.00159016,
                4.42529,
                1.04598,
                3.89975,
                5.44934])
        elif optimization == 'GCV_n':
            lam = 7.84393e-06
            q = matlab.double([
            1.34121,
            0.28397,
            0.532726,
            0.742338,
            0.031983,
            0.902516,
            0.345603,
            1.73051,
            1.34217,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.000188477
            q = matlab.double([
            1.14601,
            0.60389,
            0.913487,
            0.703613,
            0.854465,
            1.41819,
            1.27554,
            0.897641,
            0.87673,
            ])
            r = 9
        elif optimization == 'rr_sre':
            lam = 2.24151e-05
            q = matlab.double([
            0.18777,
            0.00019877,
            9.75254,
            89.5484,
            1801.06,
            159.898,
            608.704,
            13195,
            22136.6,
            ])
            r = 9
        elif optimization == 'rr_sre_n':
            lam = 0.00542979
            q = matlab.double([
            0.00167365,
            0.0559822,
            0.010507,
            0.502766,
            30.4627,
            7.97957,
            ])
            r = 6
        elif optimization == 'rr_ergas':
            lam = 9.56871e-05
            q = matlab.double([
            0.00841458,
            0.0278981,
            0.0366961,
            59.3621,
            1438.68,
            10.0628,
            13.5639,
            ])
            r = 7
        elif optimization == 'rr_rmse':
            lam = 0.000194481
            q = matlab.double([
            0.0132892,
            0.0415478,
            2.57244,
            20.0887,
            390.674,
            6.40721,
            2.30707,
            ])
            r = 7
    elif dataset=='santa_maria':
        if optimization == 'ideal':
            lam = 0.000253117
            q = matlab.double([
                0.195745,
                0.0306228,
                1.30319,
                0.575307,
                9.80953,
                4.35496,
                4.76947,
                14.0517,
                3202.57])
            r = 9
        elif optimization == 'ideal_n':
            lam = 0.000518337
            q = matlab.double([
            0.289935,
            0.018663,
            1.14199,
            0.785636,
            10.1776,
            34.6887,
            ])
            r = 6
        elif optimization == 'GCV_o':
            lam = 0.000284492
            q = matlab.double([
            0.117502,
            0.166192,
            0.999137,
            0.770664,
            1.83553,
            0.927863,
            56.5226,
            0.0961208,
            60.3816,
            9.98532,
            ])
            r = 10
        elif optimization == 'GCV':
            lam = 0.000377364
            q = matlab.double([
            0.00883758,
            0.516039,
            1.15893,
            0.0162971,
            0.388294,
            5.20711,
            34.3934,
            0.914927,
            126.781,
            ])
            r = 9
        elif optimization == 'GCV_?':
            lam = 2.02458e-05
            q = matlab.double([
            0.186332,
            0.0163227,
            19.4994,
            38.6992,
            121.31,
            335.47,
            1589.8,
            0.00964576,
            2152.02,
            ])
            r = 9
        elif optimization == 'GCV_n':
            lam = 0.000165471
            q = matlab.double([
            1.80617,
            0.292183,
            0.859114,
            1.09276,
            12.7757,
            6.15608,
            9.12394,
            2.28646,
            45.483,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.000338076
            q = matlab.double([
            2.06471,
            0.946574,
            0.958038,
            1.63968,
            0.971178,
            2.47664,
            1.14643,
            0.977708,
            0.91937])
            r = 9
        elif optimization == 'rr_sre_o':
            lam = 0.00135479
            q = matlab.double([
            0.194571,
            0.0108336,
            1.60353,
            1.85409,
            87.0953,
            255.509,
            115.941,
            ])
            r = 7
        elif optimization == 'rr_sre_n':
            lam = 0.000460541
            q = matlab.double([
            1.42074,
            0.00798513,
            4.63737,
            2.2266,
            99.0929,
            132.154,
            ])
            r = 6
        elif optimization == 'rr_sre':
            lam = 0.00143957
            q = matlab.double([
            0.468803,
            0.0251231,
            1.34975,
            1.12136,
            56.5682,
            186.201,
            109.091,
            ])
            r = 7
        elif optimization == 'rr_ergas_n':
            lam = 0.000642706
            q = matlab.double([
            0.513626,
            0.381456,
            2.19198,
            0.247901,
            20.9889,
            451.429,
            110.415,
            ])
            r = 7
        elif optimization == 'rr_ergas':
            lam = 0.000570108
            q = matlab.double([
            0.346284,
            0.00824282,
            1.75968,
            0.213888,
            25.2687,
            581.291,
            ])
            r = 6
        elif optimization == 'rr_rmse':
            lam = 0.000395771
            q = matlab.double([
            0.214682,
            0.0182629,
            1.60957,
            0.953507,
            3845.83,
            1.38986,
            185.843,
            ])
            r = 7
        elif optimization == 'rr_uiqi':
            lam = 0.000167966
            q = matlab.double([
            1.01307,
            0.986774,
            16.9371,
            33.7575,
            381.428,
            306.723,
            ])
            r = 6
        elif optimization == 'rr_ssim':
            lam = 0.000460101
            q = matlab.double([
            3.08817,
            0.000571481,
            12.7017,
            15.4504,
            234.296,
            321.394,
            ])
            r = 6
        elif optimization == 'rr_bic':
            lam = 0.00452274
            q = matlab.double([
            1.95349,
            2.64066,
            6.13779,
            2.82168,
            35.4473,
            ])
            r = 5
    elif dataset=='santa_maria_s2':
        if optimization == 'rr_ergas':
            lam = 0.000994898
            q = matlab.double([
            0.160615,
            1.07465,
            2.01359,
            6.81682,
            24.4364,
            ])
            r = 5
        elif optimization == 'rr_rmse_o':
            lam = 0.000292109
            q = matlab.double([
            0.0178033,
            0.290948,
            3.86289,
            136.374,
            50.8491,
            39.2055,
            ])
            r = 6
        elif optimization == 'rr_sre':
            lam = 0.000231284
            q = matlab.double([
            0.706203,
            1.74041,
            6.80911,
            4.71103,
            105.177,
            ])
            r = 5
        elif optimization == 'rr_sre_n':
            lam = 0.000553043
            q = matlab.double([
            0.142856,
            0.195249,
            0.985093,
            210.007,
            1259.46,
            6.77252,
            1.37802,
            4.4937,
            ])
            r = 8
        elif optimization == 'rr_rmse':
            lam = 0.00310415
            q = matlab.double([
            0.0188028,
            0.0360011,
            0.453634,
            2.51621,
            0.985141,
            110.173,
            3.54881,
            1.45994,
            ])
            r = 8
        elif optimization == 'rr_ergas_n':
            lam = 0.00100608
            q = matlab.double([
            0.437973,
            0.193673,
            1.72061,
            12.6712,
            152.284,
            7.40373,
            0.336221,
            ])
            r = 7
        elif optimization == 'GCV':
            lam = 0.000281141
            q = matlab.double([
            0.0513061,
            1.51491,
            2.97134,
            5.60074,
            1.91937,
            0.832443,
            0.391676,
            0.625703,
            0.273145,
            ])
            r = 9
        elif optimization == 'GCV_n':
            lam = 0.000144345
            q = matlab.double([
            0.0696998,
            1.74183,
            11.0268,
            8.94841,
            0.764464,
            1.47928,
            0.0496818,
            0.357481,
            0.109879,
            ])
            r = 9
    elif dataset=='seltjarnarnes':
        if optimization == 'rr_ergas':
            lam = 0.000353692
            q = matlab.double([
            2.42493,
            0.115526,
            4.70955,
            2.69254,
            4.3666,
            6.67331,
            281.593,
            ])
            r = 7
        elif optimization == 'rr_rmse':
            lam = 0.000360518
            q = matlab.double([
            1.87586,
            0.522813,
            3.73849,
            85.7581,
            7.54172,
            0.726205,
            47.4561,
            128.942,
            13.1234,
            ])
            r = 9
        elif optimization == 'rr_sre':
            lam = 0.000295606
            q = matlab.double([
            2.514,
            0.749931,
            6.28296,
            67.6788,
            4.45314,
            0.568689,
            2.05177,
            8.86209,
            ])
            r = 8
    elif dataset=='snow':
        if optimization == 'rr_sre':
            lam = 0.000165091
            q = matlab.double([
            1.17438,
            0.987536,
            39.2592,
            81.9644,
            102.152,
            ])
            r = 5
        elif optimization == 'rr_ergas':
            lam = 0.00015356
            q = matlab.double([
            0.382772,
            0.448039,
            10.2798,
            68.5665,
            821.088,
            316.509,
            82.3193,
            ])
            r = 7
        elif optimization == 'rr_rmse':
            lam = 0.000276963
            q = matlab.double([
            0.162764,
            0.115408,
            26.5781,
            34.0601,
            0.561444,
            ])
            r = 5
        elif optimization == 'GCV':
            lam = 0.000762041
            q = matlab.double([
            0.582827,
            0.514861,
            1.34369,
            0.38168,
            8.65245,
            40.8045,
            0.624175,
            19.0212,
            12.595,
            ])
            r = 9
    elif dataset=='urban':
        if optimization == 'ideal':
            lam = 0.00912825
            q = matlab.double([
            0.00846139,
            3.79809e-05,
            0.044885,
            0.389345,
            1.05078,
            89.7673,
            4.9749,
            2.34486,
            ])
            r = 8
        elif optimization == 'ideal_n':
            lam = 0.00520207
            q = matlab.double([
            0.0177712,
            0.00743125,
            0.321652,
            0.486951,
            13.8569,
            1.56069,
            66.6145,
            ])
            r = 7
        elif optimization == 'GCV':
            lam = 0.00158383
            q = matlab.double([
                0.13905,
                1.29318,
                0.254234,
                0.140175,
                2.72957,
                0.593441,
                7.55243,
                2.65688,
                32.2374])
            r = 9
        elif optimization == 'GCV_n':
            lam = 0.000685892
            q = matlab.double([
            0.0612631,
            5.74191,
            0.715746,
            1.1055,
            14.3665,
            3.01768,
            15.8682,
            0.451267,
            19.7668,
            ])
            r = 9
        elif optimization == 'GCVr':
            lam = 0.000187254
            q = matlab.double([
            1.05912,
            0.213911,
            7.84348,
            41.8325,
            46.2007,
            0.734656,
            2.60384,
            0.712278,
            ])
            r = 8
        elif optimization == 'rr_sre':
            lam = 5.58742e-05
            q = matlab.double([
            0.155244,
            0.476503,
            13.4542,
            256.614,
            652.734,
            7728.16,
            ])
            r = 6
        elif optimization == 'rr_sre_n':
            lam = 8.82404e-05
            q = matlab.double([
            0.248551,
            3.31862,
            0.762792,
            138.003,
            10622.2,
            45783.4,
            5.53113,
            5.81795,
            ])
            r = 8
        elif optimization == 'rr_ergas_n':
            lam = 0.000892799
            q = matlab.double([
            0.0511166,
            2.57109,
            0.123638,
            13.0458,
            93.1392,
            16.3694,
            ])
            r = 6
        elif optimization == 'rr_ergas':
            lam = 0.00107263
            q = matlab.double([
            0.0918719,
            1.52684,
            0.135112,
            9.50069,
            135.367,
            ])
            r = 5
        elif optimization == 'rr_rmse':
            lam = 0.000200402
            q = matlab.double([
            0.501621,
            0.946125,
            5.19259,
            95.9144,
            338.546,
            ])
            r = 5



    r = q.size[-1]
    return lam, q, r

