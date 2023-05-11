import socket
import threading

import custom_rsa as rsa

# Connection Data
host = "127.0.0.1"
port = 55555
FORMAT = "utf-8"

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server is running")

p, q = 13, 5
public_key, private_key = rsa.generate_key_pair(p, q)


# Lists For Clients and Their Nicknames

credentials = {}
nicknames = []
clients = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client, client_public_key in credentials:
        encrypted_message = rsa.encrypt(message, client_public_key)
        client.send(encrypted_message.encode(FORMAT))


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast("{} left!".format(nickname).encode(FORMAT))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        clients.append(client)
        print("Connected with {}".format(str(address)))
        client.send(public_key)

        # Request And Store Nickname and Client public key
        client.send("OK".encode(FORMAT))
        client_message = rsa.decrypt(client.recv(1024), private_key)

        nickname, client_public_key = client_message.split(":")
        credentials[nickname] = client_public_key
        nicknames.append(nickname)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))

        broadcast(f"{nickname} joined!")

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive_thread = threading.Thread(target=receive)
receive_thread.start()
