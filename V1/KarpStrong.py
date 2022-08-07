###########################################
#                                         #
#     Bones of a synth based on the       #
#       Karplus-Strong Algorithm          #
#                                         #
###########################################

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write
from Effects import *

setup = open("Setup.txt", "r")
Fs = int(setup.readlines()[1])

WAVEFORM = None
OUTSTER = None

# Create or access existing save.dat file
# Used for updating file number for Sound#.wav
def filenum(filename="saveddata.dat"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 0)
        f.seek(0)
        f.truncate()
        f.write(str(val + 1))
        return val

# Frequency in hz, length in seconds, model selection between "noise" or "ints"
# timbre only used in "noise" model
def karpstrong(hz, seconds, model=None, timbre=1):
    excitation_len = int(np.ceil(Fs / hz))
    num_samples = int(np.ceil(Fs * seconds))

    if model == "noise":
        wave = np.random.normal(0, 1, excitation_len) ** (timbre // 2 * 2 + 1)
        # normalize to float32 bounds
        wave -= (max(wave) + min(wave)) / 2
        wave *= 1 / (max(wave))
        out = wave.astype(np.float32)
    else:
        wave = np.random.randint(0, 2, excitation_len) * 2 - 1
        out = wave.astype(np.float32)

    waveform = out

    while len(out) < num_samples:
        out = np.append(out, wave)

    # 2-Channel output
    out = np.insert(np.expand_dims(out[0:num_samples], axis=0), 1, out[0:num_samples], axis=0)
    return waveform, out


def to_wav(arr):
    arr = np.asarray(np.rot90(np.fliplr(arr)))
    write("Sound" + str(filenum()) + ".wav", Fs, arr)


# Example
WAVEFORM, OUTSTER = karpstrong(60, 1, "noise", 1)
OUTSTER = haas_effect(OUTSTER, 160, "Left")
OUTSTER = gain(OUTSTER, 0.3)
to_wav(OUTSTER)
