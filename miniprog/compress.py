def compress_text(text):
    new_text = ""
    dictionary = {chr(i): i for i in range(256)}
    result = []
    w = ""
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = len(dictionary)
            w = c
    if w:
        result.append(dictionary[w])

    for num in result:
        new_text += chr(num)
    return new_text

def decompress_text(compressed_text):
    char_codes = [ord(char) for char in compressed_text]
    reverse_dict = {i: chr(i) for i in range(256)}
    result = []
    w = chr(char_codes.pop(0))
    result.append(w)
    for code in char_codes:
        if code in reverse_dict:
            entry = reverse_dict[code]
        elif code == len(reverse_dict):
            entry = w + w[0]
        else:
            raise ValueError(f"Bad compressed code: {code}")
        result.append(entry)
        reverse_dict[len(reverse_dict)] = w + entry[0]
        w = entry
    return ''.join(result)

if __name__ == "__main__":
    text = input("Enter the text to compress: ")
    compressed_text = compress_text(text)
    print("Compressed text:", compressed_text)


    decompressed_text = decompress_text(compressed_text)
    print("Decompressed text:", decompressed_text)