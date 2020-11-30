import pickle
import matplotlib.pyplot as plt
import numpy as np


only_time = []
def time_order(name):
    num_name = len(name)
    Neworder = np.zeros(num_name)
    for i in range(num_name):
        time_of_data = name[i].split('/')[-1]
        time_of_data = time_of_data.split('.')[0] 
        time_nmlz = time_of_data[0:4] + '-' + time_of_data[4:6] + '-' + time_of_data[6:8] + '-'  \
                    + time_of_data[8:10] + ':' + time_of_data[10:12] + ':' + time_of_data[12:14] \
                    + '.' +time_of_data[14:17]
        Neworder[i] = int(time_of_data)
        only_time.append(time_nmlz)
    idx = np.argsort(Neworder)
    return idx

   

if __name__ == '__main__':
    mdist = pickle.load(open('../output/pkl/EM_dist_amp.pkl', 'rb'))
    name_all = pickle.load(open('../output/pkl/name_container.pkl','rb'))
    idx = time_order(name_all)
    mdist = mdist[idx, :]
    mdist = mdist[:, idx] # replace
    print(mdist.shape)
    
    pickle.dump(np.asarray(only_time), open('../output/pkl/only_time.pkl','wb'))
    plt.figure(figsize=(6, 8))
    plt.subplot(2, 1, 1)
    plt.hist(mdist.flatten(), bins=100)
    plt.xlabel('amp distance', fontsize=15)
    plt.ylabel('Number of amp pairs', fontsize=15)
    plt.xlim([0,300])
    plt.subplot(2, 1, 2)
    im = plt.imshow(mdist, origin='lower', cmap='RdBu',
               vmin=0, vmax=100)
    plt.xlabel('amplitude spectrum', fontsize=15)
    plt.ylabel('amplitude spectrum', fontsize=15)
    cb = plt.colorbar(im, ticks=[0.0, 20, 40, 60, 80], orientation='vertical')
    cb.set_label('dissimilarity', fontsize=15)
    plt.show()

