import socket
import threading

import custom_rsa as rsa

FORMAT = "utf-8"

p, q = 19, 11
public_key, private_key = rsa.generate_key_pair(p, q)
SERVER_PUBLIC_KEY = None

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

server_public_key = client.recv(1024)
if isinstance(server_public_key, tuple):
    SERVER_PUBLIC_KEY = server_public_key


def receive():
    global SERVER_PUBLIC_KEY

    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "OK" and SERVER_PUBLIC_KEY:
                client.send(nickname.encode(FORMAT))
                message_ = f"{nickname}:{rsa.encrypt(public_key, SERVER_PUBLIC_KEY)}"
                client.send(message_.encode(FORMAT))
            else:
                print(rsa.decrypt(message, private_key))
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        message = "{}: {}".format(nickname, input("> "))
        enc_message = rsa.encrypt(message, SERVER_PUBLIC_KEY)
        client.send(enc_message)


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
