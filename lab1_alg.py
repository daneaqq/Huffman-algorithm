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

# дерево хаффмана
def build_tree(freq_dict):
    nodes = []

    for sym, freq in freq_dict.items():
        nodes.append(node(freq, sym))

    if not nodes:
        return None

    n = len(nodes)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nodes[j].freq > nodes[j + 1].freq:
                nodes[j], nodes[j + 1] = nodes[j + 1], nodes[j]

    while len(nodes) > 1:
        left = nodes.pop(0)
        right = nodes.pop(0)

        new_node = node(left.freq + right.freq, None, left, right)

        pos = 0
        for i in range(len(nodes)):
            if new_node.freq < nodes[i].freq:
                pos = i
                break
            else:
                pos = i + 1

        nodes.insert(pos, new_node)

    return nodes[0]