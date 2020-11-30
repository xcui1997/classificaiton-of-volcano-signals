import numpy as np
import pickle

if __name__ == '__main__':
    
    location = pickle.load(open('../output/pkl/events_location.pkl', 'rb'))
    #sort_idx = pickle.load(open('../output/pkl/sort_idx.pkl', 'rb'))
    sort_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19]
    labels = np.array(location)[:,6]
    f1 = open('../output/txt/clusterA.dat','w')
    f2 = open('../output/txt/clusterB.dat','w')
    f3 = open('../output/txt/clusterC.dat','w')
    f4 = open('../output/txt/clusterD.dat','w')
    f5 = open('../output/txt/clusterE.dat','w')
    print(len(labels))
    for i in range(len(sort_idx)):
    # six cluster
        idx_cls = np.where(labels == str(sort_idx[i]))[0]
        if i == 0 or i == 6 or i == 7 or i == 10 or i == 11 or i == 13 or i == 14 or i == 15 or i == 17 or i == 19:
            for j in range(len(idx_cls)):
                f1.write(location[idx_cls[j]][1]+'  '+location[idx_cls[j]][0]+'  '+location[idx_cls[j]][2]+'  '+location[idx_cls[j]][3]+'  '+location[idx_cls[j]][4]+'  '+location[idx_cls[j]][5]+'\n' )
        elif i == 2 or i == 8 or i == 12:
            for j in range(len(idx_cls)):
                f2.write(location[idx_cls[j]][1]+'  '+location[idx_cls[j]][0]+'  '+location[idx_cls[j]][2]+'  '+location[idx_cls[j]][3]+'  '+location[idx_cls[j]][4]+'  '+location[idx_cls[j]][5]+'\n' )
        elif i == 4 or i == 9 or i ==16:
            for j in range(len(idx_cls)):
                f3.write(location[idx_cls[j]][1]+'  '+location[idx_cls[j]][0]+'  '+location[idx_cls[j]][2]+'  '+location[idx_cls[j]][3]+'  '+location[idx_cls[j]][4]+'  '+location[idx_cls[j]][5]+'\n' )
        elif i == 1 or i == 5:
            for j in range(len(idx_cls)):
                f4.write(location[idx_cls[j]][1]+'  '+location[idx_cls[j]][0]+'  '+location[idx_cls[j]][2]+'  '+location[idx_cls[j]][3]+'  '+location[idx_cls[j]][4]+'  '+location[idx_cls[j]][5]+'\n' )
        
        else:
            for j in range(len(idx_cls)):
                f5.write(location[idx_cls[j]][1]+'  '+location[idx_cls[j]][0]+'  '+location[idx_cls[j]][2]+'  '+location[idx_cls[j]][3]+'  '+location[idx_cls[j]][4]+'  '+location[idx_cls[j]][5]+'\n' )   
# twenty cluster
        with open('../sh/Cls.dat/cluster'+str(i)+'.dat', 'w') as f:
            for j in range(len(idx_cls)):
                f.write(location[idx_cls[j]][1]+'  '+location[idx_cls[j]][0]+'  '+location[idx_cls[j]][2]+'  '+location[idx_cls[j]][3]+'  '+location[idx_cls[j]][4]+'  '+location[idx_cls[j]][5]+'\n' )


    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
