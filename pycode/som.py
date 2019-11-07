#%%Libraries
import pandas as pd
from tf_som.tf_som import SelfOrganizingMap
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix
import tensorflow as tf
from tqdm.auto import tqdm
np.set_printoptions(suppress=True)
plt.style.use('ggplot')

#%%Functions
def get_umatrix(weights, m, n):
    umatrix = np.zeros((m * n, 1))
    # Get the location of the neurons on the map to figure out their neighbors. I know I already have this in the
    # SOM code but I put it here too to make it easier to follow.
    neuron_locs = list()
    for i in range(m):
        for j in range(n):
            neuron_locs.append(np.array([i, j]))
    # Get the map distance between each neuron (i.e. not the weight distance).
    neuron_distmat = distance_matrix(neuron_locs, neuron_locs)

    for i in range(m * n):
        # Get the indices of the units which neighbor i
        neighbor_idxs = neuron_distmat[i] <= 1  # Change this to `< 2` if you want to include diagonal neighbors
        # Get the weights of those units
        neighbor_weights = weights[neighbor_idxs]
        # Get the average distance between unit i and all of its neighbors
        # Expand dims to broadcast to each of the neighbors
        umatrix[i] = distance_matrix(np.expand_dims(weights[i], 0), neighbor_weights).mean()

    return umatrix.reshape((m, n))

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
som = SelfOrganizingMap(m=m,n=n,dim=2,max_epochs=20)
init_op = tf.global_variables_initializer()
session.run([init_op])
som.train(num_inputs=size)

#%% Plots
#fig = plt.figure(figsize=(8,10))
#for i,feat in enumerate(features):
#    plt.subplot(3,2,i+1)
#    plt.title(feat)
#    im = plt.imshow(w.T[i],cmap='viridis',origin='lower')
#    plt.colorbar()
#Uncomment to plot distance map at the end
#plt.subplot(3,2,4)
plt.title('Matriz de Distâncias')
im = plt.imshow(som.distance_map(),cmap='viridis',origin='lower')
plt.colorbar()

#%%
