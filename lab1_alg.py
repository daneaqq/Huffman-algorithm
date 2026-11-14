import sys
import os

class node:
    def __init__(self, freq, sym=None, left=None, right=None):
        self.freq = freq
        self.sym = sym
        self.left = left
        self.right = right

# частота символов в файле
def get_freqs(fname):
    f = open(fname, 'rb')
    freqs = {}

    byte = f.read(1)
    while byte:
        if byte not in freqs:
            freqs[byte] = 0
        freqs[byte] += 1
        byte = f.read(1)

    f.close()
    return freqs