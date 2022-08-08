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

# WAVEFORM = None
# OUTMONO = None
# OUTSTER = None
# t = np.linspace(0., 1., Fs)


# Frequency in hz, length in seconds, model selection between "Noise" or "Ints"
# timbre only used in "noise" model
# fund_mult takes [0,1] accentuates the fundamental frequency (hz)
def ks_waveform(hz, model=None, timbre=1, fund_mult=0):
    excitation_len = int(np.ceil(Fs / hz))

    if model == "noise":
        wave = np.random.normal(0, 1, excitation_len) ** (timbre // 2 * 2 + 1)
        # normalize to float32 bounds
        wave -= (max(wave) + min(wave)) / 2
        wave *= 1 / (max(wave))
        out = wave.astype(np.float32)
    else:
        wave = np.random.randint(0, 2, excitation_len) * 2 - 1
        out = wave.astype(np.float32)

    for i in range(len(out)):
        out[i] = (out[i] * (1 - (i / len(out)))) + (out[i] * ((1 - fund_mult) * (i / len(out))))

    return out


# take waveform and repeat over time in seconds
def ks_length(waveform, seconds):
    out = waveform
    num_samples = int(np.ceil(Fs * seconds))
    while len(out) < num_samples:
        out = np.append(out, waveform)
    # 2-Channel output
    out = np.insert(np.expand_dims(out[0:num_samples], axis=0), 1, out[0:num_samples], axis=0)
    return  out


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


# export as float32 wav file
def to_wav(arr):
    arr = np.asarray(np.rot90(np.fliplr(arr)))
    write("Sound" + str(filenum()) + ".wav", Fs, arr)


# example
OUTSTER = ks_length(ks_waveform(60, "Noise", 1, 0.5), 1)
OUTSTER = gain(OUTSTER, 0.7)
OUTSTER = adsr(OUTSTER, 80, 400, 150, 0.4, 200, 2, 1.3, 4)
OUTSTER = haas_effect(OUTSTER, 32.4, "Left")
to_wav(OUTSTER)
