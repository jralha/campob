#%% Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(suppress=True)
plt.style.use('ggplot')

#%% Load Data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   #%% Data load
res = pd.read_csv('campob\\csv_correcao\\cluster_reorder.csv')

#%% Functions

def plot_section_discrete(df,const_col,const_val,x,y,color_dim,num_colors=3,cmap='magma'):
    plot_data = df.loc[df[const_col] == const_val]

    c_map = plt.get_cmap(cmap, num_colors)

    plt.figure(figsize=[10,4])
    plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=c_map)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(const_col+" = "+str(const_val))
    plt.colorbar(ticks=range(num_colors),label=color_dim)


def plot_section_continuous(df,const_col,const_val,x,y,color_dim,cmap='viridis'):
    plot_data = df.loc[df[const_col] == const_val]

    plt.figure(figsize=[10,4])
    plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=cmap)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(const_col+" = "+str(const_val))
    plt.colorbar(label=color_dim)

#%%Defining good constants to plot.
med_i = np.median(res['i'])
med_j = np.median(res['j'])
med_k = np.median(res['k'])


#%%
plot_section_continuous(res,'k',med_k,'i','j','cluster 0')
plot_section_continuous(res,'k',med_k,'i','j','cluster 1')
plot_section_continuous(res,'k',med_k,'i','j','cluster 2')
plot_section_discrete(res,'k',med_k,'i','j','GMM')
plot_section_discrete(res,'k',med_k,'i','j','KMeans')
plot_section_continuous(res,'k',med_k,'i','j','SW')
plot_section_continuous(res,'k',med_k,'i','j','phie')

#%%
