import socket
import rsa
import threading

from affine_cipher import affine_decrypt, affine_encrypt
from rle import rle2_compress, rle2_decompress

host = "127.0.0.1"
port = 55555

# Generate RSA keypair
public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = int(input("Do you want to host (1) or to connect (2): "))

if choice == 1:
    print("Server is running")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == 2:
    print("Connecting to server")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def sending_messages(cl):
    while True:
        message = input("> ")
        # Encrypt message using RSA public key
        affine_message_encrypt = affine_encrypt(message, 5, 8)
        rle_message_encrypt = rle2_compress(affine_message_encrypt)
        cl.send(rsa.encrypt(rle_message_encrypt.encode(), public_partner))
        print(f"You: {message}")


def receiving_messages(cl):
    while True:
        message = rsa.decrypt(cl.recv(1024), private_key).decode()
        rle_message_decrypt = rle2_decompress(message)
        affine_message_decrypt = affine_decrypt(rle_message_decrypt, 5, 8)
        print(f"User: {affine_message_decrypt}")


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
