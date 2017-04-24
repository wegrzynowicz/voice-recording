from keras.models import model_from_config
from keras.preprocessing import sequence
from sklearn import preprocessing
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from subprocess import call
import numpy as np
import json
import os.path
import sys


def load_model(model_name="model"):
    content = open('models/' + model_name + ".json", 'r').read()
    config = json.loads(content)
    model = model_from_config(config)
    model.load_weights('models/' + model_name + ".h5")
    return model


def convert_2_wav(path):
    directory, filename = os.path.split(path)
    filename, extension = os.path.splitext(filename)
    new_path = directory + '/' + filename + '.wav'
    call(('ffmpeg.exe', '-i', path, new_path), shell=True)
    # os.remove(path)
    return new_path


def get_features(path, features_dim=26):
    """
    1. Frame the signal into short frames.
    2. For each frame calculate the periodogram estimate of the power spectrum.
    3. Apply the mel filterbank to the power spectra, sum the energy in each filter.
    4. Take the logarithm of all filterbank energies  
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


def check_label(prediction, labels_file='labels'):
    f = np.load("models/" + labels_file + '.npz')
    labels = f['labels']
    return labels[prediction]


def recognize(path, features_dim=26, max_length=200):
    try:
        model = load_model()
        fbank_feat = get_features(path, features_dim)
        fbank_feat = sequence.pad_sequences(fbank_feat.T, maxlen=max_length, dtype=np.float)
        fbank_feat = preprocessing.scale(fbank_feat, axis=1, with_std=False)
        fbank_feat = fbank_feat / np.max(np.max(np.abs(fbank_feat)))
        fbank_feat = fbank_feat.reshape(1, max_length, features_dim)
        pred = np.argmax(model.predict(fbank_feat, 1))
    except:
        return 'Error'
    return check_label(pred)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        label = recognize(sys.argv[1])
    else:
        raise IOError('No audio file path specified')
    print(label)
