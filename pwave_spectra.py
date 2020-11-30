import math
import numpy as np
from obspy import read
import glob
from obspy.signal.trigger import recursive_sta_lta
import pickle
import matplotlib.pyplot as plt

def SNR(trace, arr, win, tol=0.5):
    trace.filter(type='bandpass', freqmin=1, freqmax=15)
    Mean = trace.data.mean()
    narr = int(arr * trace.stats.sampling_rate)
    nwin = int(win * trace.stats.sampling_rate)
    ntol = int(tol * trace.stats.sampling_rate)

    noise_e = np.sum((trace.data[narr-nwin:narr-ntol]-Mean)**2)
    signal_e = np.sum((trace.data[narr+ntol:narr+nwin]-Mean)**2)
    return 10*math.log10(signal_e/noise_e)

def amp_nmlz(fz,x):
    fz_nmlz = fz / fz[-1]
    x_int = np.sum(x) * (fz[1]-fz[0])
    x_nmlz = x / x_int *fz[-1]
    return x_nmlz, fz_nmlz


def fft_amp(trace, arr, win_lenth):
    narr = int(arr * trace.stats.sampling_rate)
    nwin = int(win_lenth * trace.stats.sampling_rate)
    data_remean=trace.data[narr-nwin:narr+nwin]-trace.data.mean()
    sp = np.fft.fft(data_remean)
    freq = np.fft.fftfreq(len(data_remean), d=1.0/trace.stats.sampling_rate)
    amp = np.abs(sp)
    A_upper = np.mean(amp[(freq>5.0) & (freq<15.0)])
    A_lower = np.mean(amp[(freq>1.0) & (freq<4.0)])
    return amp[(freq>=0) & (freq<15.0)], freq[(freq>=0) & (freq<15.0)], data_remean, math.log10(A_upper/A_lower)

 
#find the max and find the early to the place with the largest slope near it
def picker(trace, nsta=10, nlta=100):
    stalta = recursive_sta_lta(trace.data, nsta, nlta)
    n_max = np.argmax(stalta)
    quality = stalta[n_max]
    n_onset = int(0.5 * trace.stats.sampling_rate)
    n_diff_max = np.argmax(np.diff(stalta[n_max-n_onset:n_max+n_onset]))
    n_pick = n_max - n_onset + n_diff_max
    arr = n_pick / trace.stats.sampling_rate
    return  arr, quality


if __name__ == '__main__':
    snr_thres = 3 # in db
    win_snr = 2.5
    win_lenth = 1.28
    amp_container = []
    data_container = []
    name_container = []
    fi_container = []
    for sacname in glob.glob("data/*/*.SAC"):
        tr = read(sacname)[0]
        tr.filter(type='bandpass', freqmin=1, freqmax=15)
        t = np.arange(tr.stats.npts) / tr.stats.sampling_rate
        p_arr, quality = picker(tr)

  
        if p_arr > win_snr and p_arr < t[-1]-win_snr and quality > snr_thres:
        
            snr_value = SNR(tr, p_arr, win_snr)
            if snr_value > snr_thres:
      
                amp,freq,Data,fi = fft_amp(tr, p_arr, win_lenth)
                Amp_nmlz,freq_nmlz = amp_nmlz(freq, amp)
                amp_container.append(Amp_nmlz)
                data_container.append(Data)
                name_container.append(sacname)
                fi_container.append(fi)

    bins_ = np.linspace(-1.5, 1, 30)
    plt.hist(fi_container, bins=bins_, edgecolor='k')
    plt.show()
    pickle.dump(np.asarray(amp_container), open('../output/pkl/amp_container.pkl','wb'))
    pickle.dump(np.asarray(data_container), open('../output/pkl/TimeSeries_container.pkl','wb'))
    pickle.dump(np.asarray(name_container), open('../output/pkl/name_container.pkl','wb'))
    pickle.dump(np.asarray(fi_container), open('../output/pkl/fi_container.pkl','wb'))

