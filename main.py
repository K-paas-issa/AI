import warnings
warnings.filterwarnings('ignore'  )


from pathlib import Path
import pickle
from collections import OrderedDict
import pandas as pd
import datetime as dt

import numpy as np
try:
    np.distutils.__config__.blas_opt_info = np.distutils.__config__.blas_ilp64_opt_info
except Exception:
    pass
from scipy import stats

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import (roc_curve, roc_auc_score, confusion_matrix, accuracy_score, f1_score,
                             precision_recall_curve)
from mlxtend.plotting import plot_confusion_matrix

import pymc as pm
from pymc.variational.callbacks import CheckParametersConvergence
import statsmodels.formula.api as smf

import arviz as az
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import seaborn as sns
from collections import Counter
import numpy as np
def main2(ai_input_data):
    print('main start')
    list1 = []
    try:
        RANDOM_SEED=42
        data=np.load(ai_input_data)
        df_special = pd.DataFrame(data)
        with pm.Model() as ar1:
        # assumes 95% of prob mass is between -2 and 2
            rho = pm.Normal("rho", mu=0.0, sigma=1.0, shape=2)
        # precision of the innovation term
            tau = pm.Exponential("tau", lam=0.5)

            likelihood = pm.AR(
            "y", rho=rho, tau=tau, constant=True, init_dist=pm.Normal.dist(0, 10), observed=df_special[2]
        )

            idata = pm.sample(1000, tune=2000, random_seed=RANDOM_SEED)
        print('sample 1000, 2000 end')
        with ar1:
            predictions = pm.sample_posterior_predictive(idata, predictions=True).predictions

    #print(predictions.y[0])
        print('save sample.csv start')
        np.savetxt('sample.csv',predictions.y[0],delimiter=",")

        df=pd.read_csv("sample.csv")
        print('save sample.csv read')
        temp= list(df.columns)
        print('after temp=list(df.columns)')
        df = df.T.reset_index(drop=True).T
        print('after df = df.T.reset_index(drop=True).T')
        df1 = pd.concat([pd.DataFrame(data=[temp]),df],ignore_index=True)
        print('after df1 = pd.concat([pd.DataFrame(data=[temp]),df],ignore_index=True)')
        stat=[]
        for i in range(0,df1.shape[1]):
            stat.append( df[i].lt(0).idxmax())
        print('after for i in range(0,df1.shape[1]):')
        array=np.array(stat)
        print('after array=np.array(stat)')
        ctr=Counter(array)
        print('ctr=Counter(array)')
        if (len(ctr.most_common(1)) >= 1):
            print(ctr.most_common(1)[0])
            fmcv, ify1 = ctr.most_common(1)[0]
            dict1 = dict()
            dict1['latitude'] = df_special[0][fmcv]
            dict1['longitude'] = df_special[1][fmcv]
            dict1['risk'] = ify1
            dict1['start_prediction_time'] = dt.datetime.now()
            print('dict1 = {}'.format(dict1))
            list1.append(dict1)
        else:
            print('len(ctr.most_common(1)) < 1')
            return None

        if (len(ctr.most_common(2)) >= 2):
            print(ctr.most_common(2)[1])
            smcv, ify2 = ctr.most_common(2)[1]
            dict2 = dict()
            dict2['latitude'] = df_special[0][smcv]
            dict2['longitude'] = df_special[1][smcv]
            dict2['risk'] = ify2
            dict2['start_prediction_time'] = dt.datetime.now()
            print('dict2 = {}'.format(dict2))
            list1.append(dict2)
        else:
            print('len(ctr.most_common(2)) < 2')

        if (len(ctr.most_common(3)) >= 3):
            print(ctr.most_common(3)[2])
            tmcv, ify3 = ctr.most_common(3)[2]
            dict3 = dict()
            dict3['latitude'] = df_special[0][tmcv]
            dict3['longitude'] = df_special[1][tmcv]
            dict3['risk'] = ify3
            dict3['start_prediction_time'] = dt.datetime.now()
            print('dict3 = {}'.format(dict3))
            list1.append(dict3)
        else:
            print('len(ctr.most_common(3)) < 3')
                  
        print('most common condition end')

    except Exception as e:
        print('Final list1 exception:', list1)
        print(f"exception throws: {e}")
        
    print('main end')
    print('in main ', list1)
    print('Final list1 before return:', list1)
    return list1
