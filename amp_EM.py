import pickle
import matplotlib.pyplot as plt
import numpy as np
from time import time
from math import sqrt


if __name__ == '__main__':

    amp = pickle.load(open('../output/pkl/amp_container.pkl', 'rb'))
    num_amp, len_amp = amp.shape
    num_trial = num_amp
    mdist_amp = np.zeros((num_trial, num_trial))
    print('data shape:', amp.shape)

    starttime = time()
  
    for i in range(num_trial):
        for j in range(i+1, num_trial):
            dist_amp = np.sum((amp[i,:]-amp[j,:])**2)
            mdist_amp[i, j] = dist_amp
            mdist_amp[j, i] = dist_amp

    pickle.dump(mdist_amp, open('../output/pkl/EM_dist_amp.pkl', 'wb'))
    print('time: ', time()-starttime)

