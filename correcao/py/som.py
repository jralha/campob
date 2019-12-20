#%%Libraries
import pandas as pd
from minisom import MiniSom 
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
from tqdm.auto import tqdm
np.set_printoptions(suppress=True)
plt.style.use('ggplot')
plt.style.use('dark_background')

#%%Load Data
res = pd.read_csv('campob\\csv_correcao\\cluster_reorder.csv')

#Define Features
features = res[['phie','GR','RHOB']]

scaler = StandardScaler()
data=scaler.fit_transform(features)
feature_names = features.columns

m=5*np.sqrt(len(features))
n=int(np.sqrt(m))
size = len(feature_names)

#%%SOM
som = MiniSom(n, n, size,neighborhood_function='gaussian', sigma=5, random_seed=1,learning_rate=0.5) # Initialization of nxn SOM
som.pca_weights_init(data) #Starting weights from first two Principal Components
som.train_random(data, 200) #100 training iterations


w = som.get_weights() #Get weights, this will be a n x n x f tensor where f is the number of features


fig = plt.figure(figsize=(8,10))
for i,feat in enumerate(features):
   plt.subplot(3,2,i+1)
   plt.title(feat)
   im = plt.imshow(w.T[i],cmap='viridis',origin='lower')
   plt.colorbar()
# Uncomment to plot distance map at the end
plt.subplot(3,2,4)
plt.title('Matriz de Distâncias')
im = plt.imshow(som.distance_map(),cmap='viridis',origin='lower')
plt.colorbar()

# %%
