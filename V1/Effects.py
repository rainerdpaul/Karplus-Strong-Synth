import numpy as np

setup = open("Setup.txt", "r")
Fs = int(setup.readlines()[1])


# applies slight delay to a single channel
def haas_effect(arr, ms, side):
    amount = ms * Fs // 1000
    ind = 0 if side == "Left" else 1
    arr[ind] = np.append(arr[ind][amount:], arr[ind][:amount])
    return arr


# applies a gain factor to the signal clipped to float32 bounds
# set min and max later
def gain(arr, factor):
    return np.clip(np.multiply(arr, factor), -1, 1)


# def adsr(a, d, s, r, ac=0, dc=0, rc=0)