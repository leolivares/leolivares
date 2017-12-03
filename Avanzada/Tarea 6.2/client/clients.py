import socket
import json
import threading
import zlib
from PyQt5.QtCore import QObject, pyqtSignal


HOST = "localhost"
PORT = 5556


class Client(QObject):

    trigger_popup = pyqtSignal(str)
    trigger_access_dashboard = pyqtSignal()
    trigger_update_usernames = pyqtSignal(list)
    trigger_show_image = pyqtSignal(list)
    trigger_change_buttons = pyqtSignal(str)
    trigger_set_image_edit = pyqtSignal(list)
    trigger_add_comment = pyqtSignal(list)
    trigger_load_comments = pyqtSignal(list)
    trigger_update_img_edit = pyqtSignal(list)
    trigger_update_img_dashboard = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__()
        self.host = HOST
        self.port = PORT
        self.connected = False
        self.parent = parent
        self.username = ""
        self.currently_in = None
        self.send_lock = threading.Lock()

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

            while len(message) < length:
                message += self.socket_client.recv(length-len(message))

            decoded = message.decode()
            final = json.loads(decoded)

            self.handle_message(final)

    def handle_message(self, message):
        if message["status"] == "username":
            if message["data"][0] is False:
                self.trigger_popup.emit(message["data"][1])
            elif message["data"][0] is True:
                self.trigger_access_dashboard.emit()

        elif message["status"] == "update usernames":
            self.trigger_update_usernames.emit(message["data"])

        elif message["status"] == "image":
            self.trigger_show_image.emit(message["data"])

        elif message["status"] == "change buttons":
            self.trigger_change_buttons.emit(message["data"])

        elif message["status"] == "image edit":
            self.trigger_set_image_edit.emit(message["data"])

        elif message["status"] == "add comment":
            img = message["data"][0]
            if self.currently_in == img:
                self.trigger_add_comment.emit(message["data"][1:])

        elif message["status"] == "load comments":
            self.trigger_load_comments.emit(message["data"])

        elif message["status"] == "update image":
            self.trigger_update_img_edit.emit(message["data"])
            self.trigger_update_img_dashboard.emit(message["data"])

        elif message["status"] == "download":
            self.download_image(message["data"])

    def send(self, message):
        message_json = json.dumps(message)
        message_bytes = message_json.encode()
        length = len(message_bytes).to_bytes(4, byteorder="big")

        self.socket_client.send(length + message_bytes)

    def check_username(self, username):
        self.username = username
        message = {"status": "username", "data": username}
        self.send(message)

    def update_users(self):
        message = {"status": "update usernames"}
        self.send(message)

    def request_images(self):
        message = {"status": "images request"}
        self.send(message)

    def change_buttons(self, img):
        message = {"status": "change buttons", "data": img}
        self.send(message)

    def request_image(self, img):
        message = {"status": "request img", "data": img}
        self.send(message)

    def publish_comment(self, comment, img):
        message = {"status": "comment", "data": [img, comment, self.username]}
        self.send(message)

    def request_comments(self, img):
        message = {"status": "request comments", "data": img}
        self.send(message)

    def blurr_image(self, img):
        message = {"status": "blurry", "data": img}
        self.send(message)

    def dicc_bytes(self, img_bytes):
        cla = {}

        firm = img_bytes[:8]
        cla["firm"] = firm

        i = 8
        while i < len(img_bytes):
            length_bytes = img_bytes[i:i + 4]
            length = int.from_bytes(length_bytes, byteorder="big")

            i += 4
            type_bytes = img_bytes[i:i + 4]
            type = type_bytes.decode()
            i += 4
            data = img_bytes[i:i + length]
            i += length
            crc = img_bytes[i:i + 4]
            i += 4

            if type == "IHDR" or type == "IEND":
                cla[type] = length_bytes + type_bytes + data + crc

        return cla

    def create_png(self, dicc, idat_bytes):
        png_bytes = dicc["firm"] + dicc["IHDR"] + bytes(idat_bytes) + dicc["IEND"]
        return png_bytes

    def cut_image(self, pos, img):
        message = {"status": "cut", "data": [pos, img]}
        self.send(message)

    def bucket(self, position, color, img):
        message = {"status": "bucket", "data": [position, color, img]}
        self.send(message)

    def download(self, img):
        message = {"status": "download", "data": img}
        self.send(message)

    def download_image(self, info):
        with open("Downloads/{}".format(info[0]), "wb") as file:
            bts = bytes(info[1])
            file.write(bts)

    def upload_image(self, path):

        with open(path, "rb") as file:
            img_bytes = file.read()

        path_d = path.split("/")
        img_name = path_d[-1]

        message = {"status": "upload", "data": [img_name, list(img_bytes)]}
        self.send(message)
