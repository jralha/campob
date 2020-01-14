#%%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm.auto import tqdm
from tpot import TPOTRegressor
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

#%%
quis = pd.read_csv('props_new\\quis.csv')

#%%
well = quis.loc[ (quis['sw_well'] != 0.0) & (quis['gr_well'] != 0.0) & (quis['phie_well'] != 0.0) & (quis['rhob_well'] != 0.0) & (quis['dt_well'] != 0.0) ]

#%%
scaler = MinMaxScaler(feature_range=(0,1))
scaled = scaler.fit_transform(well)
scaled = pd.DataFrame(scaled)
scaled.columns = well.columns
X = scaled[['anttrracking','seis','dist_fault']]
props = ['sw_well','dt_well','phie_well','rhob_well','gr_well']
Y = well[props[0]]

#%%
sns.pairplot(well[['anttrracking','seis','dist_fault','sw_well','dt_well','phie_well','rhob_well','gr_well']])

#%%
ckp = 'ckp\\'
t_pot = TPOTRegressor(periodic_checkpoint_folder=ckp,verbosity=2,scoring='r2',cv=10,n_jobs=-1)

#X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2)
t_pot.fit(X,Y)
t_pot.export(ckp+'test.py')

# %%
preds = t_pot.predict(X)

plt.scatter(preds,Y)