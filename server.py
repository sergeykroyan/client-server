import socket
import threading

import custom_rsa as rsa

host = "127.0.0.1"
port = 55555
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server is running")

p, q = 13, 5
public_key, private_key = rsa.generate_key_pair(p, q)


credentials = {}
nicknames = {}
clients = []


def broadcast(message, sender):
    for client, client_public_key in credentials.items():
        if client != sender:
            encrypted_message = rsa.encrypt(message, client_public_key)
            client.send(encrypted_message.encode(FORMAT))
            client.send(nicknames[sender].encode(FORMAT))


def handle(client):
    while True:
        try:
            m = client.recv(2048).decode(FORMAT)
            message = rsa.decrypt(m, private_key)
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            del nicknames[client]
            del credentials[client]
            break


def receive():
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f"Connected with: {str(address)}")

        client.send(f"{public_key}".encode(FORMAT))
        client_public_key = eval(client.recv(2048).decode(FORMAT))

        nickname = client.recv(2048).decode(FORMAT)
        print(f"Nickname is: {nickname}")

        print(f"Connected clients: {len(clients)}")
        nicknames[client] = nickname
        credentials[client] = client_public_key

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive_thread = threading.Thread(target=receive)
receive_thread.start()
