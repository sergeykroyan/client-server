import socket
import threading

from custom_rsa import RSAEncryptor


class Server:
    p, q = 13, 5

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        print("Server is running")

        self.rsa = RSAEncryptor(self.p, self.q)
        self.public_key, self.private_key = self.rsa.generate_key_pair()

        self.credentials = {}
        self.nicknames = {}
        self.clients = []

    def broadcast(self, message, sender):
        for client, client_public_key in self.credentials.items():
            if client != sender:
                encrypted_message = self.rsa.encrypt(message, client_public_key)
                client.send(encrypted_message.encode(FORMAT))
                client.send(self.nicknames[sender].encode(FORMAT))

    def handle(self, client):
        while True:
            try:
                m = client.recv(2048).decode(FORMAT)
                message = self.rsa.decrypt(m, self.private_key)
                self.broadcast(message, client)
            except:
                self.clients.remove(client)
                client.close()
                del self.nicknames[client]
                del self.credentials[client]
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            print(f"Connected with: {str(address)}")

            client.send(f"{self.public_key}".encode(FORMAT))
            client_public_key = eval(client.recv(2048).decode(FORMAT))

            nickname = client.recv(2048).decode(FORMAT)
            print(f"Nickname is: {nickname}")

            print(f"Connected clients: {len(self.clients)}")
            self.nicknames[client] = nickname
            self.credentials[client] = client_public_key

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()


if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 55555
    FORMAT = "utf-8"

    chat_server = Server(server_host, server_port)
    chat_server.start()
