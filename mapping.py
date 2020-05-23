#%% Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(suppress=True)
plt.style.use('ggplot')

#%% Load Data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   #%% Data load
res = pd.read_csv('props_new\\cluster_reorder.csv')

#%%Defining good constants to plot.
med_i = np.median(res['celli'])
med_j = np.median(res['cellj'])
med_k = np.median(res['cellk'])

res['cluster 1 ou 2'] = 1-res['cluster 0']

#%% Functions

def plot_section(df,const_col,const_val,x,y,color_dim,orientation,plot_type=None,num_colors=None,cmap='magma',sz=15,savefile=None):
    plot_data = df.loc[df[const_col] == const_val]

    if orientation == 'depth':
        plt.figure(figsize=[8,8])
    elif orientation == 'vertical':
        plt.figure(figsize=[10,2])

    if plot_type == 'discrete': 
        c_map = plt.get_cmap(cmap, num_colors)
        plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=c_map,s=sz)
        plt.colorbar(ticks=range(num_colors),label=color_dim)
    elif plot_type == 'continuous':
        plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=cmap,s=sz)
        plt.colorbar(label=color_dim)

    
    plt.xlabel(x)
    plt.ylabel(y)
    
    plt.show()


#%%
plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 0','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 1','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 2','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 1 ou 2','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','GMM','depth',plot_type='discrete',num_colors=3)
# plot_section(res,'cellk',med_k,'xcoord','ycoord','KMeans','depth',plot_type='discrete',num_colors=3)
# plot_section(res,'cellk',med_k,'xcoord','ycoord','sw','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','phie','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','rhob','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','gr','depth',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','dt','depth',plot_type='continuous')

#%%
plot_section(res,'cellj',med_j,'xcoord','zcoord','cluster 0','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','cluster 1','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','cluster 2','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','cluster 1 ou 2','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','GMM','vertical',plot_type='discrete',num_colors=3)
plot_section(res,'cellj',med_j,'xcoord','zcoord','KMeans','vertical',plot_type='discrete',num_colors=3)
plot_section(res,'cellj',med_j,'xcoord','zcoord','sw','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','phie','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','rhob','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','gr','vertical',plot_type='continuous')
plot_section(res,'cellj',med_j,'xcoord','zcoord','dt','vertical',plot_type='continuous')


# %%
