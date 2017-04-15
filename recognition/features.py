from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
from keras.preprocessing import sequence
from sklearn import preprocessing
import scipy.io.wavfile as wav
import glob
import os.path
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import logging

plt.interactive(True)
plt.close('all')


def _get_info(filepath):
    filename = os.path.basename(filepath)
    splitted = filename.split('-')
    return splitted[0], splitted[1], splitted[2]


def _label_to_one_hot(labels, unique_labels):
    lookup = np.eye(len(unique_labels))
    Y = np.empty([len(labels), len(unique_labels)])
    for lab_it in range(len(labels)):
        idx = unique_labels.index(labels[lab_it])
        Y[lab_it, :] = lookup[idx, :]
    return Y


def _label_to_int(labels):
    unique_labels = list(set(labels))
    ints = np.empty(len(labels), dtype=np.int)
    for lab_it in range(len(labels)):
        ints[lab_it] = unique_labels.index(labels[lab_it])
    return ints


def convert_2_wav(path):
    directory, filename = os.path.split(path)
    filename, extension = os.path.splitext(filename)

    new_path = directory + '/' + filename + '.wav'
    out = subprocess.check_output(('ffmpeg.exe', '-i', path, new_path), shell=True)
    os.remove(path)
    return new_path


def features_from_file(path):
    label, person, time = _get_info(path)

    # Convert audio file (opus codec) to WAV file
    if path.find('wav') == -1:
        path = convert_2_wav(path)
    # Read WAV file
    (rate, sig) = wav.read(path)
    sig = sig.astype(np.float)
    rate = float(rate)
    # If audio is stereo, select first channel
    if len(sig.shape) > 1:
        sig = sig[:, 0]
    if np.std(sig) == 0.0:
        raise Exception('Signal is empty')
    # Frame the signal into short frames.
    # For each frame calculate the periodogram estimate of the power spectrum.
    # Apply the mel filterbank to the power spectra, sum the energy in each filter.
    # Take the logarithm of all filterbank energies.
    # Take the DCT of the log filterbank energies.
    # Keep DCT coefficients 2-13, discard the rest.

    mfcc_feat = mfcc(sig, samplerate=rate, winlen=0.025, winstep=0.01, numcep=25,
                     nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97,
                     ceplifter=22, appendEnergy=True)
    # Compute simple deltas of MFCC features
    d_mfcc_feat = delta(mfcc_feat, 2)
    fbank_feat = logfbank(sig, rate, winlen=0.025, winstep=0.01,
                          nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97)
    return label, person, sig, mfcc_feat, fbank_feat


max_length = 200
features_dim = 25
recordings_list = glob.glob('../uploads/*')
n_files = len(recordings_list)
labels = list()
people = list()
X = list()

for file_it in range(n_files):
    path = recordings_list[file_it]
    if path.find('.wav') == -1:
        path = convert_2_wav(path)
    try:
        label, person, sig, mfcc_feat, fbank_feat = features_from_file(path)

    except Exception as e:
        logging.error(e)
        print(e)
        print('File: ' + path + ' will be omited')
        continue

    mfcc_feat = sequence.pad_sequences(mfcc_feat.T, maxlen=max_length, dtype=np.float)
    fbank_feat = sequence.pad_sequences(fbank_feat.T, maxlen=max_length, dtype=np.float)

    mfcc_feat = preprocessing.scale(mfcc_feat, axis=1, with_std=False)
    fbank_feat = preprocessing.scale(fbank_feat, axis=1, with_std=False)

    mfcc_feat = mfcc_feat / np.max(np.max(np.abs(mfcc_feat)))
    fbank_feat = fbank_feat / np.max(np.max(np.abs(fbank_feat)))

    X.append(fbank_feat.T)
    labels.append(label)
    people.append(person)

Y = _label_to_int(labels)
np.savez('features', X=np.array(X), Y=Y, labels=labels, people=people)

plt.matshow(mfcc_feat)
plt.matshow(fbank_feat)
