from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import glob
import os.path
import matplotlib.pyplot as plt
import numpy as np

plt.interactive(True)
plt.close('all')

def _get_info(filepath):
    filename = os.path.basename(filepath)
    label = filename.split('-')[0]
    return label

max_length = 200

recordings_list = glob.glob('./uploads/*.wav')
n_files = len(recordings_list)
labels = list()
X = np.empty([n_files,max_length,26])

for i in range(len(recordings_list)):
    labels.append(_get_info(recordings_list[i]))

    (rate, sig) = wav.read(recordings_list[i])
    sig = sig[:,0]
    mfcc_feat = mfcc(sig, samplerate=rate, winlen=0.025, winstep=0.01, numcep=13,
                     nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97,
                     ceplifter=22, appendEnergy=True)
    d_mfcc_feat = delta(mfcc_feat, 2)
    fbank_feat = logfbank(sig, rate,winlen=0.025,winstep=0.01,
          nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97)
    print(fbank_feat.shape)

    fbank_feat = np.pad(fbank_feat,((0,max_length-fbank_feat.shape[0]),(0,0)), mode='constant', constant_values=0)
    X[i, :, :] =fbank_feat

unique_labels = list(set(labels))
n_labels = len(unique_labels)
lookup = np.eye(n_labels)
Y =np.empty([n_files,n_labels])
for k in range(n_labels):
    idx = unique_labels.index(labels[i])
    Y[i,:] = lookup[idx,:]


    # print(fbank_feat[1:3, :])
    # plt.figure()
    # plt.matshow(mfcc_feat[:,1:13])
    # plt.figure()
    # plt.plot(mfcc_feat[:,1:13])

# MFCC computation:
# 1. Frame the signal into short frames.
# 2. For each frame calculate the periodogram estimate of the power spectrum.
# 3. Apply the mel filterbank to the power spectra, sum the energy in each filter.
# 4. Take the logarithm of all filterbank energies.
# 5. Take the DCT of the log filterbank energies.
# 6. Keep DCT coefficients 2-13, discard the rest.
