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
RANDOM_SEED=42
data=np.load('data.npy')
df = pd.DataFrame(data)
with pm.Model() as ar1:
    # assumes 95% of prob mass is between -2 and 2
    rho = pm.Normal("rho", mu=0.0, sigma=1.0, shape=2)
    # precision of the innovation term
    tau = pm.Exponential("tau", lam=0.5)

    likelihood = pm.AR(
        "y", rho=rho, tau=tau, constant=True, init_dist=pm.Normal.dist(0, 10), observed=df[2]
    )

    idata = pm.sample(1000, tune=2000, random_seed=RANDOM_SEED)
