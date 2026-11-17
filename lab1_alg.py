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



# рекурсивно коды хаффмана
def make_codes(node, cur_code, codes):
    if node.sym is not None:
        if cur_code == "":
            codes[node.sym] = "0"
        else:
            codes[node.sym] = cur_code
        return

    make_codes(node.left, cur_code + "0", codes)
    make_codes(node.right, cur_code + "1", codes)


# сохраняет дерево
def save_tree(node, f):
    if node.sym is not None:
        f.write(b'L')
        f.write(node.sym)
    else:
        f.write(b'I')
        save_tree(node.left, f)
        save_tree(node.right, f)


# грузит дерево
def load_tree(f):
    type_byte = f.read(1)
    if not type_byte:
        return None

    if type_byte == b'L':
        sym = f.read(1)
        return node(0, sym)
    else:
        left = load_tree(f)
        right = load_tree(f)
        return node(0, None, left, right)


# кодирует файл
def encode_file(in_name, out_name):
    print("encoding", in_name)

    freqs = get_freqs(in_name)
    if not freqs:
        f = open(out_name, 'wb')
        f.close()
        print("empty file")
        return

    root = build_tree(freqs)

    codes = {}
    make_codes(root, "", codes)

    bit_str = ""
    with open(in_name, 'rb') as inf:
        data = inf.read()

    for b in data:
        bit_str += codes[bytes([b])]

    pad_len = 0
    if len(bit_str) % 8 != 0:
        pad_len = 8 - (len(bit_str) % 8)
        bit_str += "0" * pad_len

    with open(out_name, 'wb') as outf:
        save_tree(root, outf)
        outf.write(b'|')
        outf.write(bytes([pad_len]))

        for i in range(0, len(bit_str), 8):
            byte_str = bit_str[i:i + 8]
            byte_val = int(byte_str, 2)
            outf.write(bytes([byte_val]))

    in_size = os.path.getsize(in_name)
    out_size = os.path.getsize(out_name)
    print(f"size {in_size} -> {out_size} bytes")
    if in_size > 0:
        ratio = ((in_size - out_size) / in_size) * 100
        print(f"ratio {ratio:.1f}%")

    print("done")



# декодирует файлик
def decode_file(in_name, out_name):
    print("decoding", in_name)

    with open(in_name, 'rb') as inf:
        root = load_tree(inf)
        if root is None:
            open(out_name, 'wb').close()
            print("empty file")
            return

        while True:
            byte = inf.read(1)
            if not byte or byte == b'|':
                break

        pad_len = inf.read(1)
        if not pad_len:
            open(out_name, 'wb').close()
            return
        pad_len = pad_len[0]

        encoded_bytes = inf.read()
        if not encoded_bytes:
            open(out_name, 'wb').close()
            return

    bit_str = ""
    for byte in encoded_bytes:
        bit_str += f"{byte:08b}"

    if pad_len > 0:
        bit_str = bit_str[:-pad_len]

    result_bytes = []
    cur_node = root

    for bit in bit_str:
        if bit == '0':
            cur_node = cur_node.left
        else:
            cur_node = cur_node.right

        if cur_node.sym is not None:
            result_bytes.append(cur_node.sym)
            cur_node = root

    with open(out_name, 'wb') as outf:
        for byte in result_bytes:
            outf.write(byte)

    print("done")



def main():
    if len(sys.argv) < 4:
        print("python huffman.py encode input.txt file.huf")
        print("python huffman.py decode file.huf input.txt")
        return 1

    mode = sys.argv[1]
    in_file = sys.argv[2]
    out_file = sys.argv[3]

    if not os.path.exists(in_file):
        print("error")
        return 1

    if mode == "encode":
        encode_file(in_file, out_file)
    elif mode == "decode":
        decode_file(in_file, out_file)
    else:
        print("error")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
