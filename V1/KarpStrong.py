###########################################
#                                         #
#     Bones of a synth based on the       #
#       Karplus-Strong Algorithm          #
#                                         #
###########################################

import numpy as np
from scipy.io.wavfile import write

# Setting sample rate
Fs = 44100
OUTMONO = None
OUTSTER = None

# Create or access existing saveddata.dat file
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

    while len(out) < num_samples:
        out = np.append(out, wave)

    # 1-channel output
    out = out[0:num_samples]
    global OUTMONO
    OUTMONO = out
    # 2-channel output
    out = np.insert(np.expand_dims(out, axis=1), 1, out, axis=1)
    global OUTSTER
    OUTSTER = out
    return out


def to_wav(arr):
    write("Sound" + str(filenum()) + ".wav", Fs, arr)


# Example
karpstrong(60, 1, "noise", 25)
to_wav(OUTSTER)
