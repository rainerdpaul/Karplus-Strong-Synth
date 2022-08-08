import numpy as np

setup = open("Setup.txt", "r")
Fs = int(setup.readlines()[1])


# sums L, R channels
def mono(arr):
    arr[0] = np.sum(arr, axis=0) * 0.5
    arr[1] = np.sum(arr, axis=0) * 0.5
    return arr


# panning L to R [-1,1]
def pan(arr, pan):
    arr[0] = np.multiply(arr[0], 1 - pan).clip(-1,1)
    arr[1] = np.multiply(arr[1], 1 + pan).clip(-1,1)
    return arr


# shifts whole sample by ms value
def shift(arr, ms):
    amount = int(ms * Fs / 1000)
    if amount == 0:
        return arr
    if amount != 0:
        arr[0] = np.append(np.zeros(amount), arr[0][:-amount])
        arr[1] = np.append(np.zeros(amount), arr[1][:-amount])
        return arr


# applies slight delay to a single channel
def haas_effect(arr, ms, side):
    amount = int(ms * Fs / 1000)
    ind = 0 if side == "Left" else 1
    arr[ind] = np.append(arr[ind][-amount:], arr[ind][:-amount])
    return arr


# applies a gain factor to the signal clipped to float32 bounds
# set min and max later
def gain(arr, factor):
    return np.clip(np.multiply(arr, factor), -1, 1)


# a, d, s, r in ms, s_level in [0,1]
# ac, dc, and rc are exponential curving factors between [0, 10]
def adsr(arr, a, d, s, s_level, r, ac=1, dc=1, rc=1):
    a_len = a * Fs // 1000
    d_len = d * Fs // 1000
    s_len = s * Fs // 1000
    r_len = r * Fs // 1000
    a_max = a_len
    d_max = a_max + d_len
    s_max = d_max + s_len
    r_max = s_max + r_len
    for i in range(len(arr[1])):
        if i < a_max:
            arr[0][i] = arr[0][i] * ((i / a_len) ** ac)
            arr[1][i] = arr[1][i] * ((i / a_len) ** ac)
        if a_max <= i < d_max:
            arr[0][i] = (arr[0][i] * ((s_level * (i - a_max)) / d_len)) + (arr[0][i] * (((d_len - (i - a_max)) / d_len) ** dc))
            arr[1][i] = (arr[1][i] * ((s_level * (i - a_max)) / d_len)) + (arr[1][i] * (((d_len - (i - a_max)) / d_len) ** dc))
        if d_max <= i < s_max:
            arr[0][i] = arr[0][i] * s_level
            arr[1][i] = arr[1][i] * s_level
        if s_max <= i < r_max:
            arr[0][i] = arr[0][i] * (((r_len - (i - s_max)) / r_len) ** rc) * s_level
            arr[1][i] = arr[1][i] * (((r_len - (i - s_max)) / r_len) ** rc) * s_level
        if i >= r_max:
            arr[0][i] = 0
            arr[1][i] = 0
    return arr
