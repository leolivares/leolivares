import socket
import json
import threading
import zlib
from PyQt5.QtCore import QObject, pyqtSignal


class Client(QObject):

    trigger_popup = pyqtSignal(str)
    trigger_access_dashboard = pyqtSignal()
    trigger_show_image = pyqtSignal(list)
    trigger_online_users = pyqtSignal(list)
    trigger_change_buttons = pyqtSignal(bytes)

    def __init__(self, parent):
        super().__init__()
        self.host = "localhost"
        self.port = 5554
        self.connected = False
        self.parent = parent
        self.username = ""

        self.trigger_popup.connect(self.parent.show_popup)
        self.trigger_access_dashboard.connect(self.parent.access_dashboard)

        try:
            self.socket_client = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM)
            self.socket_client.connect((self.host, self.port))

            thread = threading.Thread(target=self.listen_server, daemon=True)
            thread.start()

        except ConnectionRefusedError:
            print("Conexion invalida")
            self.socket_client.close()

    def listen_server(self):
        while True:

            length_bytes = self.socket_client.recv(4)
            length = int.from_bytes(length_bytes, byteorder="big")

            message = bytearray()
            i = 256
            while len(message) < length:
                if len(message) + 256 >= length:
                    i = length - len(message)
                message += self.socket_client.recv(i)

            message = message.decode()
            message = json.loads(message)

            self.handle_message(message)


    def handle_message(self, message):

        if message["status"] == "username":
            if message["data"][0] is False:
                self.trigger_popup.emit(message["data"][1])
            elif message["data"][0] is True:
                self.trigger_access_dashboard.emit()

        elif message["status"] == "image":
            self.trigger_show_image.emit(message["data"])

        elif message["status"] == "update users":
            self.trigger_online_users.emit(message["data"])

        elif message["status"] == "change buttons":
            self.trigger_change_buttons.emit(bytes(message["data"]))

    def send(self, message):
        message_json = json.dumps(message)
        message_bytes = message_json.encode()
        length = len(message_bytes).to_bytes(4, byteorder="big")

        self.socket_client.send(length + message_bytes)

    def check_username(self, username):
        self.username = username
        message = {"status": "username", "data": username}
        self.send(message)

    def request_images(self):
        message = {"status": "images request"}
        self.send(message)

    def change_buttons(self, img):
        message = {"status": "change buttons", "data": list(img)}
        self.send(message)


