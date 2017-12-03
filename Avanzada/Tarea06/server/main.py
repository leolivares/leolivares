import socket
import json
import threading
import zlib
import os
from random import choice, sample

class Server:

    def __init__(self):
        self.host = "localhost"
        self.port = 5555

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        self.send_lock = threading.Lock()

        self.socket_server.listen(10)

        thread = threading.Thread(target=self.accept_clients, daemon=True)
        thread.start()

        self.clients = []


    def accept_clients(self):
        while True:
            socket_client, address = self.socket_server.accept()

            listening_thread = threading.Thread(
                target=self.listen_client, daemon=True, args=(socket_client,))
            listening_thread.start()


    def listen_client(self, socket_client):
        listen = True
        while listen:

            try:
                length_bytes = socket_client.recv(4)
                length = int.from_bytes(length_bytes, byteorder="big")

                message = bytearray()
                i = 256
                while len(message) < length:
                    if len(message) + i > length:
                        i = length - len(message)
                    message += socket_client.recv(i)

                message = message.decode()
                message = json.loads(message)

                self.handle_message(message, socket_client)

            except json.decoder.JSONDecodeError:
                socket_client.close()
                self.remove(socket_client)
                self.update_users()
                listen = False

    def remove(self, socket_client):
        self.clients = [x for x in self.clients if x[1] != socket_client]

    def handle_message(self, message, socket_client):
        if message["status"] == "username":
            self.check_username(message["data"], socket_client)

        elif message["status"] == "images request":
            self.select_images(socket_client)

        elif message["status"] == "change buttons":
            self.change_buttons(message["data"])


    def send(self, message, socket_client):

        with self.send_lock:
            message_json = json.dumps(message)
            message_bytes = message_json.encode()

            length = len(message_bytes).to_bytes(4, byteorder="big")

            socket_client.send(length + message_bytes)


    def check_username(self, username, socket_client):
        valid_username = False
        current_usernames = list(map(lambda x: x[0], self.clients))

        if len(username) < 2:
            message = {"status": "username", "data": [False, "El username debe tener como minimo dos caracteres"]}

        elif username in current_usernames:
            message = {"status": "username", "data": [False, "Usuario actualmente en linea"]}

        elif not username.isalnum():
            message = {"status": "username", "data": [False, "El username no puede tener espacios. Solo letras y numeros"]}

        else:
            self.clients.append((username, socket_client))
            message = {"status": "username", "data": [True, ""]}
            valid_username = True

        self.send(message, socket_client)

        if valid_username:
            self.update_users()

    def select_images(self, socket_client):
        available = os.listdir("image")

        selections = sample(available, 6)
        for img in selections:
            with open("image/{}".format(img), "rb") as file:
                img_bytes = file.read()

            needed_bytes = self.extract_bytes(img_bytes)

            message = {"status": "image", "data": [img, list(needed_bytes)]}

            self.send(message, socket_client)

    def extract_bytes(self, img_bytes):
        i = 0
        while i < len(img_bytes):
            if i == 0:
                firm = img_bytes[:8]
                needed_bytes = firm
                i += 8
            else:
                length_bytes = img_bytes[i:i+4]
                i += 4
                length = int.from_bytes(length_bytes, byteorder="big")
                type_bytes = img_bytes[i:i+4]
                i += 4
                type = type_bytes.decode()

                if type in ["IHDR", "IDAT", "IEND"]:
                    needed_bytes += length_bytes
                    needed_bytes += type_bytes

                    info_bytes = img_bytes[i:i+length]
                    needed_bytes += info_bytes
                    crc_bytes = img_bytes[i+length:i+length+4]
                    needed_bytes += crc_bytes

                i += length + 4

        return needed_bytes

    def update_users(self):
        users_online = list(map(lambda x: x[0], self.clients))
        for user in self.clients:
            message = {"status": "update users", "data": users_online}
            self.send(message, user[1])

    def change_buttons(self, img):
        for user in self.clients:
            message = {"status": "change buttons", "data": img}
            self.send(message, user[1])


if __name__ == '__main__':
    server = Server()

    while True:
        pass
