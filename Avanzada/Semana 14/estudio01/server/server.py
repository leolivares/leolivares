# Servidor...
import os
import json
import socket
import threading


class Server:

    def __init__(self):
        self.host = "localhost"
        self.port = 5556
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(5)

        self.cliente = None

        thread = threading.Thread(target=self.accept_clients, daemon=True)
        thread.start()

    def accept_clients(self):
        while True:
            socket_cliente, address = self.socket_server.accept()

            print("Cliente Conectado {} {}".format(socket_cliente, address))
            self.cliente = socket_cliente

            thread = threading.Thread(target=self.listen_client, daemon=True, args=(self.cliente,))
            thread.start()


    def listen_client(self, client):
        while True:
            msg = client.recv(2048)
            msg = msg.decode("UTF-8")

            msg = json.loads(msg)

            if msg["status"] == "ingreso":
                if len(msg["data"]) != 0:
                    response = {"status": "ingreso", "data": True}
                else:
                    response = {"status": "ingreso", "data": False}

            self.handle(response, client)

    def handle(self, response, client):
        response = json.dumps(response)
        response = response.encode()

        client.send(response)



if __name__ == '__main__':
    server = Server()

    while True:
        pass
