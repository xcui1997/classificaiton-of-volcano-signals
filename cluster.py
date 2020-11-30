import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import pickle
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage


def clust_stats(clust, draw=False):
    labels = np.unique(clust.labels_)
    n_clusters = len(labels)
    counts = np.zeros(n_clusters, dtype='int')
    for i in range(n_clusters):
        idx = np.where(clust.labels_ == labels[i])[0]
        counts[i] = len(idx)
    if draw:
        fig = plt.figure()
        plt.bar(np.arange(n_clusters), counts)
        for i in range(n_clusters):
            plt.text(i, counts[i], str(counts[i]),
                     horizontalalignment='center',
                     verticalalignment='bottom')
        plt.xticks(np.arange(n_clusters))
        title = '.'.join(['../output/hist', 'png'])
        plt.savefig(title, format='png')
        plt.close()
    return counts


def plot_rep(clust, stfs, name):
    labels = np.unique(clust.labels_)
    num_rep = 100
    mx, my = 10, 10
    sort_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19]
   # sort_idx = pickle.load(open('../output/pkl/sort_idx.pkl', 'rb'))
    for label in labels:
        idx = np.where(clust.labels_ == sort_idx[label])[0]
        if len(idx)>num_rep:
            sel_idx = idx[np.random.choice(len(idx), num_rep)]
        else:
            sel_idx = idx
        fig = plt.figure()
        for i in range(len(sel_idx)):
            plt.subplot(mx, my, i+1)
            plt.plot(stfs[idx[i], :]/np.max(stfs[idx[i], :]), c='k', linewidth=1.0)
            plt.axis('off')
        title1 = 'Cluster #' + str(label)
        title2 = ' ('+str(len(idx))+'vol_seismics)'
        fig.suptitle(title1+title2, fontsize=15)
        title = '../output/cls_png/'+str(label)+name+'png'
        plt.savefig(title, format='png')
        plt.close()


if __name__ == '__main__':

  
    data_container = pickle.load(open('../output/pkl/timeseries_container.pkl','rb'))
    X = pickle.load(open('../output/pkl/EM_dist_amp.pkl', 'rb'))
    m, n = X.shape
    amps = pickle.load(open('../output/pkl/amp_container.pkl', 'rb'))
    num_amp, len_amp = amps.shape
    print(num_amp, len_amp)
    n_cls = 20

    # Dendrogram
    X_vec = squareform(X)
    linkage_matrix = linkage(X_vec, "complete") 
    plt.figure(figsize=(12, 6))
    dendrogram(linkage_matrix, p=n_cls, truncate_mode="lastp") 
    plt.ylabel('amp distance', fontsize=20)
    plt.title("Dendrogram with "+str(n_cls)+" clusters")
    plt.savefig('../output/dendrogram.png', format='png')

    # Agglomerative Clustering
    clust = AgglomerativeClustering(n_clusters=n_cls,
                                    linkage='complete',
                                    affinity='precomputed').fit(X)
    pickle.dump(clust.labels_, open('../output/pkl/labels_stfre.pkl', 'wb'))
    counts = clust_stats(clust, draw=True)
    type1 = 'magnitude'
    type2 = 'timeseries'
    plot_rep(clust, amps, type1)
   # plot_rep(clust, data_container, type2)
