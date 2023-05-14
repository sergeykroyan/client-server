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
nicknames = {}
clients = []


# Sending Messages To All Connected Clients
def broadcast(message, sender):
    for client, client_public_key in credentials.items():
        if client != sender:
            encrypted_message = rsa.encrypt(message, client_public_key)
            client.send(encrypted_message.encode(FORMAT))
            client.send(nicknames[sender].encode(FORMAT))


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            m = client.recv(2048).decode(FORMAT)
            message = rsa.decrypt(m, private_key)
            broadcast(message, client)
        except:
            # Removing And Closing Clients
            clients.remove(client)
            client.close()
            del nicknames[client]
            del credentials[client]
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        clients.append(client)
        print("Connected with {}".format(str(address)))

        client.send(f"{public_key}".encode(FORMAT))
        client.send(f"{private_key}".encode(FORMAT))
        client_public_key = eval(client.recv(2048).decode(FORMAT))

        nickname = client.recv(2048).decode(FORMAT)
        print("Nickname is {}".format(nickname))

        nicknames[client] = nickname
        credentials[client] = client_public_key

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive_thread = threading.Thread(target=receive)
receive_thread.start()
