import itertools
import re


def rle2_compress(s):
    encoded = []
    for char, group in itertools.groupby(s):
        count = len(list(group))
        encoded.append(str(count) + " " + str(ord(char)) + " ")
    return ''.join(encoded)


def rle2_decompress(s):
    decoded = []
    for group in re.findall("(\d+\s\d+\s)", s):
        value = group.split(" ")
        count, char = value[0], value[1]
        char = chr(int(char))
        decoded.append(char * int(count))
    return ''.join(decoded)
