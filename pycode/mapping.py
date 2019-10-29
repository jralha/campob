#%% Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(suppress=True)
plt.style.use('ggplot')

#%% Load Data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   #%% Data load
res = pd.read_csv('campob\\csv_correcao\\cluster_reorder.csv')

#%% Functions

def plot_section_discrete(df,const_col,const_val,x,y,color_dim,orientation,num_colors=3,cmap='magma',sz=15):
    plot_data = df.loc[df[const_col] == const_val]

    c_map = plt.get_cmap(cmap, num_colors)

    plt.figure(figsize=[10,3])
    plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=c_map,s=sz)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.colorbar(ticks=range(num_colors),label=color_dim)
    plt.show()


def plot_section_continuous(df,const_col,const_val,x,y,color_dim,orientation,cmap='viridis',sz=15):
    plot_data = df.loc[df[const_col] == const_val]

    plt.figure(figsize=[10,3])
    plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=cmap,s=sz)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.colorbar(label=color_dim)
    plt.show()

#%%Defining good constants to plot.
med_i = np.median(res['i'])
med_j = np.median(res['j'])
med_k = np.median(res['k'])

res['cluster 1 ou 2'] = 1-res['cluster 0']

#%%
plot_section_continuous(res,'k',med_k,'X','Y','cluster 0','depth')
plot_section_continuous(res,'k',med_k,'X','Y','cluster 1','depth')
plot_section_continuous(res,'k',med_k,'X','Y','cluster 2','depth')
plot_section_continuous(res,'k',med_k,'X','Y','cluster 1 ou 2','depth')
plot_section_discrete(res,'k',med_k,'X','Y','GMM','depth')
plot_section_discrete(res,'k',med_k,'X','Y','KMeans','depth')
plot_section_continuous(res,'k',med_k,'X','Y','SW','depth')
plot_section_continuous(res,'k',med_k,'X','Y','phie','depth')

#%%
plot_section_continuous(res,'j',med_j,'i','k','cluster 0','vertical')
plot_section_continuous(res,'j',med_j,'i','k','cluster 1','vertical')
plot_section_continuous(res,'j',med_j,'i','k','cluster 2','vertical')
plot_section_continuous(res,'j',med_j,'i','k','cluster 1 ou 2','vertical')
plot_section_discrete(res,'j',med_j,'i','k','GMM','vertical')
plot_section_discrete(res,'j',med_j,'i','k','KMeans','vertical')
plot_section_continuous(res,'j',med_j,'i','k','SW','vertical')
plot_section_continuous(res,'j',med_j,'i','k','phie','vertical')


# %%
