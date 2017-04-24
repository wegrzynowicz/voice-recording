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

MAX_LENGTH = 200
FEATURES_DIM = 26


def get_info(filepath):
    filename = os.path.basename(filepath)
    splitted = filename.split('-')
    return splitted[0], splitted[1], splitted[2]


def label_to_int(labels):
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


def get_features(path, features_dim=26):
    """
    1. Frame the signal into short frames.
    2. For each frame calculate the periodogram estimate of the power spectrum.
    3. Apply the mel filterbank to the power spectra, sum the energy in each filter.
    4. Take the logarithm of all filterbank energies  
    :param path: 
    :param features_dim: 
    :return: 
    """
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
    fbank_feat = logfbank(sig, rate, winlen=0.025, winstep=0.01,
                          nfilt=features_dim, nfft=512, lowfreq=0, highfreq=None, preemph=0.97)
    return fbank_feat


if __name__ == "__main__":
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
            label, person, time = get_info(path)
            fbank_feat = get_features(path, FEATURES_DIM)
        except Exception as e:
            logging.error(e)
            print(e)
            print('File: ' + path + ' will be omited')
            continue
        fbank_feat = sequence.pad_sequences(fbank_feat.T, maxlen=MAX_LENGTH, dtype=np.float)
        fbank_feat = preprocessing.scale(fbank_feat, axis=1, with_std=False)
        fbank_feat = fbank_feat / np.max(np.max(np.abs(fbank_feat)))
        X.append(fbank_feat.T)
        labels.append(label)
        people.append(person)

    Y = label_to_int(labels)
    np.savez('features', X=np.array(X), Y=Y, labels=labels, people=people)

    # f, axarr = plt.subplots(2, sharex=True)
    # axarr[0].plot(np.linspace(0,fbank_feat.shape[0],len(sig)),sig)
    # axarr[0].set_title('Recorded audio signal')
    # axarr[1].imshow(fbank_feat.T)
    # axarr[1].set_title("log Mel-filterbank energy features from an audio signal",fontsize=14)
    # axarr[1].set_ylabel("Features")
    # axarr[1].set_xlabel("Recording time")
