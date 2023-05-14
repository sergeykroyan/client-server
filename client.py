import socket
import threading

import custom_rsa as rsa
from affine_cipher import affine_encrypt, affine_decrypt
from rle import rle2_compress, rle2_decompress

FORMAT = "utf-8"

p, q = 19, 11
public_key, private_key = rsa.generate_key_pair(p, q)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

SERVER_PUBLIC_KEY = eval(client.recv(2048).decode(FORMAT))
client.send(f"{public_key}".encode(FORMAT))

nickname = input("Choose your nickname: ")
client.send(nickname.encode(FORMAT))


def receive():
    while True:
        message = client.recv(2048).decode(FORMAT)
        if message:
            decrypted_message = rsa.decrypt(message, private_key)
            rle_message_decrypt = rle2_decompress(decrypted_message)
            affine_message_decrypt = affine_decrypt(rle_message_decrypt, 5, 8)
            print(f"{client.recv(2048).decode(FORMAT)}: {affine_message_decrypt}")


def write():
    while True:
        message = input("> ")
        if not message:
            break
        affine_message_encrypt = affine_encrypt(message, 5, 8)
        rle_message_encrypt = rle2_compress(affine_message_encrypt)
        encrypted_message = rsa.encrypt(rle_message_encrypt, SERVER_PUBLIC_KEY)
        client.send(encrypted_message.encode(FORMAT))
        print(f"You: {message}")


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
