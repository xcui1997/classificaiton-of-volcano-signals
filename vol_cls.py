import math
import numpy as np
from obspy import read
import glob
import matplotlib.pyplot as plt
from obspy.signal.trigger import recursive_sta_lta


def SNR(trace, arr, win, tol=0.5):
    narr = int(arr * trace.stats.sampling_rate)
    nwin = int(win * trace.stats.sampling_rate)
    ntol = int(tol * trace.stats.sampling_rate) # tolerance of pick uncertainty
    noise_e = np.sum(trace.data[narr-nwin-ntol:narr-ntol]**2)
    signal_e = np.sum(trace.data[narr+ntol:narr+nwin+ntol]**2)
    return 10*math.log10(signal_e/noise_e)


def fft_amp(x, smpr):
    sp = np.fft.fft(x)
    freq = np.fft.fftfreq(len(x), d=1.0/smpr) 
    amp = np.abs(sp)
    return amp[freq>0.0], freq[freq>0.0] # take positive half


def fi(trace, arr, win):
    narr = int(arr * trace.stats.sampling_rate)
    nwin = int(win * trace.stats.sampling_rate)
    amp, freq = fft_amp(trace.data[narr-nwin:narr+nwin],
                        trace.stats.sampling_rate)
    A_upper = np.mean(amp[(freq>5.0) & (freq<15.0)])
    A_lower = np.mean(amp[(freq>1.0) & (freq<5.0)])
    return math.log10(A_upper/A_lower)


def picker(trace, nsta=10, nlta=100):
    stalta = recursive_sta_lta(trace.data, nsta, nlta)
    n_max = np.argmax(stalta)
    quality = stalta[n_max]
    n_onset = int(0.5 * trace.stats.sampling_rate)
    n_diff_max = np.argmax(np.diff(stalta[n_max-n_onset:n_max+n_onset]))
    n_pick = n_max - n_onset + n_diff_max
    arr = n_pick / trace.stats.sampling_rate
    return  arr, quality


snr_thres = 3.0 # in db
win = 3.0 # window length to calculate snr
freq_idx_container = []
for sacname in glob.glob("../data/HV.OTLD/201*.SAC"):
    tr = read(sacname)[0]
    tr.detrend(type='linear')
    t = np.arange(tr.stats.npts) / tr.stats.sampling_rate
    p_arr, quality = picker(tr)
    print(sacname, p_arr, quality)

    if p_arr > win and p_arr < t[-1]-win and quality > 4.0:

        snr = SNR(tr, p_arr, win)
        freq_idx = fi(tr, p_arr, win)
        freq_idx_container.append(freq_idx)
        
        # plot individual waveform, comment if only calculate fi hist
        #fig, ax = plt.subplots(2, 1)
        #ax[0].plot(t, tr.data)
        #ax[0].axvline(x=p_arr, color='r')
        #ax[0].set_title('quality={:.1f}, snr={:.1f}, fi={:.2f}'.\
        #                format(quality, snr, freq_idx))
        #amp, freq = fft_amp(tr.data, tr.stats.sampling_rate)
        #ax[1].semilogx(freq, amp)
        #plt.show() 

  
bins_ = np.linspace(-2, 1, 30)
plt.hist(freq_idx_container, bins=bins_, edgecolor='k')
plt.show()

