import os
import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from scipy.signal.spectral import spectrogram
import sys
import importlib

importlib.reload(matplotlib)
matplotlib.use('Agg') #Use this as the backend while saving, Matplotlib has some weird memory leak issues without it

AUDIO_PATH = f''

X_ST = 1.5
Y_ST = 0.9
DPI_ST = 400

X_VGG = 1
Y_VGG = 0.9
DPI_VGG = 292
SAMPLING_RATE = 22050
HOP_LENGTH = 512
N_FFT = 2048

#All these parameters result in a final spectrogram size of 512x512 on my machine, change as per your needs!

audio_clips = os.listdir(AUDIO_PATH)

item = 1
for file in os.listdir(AUDIO_PATH):
    print(f"Generating and Saving Spectrogram ({sys.argv[1]}) - ## FILE @ {item} --> [{file}] ##")
    signal, sr = librosa.load(AUDIO_PATH+file, sr=SAMPLING_RATE)
    mel_spectrogram = librosa.feature.melspectrogram(y=signal, sr=sr)
    mel_spectrogram_db = librosa.amplitude_to_db(mel_spectrogram, ref=np.max)
    librosa.display.specshow(mel_spectrogram_db, y_axis='mel', hop_length=HOP_LENGTH, x_axis='time')
    figure = plt.gcf()
    plt.axis('off')
    figure.set_size_inches(X_ST,Y_ST)
    plt.savefig(f'{AUDIO_PATH}/spectrograms/{sys.argv[1]}_{item}.png',bbox_inches='tight', pad_inches=0, dpi=DPI_ST)
    item += 1
    del figure
    plt.clf()
    plt.close('all')







