def affine_encrypt(text, a, b):
    result = ''
    for char in text:
        if char.isalpha():
            char_index = ord(char.lower()) - 97
            encrypted_index = (a * char_index + b) % 26
            result += chr(encrypted_index + 97)
        else:
            result += char
    return result


def affine_decrypt(text, a, b):
    result = ''
    a_inverse = pow(a, -1, 26)
    for char in text:
        if char.isalpha():
            char_index = ord(char.lower()) - 97
            decrypted_index = (a_inverse * (char_index - b)) % 26
            result += chr(decrypted_index + 97)
        else:
            result += char
    return result
