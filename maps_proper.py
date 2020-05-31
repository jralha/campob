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
def plot_section(df,const_col,const_val,x,y,color_dim,plot_type=None,num_colors=3,cmap='plasma',sz=15,savefile=None):
    plot_data = df.loc[df[const_col] == const_val]
    # return plot_data

    plt.figure(figsize=[8,8])


    plt.title('Profundidade = '+str(np.round(np.mean(plot_data['zcoord']),2))+' m')

    if plot_type == 'discrete': 
        c_map = plt.get_cmap('magma',num_colors)
        plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=c_map,s=sz)
        plt.colorbar(ticks=range(num_colors),label=color_dim)
    elif plot_type == 'continuous':
        plt.scatter(plot_data[x],plot_data[y],c=plot_data[color_dim],cmap=cmap,s=sz)
        plt.colorbar(label=color_dim)

    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plt.show()


# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 0',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 1',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 2',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','cluster 1 ou 2',plot_type='continuous')
plot_section(res,'cellk',med_k,'xcoord','ycoord','GMM',plot_type='discrete')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','KMeans',plot_type='discrete')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','sw',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','phie',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','rhob',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','gr',plot_type='continuous')
# plot_section(res,'cellk',med_k,'xcoord','ycoord','dt',plot_type='continuous')



# %%
