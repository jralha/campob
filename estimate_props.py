#%%
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# %%
quis = pd.read_csv('props_new\\quis.csv')
res = pd.read_csv('props_new\\res.csv')

well = quis.loc[ (quis['sw_well'] != 0.0) & (quis['gr_well'] != 0.0) ]

#%%

cell_range=2
grid_size = ((2*cell_range)+1)**2
edata = np.zeros((len(well)*grid_size,8))

#%%
ei = 0
for index,row in tqdm(well.iterrows()):
    rk = row['cellk']
    ri = row['celli']
    rj = row['cellj']
    for ip in range(cell_range+1):
        temp_i = ri + ip
        for jp in range(cell_range+1):
            temp_j = rj + jp

            df = quis.loc[ (quis['cellk']==rk) & (quis['celli']== temp_i) & (quis['cellj'] == temp_j)    ]

            edata[ei,0] = np.mean(df['seis'].values)
            edata[ei,1] = np.mean(df['anttrracking'].values)
            edata[ei,2] = np.mean(df['dist_fault'].values)
            edata[ei,3] = np.mean(row['sw'])
            edata[ei,4] = np.mean(row['dt'])
            edata[ei,5] = np.mean(row['phie'])
            edata[ei,6] = np.mean(row['rhob'])
            edata[ei,7] = np.mean(row['gr'])
            ei = ei+1

    for nip in range(cell_range):
        temp_i = ri - (nip+1)
        for njp in range(cell_range):
            temp_j = rj - (njp+1)
            df = quis.loc[ (quis['cellk']==rk) & (quis['celli']==temp_i) & (quis['cellj'] ==temp_j)    ]

            edata[ei,0] = np.mean(df['seis'].values)
            edata[ei,1] = np.mean(df['anttrracking'].values)
            edata[ei,2] = np.mean(df['dist_fault'].values)
            edata[ei,3] = np.mean(row['sw'])
            edata[ei,4] = np.mean(row['dt'])
            edata[ei,5] = np.mean(row['phie'])
            edata[ei,6] = np.mean(row['rhob'])
            edata[ei,7] = np.mean(row['gr'])
            ei = ei+1

#%%
nonzeros=edata[~np.all(edata == 0, axis=1)]
X = nonzeros[:,0:3]
Ys = nonzeros[:,3:]
props = ['sw','dt','phie','rhob','gr']

#%%
cv=10

est = xgb.XGBRegressor(
    max_depth=15,
    learning_rate=0.01,
    n_estimators=10000,
    verbosity=0,
    n_jobs=-1,
)

prop_preds=[]
prop_scores=[]
for nprop,prop in enumerate(props):
    Y = Ys[:,nprop]
    ##scaler = MinMaxScaler()
    #X = scaler.fit_transform(X)
    #Y = scaler.fit_transform(Y)

    scores=[]
    best_score=0
    for fold in tqdm(range(cv)):
        X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2)

        est.fit(X_train,y_train)

        temp_preds = est.predict(X_test)
        score = (r2_score(y_test,temp_preds))
        scores.append(score)
        print(score)
        if score > best_score:
            best_score = score
            preds = temp_preds

    prop_preds.append(preds)
    prop_scores.append(best_score)

    print("\nStats for "+prop+" prediction.")
    print("Best score: "+str(best_score))
    print("Avg score: "+str(np.mean(scores)))

# %%
