#%% Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
np.set_printoptions(suppress=True)
plt.style.use('ggplot')

#%% Load Data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   #%% Data load
res = pd.read_csv('props_new\\cluster_reorder.csv')

#%%Defining constants to plot.
med_i = np.median(res['celli'])
med_j = np.median(res['cellj'])
med_k = np.median(res['cellk'])

res['cluster 1 ou 2'] = 1-res['cluster 0']

#%% Functions

def plot_map(df,depth,prop,const_col='cellk',x='xcoord',y='ycoord',cbarlabel=None,profile=True,plot_type=None,num_colors=3,cmap=None,savefile=None):
    const_val = depth
    color_dim = prop
    plot_data = df.loc[df[const_col] == const_val]
    # sample_size=1000
    # plot_data = plot_data.sample(n=sample_size)
    depth = np.mean(plot_data['zcoord'])
    line = plot_data.loc[plot_data['cellj'] == np.median(plot_data['cellj'])]

    if plot_type == 'discrete': 
        if cmap == None: cmap = 'Accent_r'
        c_map = plt.get_cmap(cmap, num_colors)
    elif plot_type == 'continuous':
        if cmap == None: cmap = 'viridis'
        c_map = plt.get_cmap(cmap)
    
    if profile == False:
        fig = plt.figure(figsize=[8,8])
    else:
        fig = plt.figure(figsize=[8,10])

    gs = fig.add_gridspec(50,10)    

    if profile == True:
        prof_data = df.loc[df['cellj'] == np.median(plot_data['cellj'])]
        # sample_size=1000
        # prof_data = prof_data.sample(n=sample_size)

        minz = np.min(prof_data['zcoord'])
        maxz = np.max(prof_data['zcoord'])
        mink = np.min(prof_data['cellk'])
        maxk = np.max(prof_data['cellk'])
        dx = np.max(plot_data[x])-np.min(plot_data[x])
        dy = np.max(plot_data[y])-np.min(plot_data[y])
        hyp = np.round(np.sqrt(dx**2+dy**2)/1000,0)*1000
        minx = np.min(prof_data[x])
        maxx = np.max(prof_data[x])
        medx = np.median(prof_data[x])

        ax1 = fig.add_subplot(gs[0:35,:])
        ax2 = fig.add_subplot(gs[43:,:])
        px = prof_data[x].values
        py = prof_data['cellk'].values
        pz = prof_data[color_dim].values
        ax2.scatter(px,py,c=pz,cmap=c_map,alpha=0.55,marker='.',s=50)
        
        ax2.set_xlabel('Distância (m)')
        ax2.set_ylabel('Profundidade (m)')
        ax2.set_yticks(ticks=[mink,maxk])
        ax2.set_xticks(ticks=[minx,medx,maxx])
        ax2.set_yticklabels(labels=[str(minz),str(maxz)])
        ax2.set_xticklabels(labels=['0',str(hyp/2),str(hyp)])
        ax2.set_title('Perfil')
        ax1.plot(line[x],line[y],c='red',label='Perfil')

    else:
        ax1 = fig.add_subplot(gs[:,:])


    px = plot_data[x].values
    py = plot_data[y].values
    pz = plot_data[color_dim].values
    propmap = ax1.scatter(px,py,c=pz,cmap=c_map,marker='.',s=50,alpha=0.55)

    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_title('Profundidade = '+str(np.round(depth,2))+'m')
    ax1.legend()


    if cbarlabel == None:
        cbarlabel = color_dim

    if plot_type == 'discrete': 
        cb = fig.colorbar(propmap,ticks=range(num_colors),ax=ax1)
    elif plot_type == 'continuous':
        cb = fig.colorbar(propmap,ax=ax1)
    cb.set_label(label=cbarlabel,size='large', weight='bold')
    cb.ax.tick_params(labelsize='large')

    plt.tight_layout()

# plot_map(res,med_k,'cluster 0',plot_type='continuous')
# plot_map(res,med_k,'cluster 1',plot_type='continuous')
# plot_map(res,med_k,'cluster 2',plot_type='continuous')
# plot_map(res,med_k,'cluster 1 ou 2',plot_type='continuous',cbarlabel='Probabilidade Cluster 1 ou 2')
plot_map(res,med_k,'GMM',plot_type='discrete',cbarlabel='Clusters Gussian Mixture Model')
plot_map(res,med_k,'KMeans',plot_type='discrete',cbarlabel='Clusters K-Means')
# plot_map(res,med_k,'sw',plot_type='continuous')
# plot_map(res,med_k,'phie',plot_type='continuous')
# plot_map(res,med_k,'rhob',plot_type='continuous')
# plot_map(res,med_k,'gr',plot_type='continuous')
# plot_map(res,med_k,'dt',plot_type='continuous')


# %%
