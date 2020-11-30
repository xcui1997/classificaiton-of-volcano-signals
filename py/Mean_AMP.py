import numpy as np
import pickle
import matplotlib.pyplot as plt


def Mean_plot(amp, idx_cls, imin, mean_amp, name, plot_mean=True):
    plt.plot(amp[idx_cls, :][imin, :], linewidth=1, c='#333333')
    if plot_mean:
        plt.plot(mean_amp, linewidth=1, c='#FF3333')
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    figtitle = 'Cluster #'+str(i)+' ('+str(len(idx_cls))+' STFs)'
    plt.text(0.01, 0.99, 'Cluster #'+str(i),
             fontsize=10, fontweight='bold',
             horizontalalignment='left',
             verticalalignment='center',
             transform=ax.transAxes )
    plt.text(0.99, 0.99, '('+str(len(idx_cls))+')',
             horizontalalignment='right',
             verticalalignment='center',
             fontsize=10, transform=ax.transAxes )
    plt.savefig('../output/'+name+'.svg', format='svg')
    plt.savefig('../output/'+name+'.png', format='png')



if __name__ == '__main__':

    Mean_amp_container = []
    Mean_data_container = []
    labels = pickle.load(open('../output/pkl/labels_stfre.pkl', 'rb'))
    amps = pickle.load(open('../output/pkl/amp_container.pkl', 'rb'))
    data = pickle.load(open('../output/pkl/timeseries_container.pkl','rb'))
    X = pickle.load(open('../output/pkl/EM_dist_amp.pkl', 'rb'))
    #sort_idx = pickle.load(open('../output/pkl/sort_idx.pkl','rb'))
    sort_idx = [0, 1, 2, 3, 4, 5, 6, 7 ,8 , 9, 10, 
                11, 12, 13, 14, 15, 16, 17, 18, 19]
    # loop over each cluster
    fig = plt.figure(figsize=(8, 10))
    for i in range(len(sort_idx)):

        # retrieve the cluster members
        idx_cls = np.where(labels == sort_idx[i])[0]
        X_cls = X[idx_cls, :][:, idx_cls]
        # find the reference smediantf (closest to the cls center)
        # i.e., the one with min distance from other group members
        median_dist = np.median(X_cls, axis=1)
        imin = np.argmin(median_dist) # locade of the min 

        mean_amp = np.zeros(amps.shape[1])
        mean_data = np.zeros(data.shape[1])
 
        ax = plt.subplot(5, 4, i+1)
        
        for j in idx_cls:
            
            mean_amp += amps[j,:]
            mean_data += data[j,:]
            
        mean_amp = mean_amp / len(idx_cls)
        mean_data = mean_data / len(idx_cls)
        
        Mean_amp_container.append(mean_amp)
        Mean_data_container.append(mean_data)
        
        Mean_plot(amps, idx_cls, imin, mean_amp, 'amp', plot_mean=True)
       # Mean_plot(data, idx_cls, imin, mean_data, 'time_seies', plot_mean=False)
 
    pickle.dump(np.asarray(Mean_amp_container), open('../output/pkl/Mean_amp_container.pkl','wb'))
   # pickle.dump(np.asarray(Mean_data_container), open('../output/pkl/Mean_data_container.pkl','wb'))
    plt.show()
