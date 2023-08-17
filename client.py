import socket
import threading

from custom_rsa import RSAEncryptor
from affine_cipher import AffineCipher
from rle import RLECompressor


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.p, self.q = 19, 11
        self.rsa = RSAEncryptor(self.p, self.q)
        self.public_key, self.private_key = self.rsa.generate_key_pair()

        self.SERVER_PUBLIC_KEY = None

        self.rle = RLECompressor()
        self.affine_cipher = AffineCipher()

    def start(self):
        self.SERVER_PUBLIC_KEY = eval(self.client.recv(2048).decode(FORMAT))
        self.client.send(f"{self.public_key}".encode(FORMAT))

        nickname = input("Choose your nickname: ")
        self.client.send(nickname.encode(FORMAT))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def receive(self):
        while True:
            message = self.client.recv(2048).decode(FORMAT)
            if message:
                decrypted_message = self.rsa.decrypt(message, self.private_key)
                rle_message_decrypt = self.rle.decompress(decrypted_message)
                affine_message_decrypt = self.affine_cipher.decrypt(rle_message_decrypt, 5, 8)
                print(f"{self.client.recv(2048).decode(FORMAT)}: {affine_message_decrypt}")

    def write(self):
        while True:
            message = input("> ")
            if not message:
                break
            affine_message_encrypt = self.affine_cipher.encrypt(message, 5, 8)
            rle_message_encrypt = self.rle.compress(affine_message_encrypt)
            encrypted_message = self.rsa.encrypt(rle_message_encrypt, self.SERVER_PUBLIC_KEY)
            self.client.send(encrypted_message.encode(FORMAT))
            print(f"You: {message}")


if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 55555
    FORMAT = "utf-8"

    chat_client = Client(server_host, server_port)
    chat_client.start()
