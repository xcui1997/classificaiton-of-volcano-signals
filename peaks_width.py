import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
     

def find_peaks(x):
    max_index =np.argmax(x)
    return max_index


def peak_width(fremax, fremin, maxindex):
    freq = np.linspace(0, 15, 60, endpoint=False)
    width = freq[fremax] - freq[fremin]
    amp_max = freq[maxindex]
    return width, amp_max, freq[fremax], freq[fremin]


def find_width(x):
    x_cum = np.cumsum(x) # 1 2 3->1 3 6
    fre_max = np.where(x_cum >= 0.9*x_cum[-1])[0][0]
    fre_min = np.where(x_cum >= 0.1*x_cum[-1])[0][0]
    return fre_max,fre_min

if __name__ == "__main__":
    freq = np.linspace(0, 15, 60, endpoint=False)
    Mean_amp = pickle.load(open('../output/pkl/Mean_amp_container.pkl','rb'))
    num_mean,len_mean = Mean_amp.shape
    # sort with peak frequency
    max_amp = np.max(Mean_amp, axis=-1)
    max_amp_idx = np.argmax(Mean_amp, axis=-1)
    peak_freq = freq[max_amp_idx]
    width = []
    entrp = []

    for i in range(num_mean):
        fre_max,fre_min = find_width(Mean_amp[i,:])
        max_index = find_peaks(Mean_amp[i,:])
        w, amp_max, fmin, fmax = peak_width(fre_max, fre_min, max_index)
        width.append(w)
        entrp.append(entropy(Mean_amp[i,:]))

    fig2, ax2 = plt.subplots(2, 2, figsize=(6, 6))
    ax2[0, 0].scatter(peak_freq, 1./max_amp)
    ax2[0, 1].scatter(peak_freq, width)
    ax2[1, 0].scatter(peak_freq, entrp)
    for i in range(num_mean):
        ax2[0, 0].text(peak_freq[i], 1./max_amp[i], str(i))
        ax2[0, 1].text(peak_freq[i], width[i], str(i))
        ax2[1, 0].text(peak_freq[i], entrp[i], str(i))
    ax2[1, 0].set_xlabel('Peak frequency (Hz)')
    ax2[0, 0].set_ylabel('1/Peak amplitude')
    ax2[0, 1].set_ylabel('Widtd')
    ax2[1, 0].set_ylabel('Entropy')
    plt.savefig('../output/group.png')
    plt.show()

     
#pickle.dump(sort_idx, open('../output/pkl/sort_idx.pkl', 'wb'))
