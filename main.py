import warnings
warnings.filterwarnings('ignore'  )


from pathlib import Path
import pickle
from collections import OrderedDict
import pandas as pd

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
def main2():
    RANDOM_SEED=42
    data=np.load('data.npy')
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

    with ar1:
        predictions = pm.sample_posterior_predictive(idata, predictions=True).predictions

#print(predictions.y[0])
    np.savetxt('sample.csv',predictions.y[0],delimiter=",")

    df=pd.read_csv("sample.csv")
    temp= list(df.columns)
    df = df.T.reset_index(drop=True).T
    df1 = pd.concat([pd.DataFrame(data=[temp]),df],ignore_index=True)
    stat=[]
    for i in range(0,df1.shape[1]):
        stat.append( df[i].lt(0).idxmax())

    array=np.array(stat)
    ctr=Counter(array)
    fmcv, ify1 = ctr.most_common(1)[0]
    smcv, ify2 = ctr.most_common(2)[1]
    tmcv, ify3 = ctr.most_common(3)[2]
    return(df_special[0],df_special[1],fmcv,ify1,smcv,ify2,tmcv,ify3)
