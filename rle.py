def rle2_compress(text):
    compressed = ''
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            count += 1
        else:
            compressed += str(count) + text[i-1]
            count = 1
    compressed += str(count) + text[-1]
    return compressed


def rle2_decompress(text):
    decompressed = ''
    i = 0
    while i < len(text):
        count = int(text[i])
        char = text[i+1]
        decompressed += char * count
        i += 2
    return decompressed
