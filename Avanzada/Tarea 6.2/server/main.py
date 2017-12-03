import socket
import json
import threading
import zlib
import os
import datetime
import numpy
from random import choice, sample


HOST = "localhost"
PORT = 5556


class Server:

    def __init__(self):
        self.host = HOST
        self.port = PORT

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
                while len(message) < length:
                    message += socket_client.recv(length-len(message))

                decoded = message.decode()
                final = json.loads(decoded)

                self.handle_message(final, socket_client)

            except json.decoder.JSONDecodeError:
                socket_client.close()
                self.remove(socket_client)
                self.update_usernames()
                listen = False

    def remove(self, socket_client):
        self.clients = [x for x in self.clients if x[1] != socket_client]


    def handle_message(self, message, socket_client):
        if message["status"] == "username":
            self.check_username(message["data"], socket_client)

        elif message["status"] == "update usernames":
            self.update_usernames()

        elif message["status"] == "images request":
            self.select_images(socket_client)

        elif message["status"] == "change buttons":
            self.change_buttons(message["data"])

        elif message["status"] == "request img":
            msg = self.request_image(message["data"])
            msg["status"] = "image edit"
            self.send(msg, socket_client)

        elif message["status"] == "comment":
            self.save_message(message["data"])

        elif message["status"] == "request comments":
            self.retreive_comments(message["data"], socket_client)

        elif message["status"] == "blurry":
            self.blurr_image(message["data"])

        elif message["status"] == "cut":
            self.cut_image(message["data"])

        elif message["status"] == "bucket":
            self.bucket_image(message["data"])

        elif message["status"] == "download":
            msg= self.request_image(message["data"])
            msg["status"] = "download"
            self.send(msg, socket_client)

        elif message["status"] == "upload":
            self.save_new_image(message["data"])

    def send(self, message, socket_client):

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

    def update_usernames(self):
        online_clients = list(map(lambda x: x[0], self.clients))
        for cliente in self.clients:
            message = {"status": "update usernames", "data": online_clients}
            self.send(message, cliente[1])

    def select_images(self, socket_client):
        available = os.listdir("Imagenes")
        available = list(filter(lambda x: x[len(x)-4:len(x)] == ".png", available))

        selections = sample(available, 6)
        for img in selections:
            message = self.request_image(img)
            self.send(message, socket_client)

    def request_image(self, img):
        with open("Imagenes/{}".format(img), "rb") as file:
            img_bytes = file.read()
        needed_bytes = self.extract_bytes(img_bytes)
        message = {"status": "image", "data": [img, list(needed_bytes)]}
        return message

    def request_img_update(self, img):
        with open("Imagenes/{}".format(img), "rb") as file:
            img_bytes = file.read()
        needed_bytes = self.extract_bytes(img_bytes)
        clas = self.classify_bytes(needed_bytes)

        message = {"status": "update image", "data": [img, list(clas["IDAT"])]}
        return message

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

    def change_buttons(self, img):
        for user in self.clients:
            message = {"status": "change buttons", "data": img}
            self.send(message, user[1])

    def save_message(self, data):
        img = data[0]
        comment = data[1]
        user = data[2]
        now = datetime.datetime.now()

        with open("comments.txt", "a") as file:
            print(img, user, comment, str(now), sep=",", file=file)

        for client in self.clients:
            message = {"status": "add comment", "data": [img, comment, user, str(now)]}
            self.send(message, client[1])

    def retreive_comments(self, img, socket_client):

        if os.path.exists("comments.txt"):

            with open("comments.txt", "r") as file:
                comments = list(filter(lambda x: x[0] == img,
                                       map(lambda x: x.strip().split(","),
                                           file.readlines())))

            if len(comments) != 0:
                message = {"status": "load comments", "data": comments}
                self.send(message, socket_client)


    def blurr_image(self, img):

        with open("Imagenes/{}".format(img), "rb") as file:
            img_bytes = file.read()

        img_bytes = self.extract_bytes(img_bytes)

        dicc = self.classify_bytes(img_bytes)

        ihdr_chunk = dicc["IHDR"]
        length = int.from_bytes(ihdr_chunk[:4], byteorder="big")
        type_b = ihdr_chunk[4:8]
        width = int.from_bytes(ihdr_chunk[8:12], byteorder="big")
        height = int.from_bytes(ihdr_chunk[12:16], byteorder="big")

        idat_chunk = dicc["IDAT"]

        length_b = idat_chunk[:4]
        length = int.from_bytes(length_b, byteorder="big")

        type = idat_chunk[4:8]

        a = idat_chunk[8:8 + length]

        idat_dat = zlib.decompress(a)

        if height * ((width * 3) + 1) % len(idat_dat) == 0:
            bytes_por_pixeles = 3
        else:
            bytes_por_pixeles = 4

        matrices = []
        i = 0
        for _ in range(bytes_por_pixeles):
            matrix = [idat_dat[n - ((width * bytes_por_pixeles) + 1):n] for n
                      in range((width * bytes_por_pixeles) + 1,
                               len(idat_dat) + (
                               (width * bytes_por_pixeles) + 1),
                               (width * bytes_por_pixeles) + 1)]

            matrix = [self.filtrar(fila, i, bytes_por_pixeles) for fila in matrix]
            nueva_matriz = self.new_matrix(matrix)
            matrices.append(nueva_matriz)

            i += 1

        final = b''
        for _ in range(len(matrices[0])):
            row = [0]
            for i in range(len(matrices[0][0])):
                row.append(matrices[0][_][i])
                row.append(matrices[1][_][i])
                row.append(matrices[2][_][i])
                if bytes_por_pixeles == 4:
                    row.append(matrices[3][_][i])
            final += bytes(row)

        final = zlib.compress(final)

        new_len = len(final).to_bytes(4, byteorder="big")
        type = "IDAT".encode()
        new_crc = zlib.crc32(type + final).to_bytes(4, byteorder="big")

        with open("Imagenes/{}".format(img), "wb") as file:
            f = dicc["firm"] + dicc[
                "IHDR"] + new_len + type + final + new_crc + dicc["IEND"]
            file.write(f)

        message = self.request_img_update(img)
        for user in self.clients:
            self.send(message, user[1])


    def classify_bytes(self, bytes):
        cla = {}
        idat_bytes = b''

        firm = bytes[:8]
        cla["firm"] = firm

        i = 8
        while i < len(bytes):

            length_bytes = bytes[i:i + 4]
            length = int.from_bytes(length_bytes, byteorder="big")
            i += 4
            type_bytes = bytes[i:i + 4]
            type = type_bytes.decode()
            i += 4
            data = bytes[i:i + length]
            i += length
            crc = bytes[i:i + 4]
            i += 4

            if type == "IHDR" or type == "IEND":
                cla[type] = length_bytes + type_bytes + data + crc
            else:
                idat_bytes += data

        new_length = len(idat_bytes).to_bytes(4, byteorder="big")
        type = "IDAT".encode()
        new_crc = zlib.crc32(type + idat_bytes).to_bytes(4, byteorder="big")

        cla["IDAT"] = new_length + type + idat_bytes + new_crc

        return cla

    def filtrar(self, fila, i, per):
        fila = fila[1:]
        fila_nueva = [fila[n] for n in range(i, len(fila), per)]
        return bytes(fila_nueva)

    def new_matrix(self, matrix):
        new_matr = []
        i = 0
        for fila in matrix:
            j = 0
            new_row = []
            for byte in fila:
                new_row.append(self.ponderar(byte, i, j, matrix))
                j += 1
            new_matr.append(new_row)
            i += 1

        return new_matr

    def ponderar(self, byte, i, j, original):
        up = 0
        down = 0
        left = 0
        right = 0
        up_right = 0
        up_left = 0
        lo_right = 0
        lo_left = 0

        center = original[i][j] * 4

        if i - 1 > 0:
            up = original[i - 1][j] * 2
        if i + 1 < len(original):
            down = original[i + 1][j] * 2
        if j - 1 > 0:
            left = original[i][j - 1] * 2
        if j + 1 < len(original[0]):
            right = original[i][j + 1] * 2

        if i - 1 > 0 and j + 1 < len(original[0]):
            up_right = original[i - 1][j + 1]
        if i - 1 > 0 and j - 1 > 0:
            up_left = original[i - 1][j - 1]
        if i + 1 < len(original) and j + 1 < len(original[0]):
            lo_right = original[i + 1][j + 1]
        if i + 1 < len(original) and j - 1 > 0:
            lo_left = original[i + 1][j - 1]

        number = up + down + left + right + up_left + up_right + lo_left + lo_right + center
        number = number / 16
        number = numpy.round(number, 0)

        return int(number)

    def cut_image(self, info):
        posiciones = info[0]
        img = info[1]

        with open("Imagenes/{}".format(img), "rb") as file:
            img_bytes = file.read()

        img_bytes = self.extract_bytes(img_bytes)

        dicc = self.classify_bytes(img_bytes)

        maxi_x = int(max((posiciones[0][0], posiciones[1][0])))
        mini_x = int(min((posiciones[0][0], posiciones[1][0])))

        maxi_y = int(max((posiciones[0][1], posiciones[1][1])))
        mini_y = int(min((posiciones[0][1], posiciones[1][1])))

        width, height = self.width_height(dicc["IHDR"])

        idat_bytes = dicc["IDAT"]

        length = int.from_bytes(idat_bytes[:4], byteorder="big")
        type_bytes = idat_bytes[4:8]
        idat_info = idat_bytes[8:8 + length]
        idat_crc = idat_bytes[8 + length:8 + length + 4]

        idat_dat = zlib.decompress(idat_info)

        if height * ((width * 3) + 1) % len(idat_dat) == 0:
            bytes_por_pixeles = 3
        else:
            bytes_por_pixeles = 4

        matrix = [idat_dat[n - ((width * bytes_por_pixeles) + 1):n]
                  for n in range((width * bytes_por_pixeles) + 1,
                                 len(idat_dat) + (
                                 (width * bytes_por_pixeles) + 1),
                                 (width * bytes_por_pixeles) + 1)]

        final = b''

        for fila in range(mini_y):
            final += matrix[fila]

        for fila in range(mini_y, maxi_y, 1):
            array = bytearray(matrix[fila])
            if bytes_por_pixeles == 3:
                b = bytes([255, 255, 255] * (maxi_x - mini_x))
                array[(mini_x * 3)-3 + 1:(maxi_x * 3)-3 + 1] = b
            else:
                b = bytes([255, 255, 255, 255] * (maxi_x - mini_x))
                array[(mini_x*4)-4 + 1:(maxi_x*4)-4 + 1] = b

            final += bytes(array)

        for fila in range(maxi_y, len(matrix), 1):
            final += matrix[fila]

        final = zlib.compress(final)

        new_length = len(final).to_bytes(4, byteorder="big")
        type = "IDAT".encode()
        new_crc = zlib.crc32(type + final).to_bytes(4, byteorder="big")

        with open("Imagenes/{}".format(img), "wb") as file:
            f = dicc["firm"] + dicc[
                "IHDR"] + new_length + type + final + new_crc + dicc["IEND"]
            file.write(f)

        message = self.request_img_update(img)
        for user in self.clients:
            self.send(message, user[1])

    def width_height(self, ihdr_chunk):
        length = int.from_bytes(ihdr_chunk[:4], byteorder="big")
        type_b = ihdr_chunk[4:8]
        width = int.from_bytes(ihdr_chunk[8:12], byteorder="big")
        height = int.from_bytes(ihdr_chunk[12:16], byteorder="big")

        return width, height

    def bucket_image(self, info):

        position = info[0]
        img = info[2]
        color = info[1]

        with open("Imagenes/{}".format(img), "rb") as file:
            img_bytes = file.read()

        img_bytes = self.extract_bytes(img_bytes)
        dicc = self.classify_bytes(img_bytes)

        width, height = self.width_height(dicc["IHDR"])
        idat_bytes = dicc["IDAT"]

        length = int.from_bytes(idat_bytes[:4], byteorder="big")
        type_bytes = idat_bytes[4:8]
        idat_info = idat_bytes[8:8 + length]
        idat_crc = idat_bytes[8 + length:8 + length + 4]

        idat_dat = zlib.decompress(idat_info)

        if height * ((width * 3) + 1) % len(idat_dat) == 0:
            bytes_por_pixeles = 3
        else:
            bytes_por_pixeles = 4
            color = (color[0], color[1], color[2], 255)

        matrix = [idat_dat[n - ((width * bytes_por_pixeles) + 1):n]
                  for n in range((width * bytes_por_pixeles) + 1,
                                 len(idat_dat) + (
                                 (width * bytes_por_pixeles) + 1),
                                 (width * bytes_por_pixeles) + 1)]

        matrix = [self.group_by(x, bytes_por_pixeles) for x in matrix]

        x_start = int(position[0])
        y_start = int(position[1])
        color_base = matrix[y_start][x_start]

        checked = set()
        por_revisar = [(x_start, y_start)]

        i = 0

        while len(por_revisar) != 0:
            revisar = por_revisar.pop(0)
            checked.add(revisar)

            if revisar[0] + 1 < len(matrix[0]):
                if matrix[revisar[1]][revisar[0] + 1] == color_base and (
                    revisar[0] + 1, revisar[1]) not in checked and (
                    revisar[0] + 1, revisar[1]) not in por_revisar:
                    por_revisar.append((revisar[0] + 1, revisar[1]))

                if revisar[1] - 1 > 0:
                    if matrix[revisar[1] - 1][
                                revisar[0] + 1] == color_base and (
                        revisar[0] + 1, revisar[1] - 1) not in checked and (
                        revisar[0] + 1, revisar[1] - 1) not in por_revisar:
                        por_revisar.append((revisar[0] + 1, revisar[1] - 1))

                if revisar[1] + 1 < len(matrix):
                    if matrix[revisar[1] + 1][
                                revisar[0] + 1] == color_base and (
                        revisar[0] + 1, revisar[1] + 1) not in checked and (
                        revisar[0] + 1, revisar[1] + 1) not in por_revisar:
                        por_revisar.append((revisar[0] + 1, revisar[1] + 1))

            if revisar[1] + 1 < len(matrix):
                if matrix[revisar[1] + 1][revisar[0]] == color_base and (
                revisar[0], revisar[1] + 1) not in checked and (
                revisar[0], revisar[1] + 1) not in por_revisar:
                    por_revisar.append((revisar[0], revisar[1] + 1))

            if revisar[0] - 1 > 0:
                if matrix[revisar[1]][revisar[0] - 1] == color_base and (
                    revisar[0] - 1, revisar[1]) not in checked and (
                    revisar[0] - 1, revisar[1]) not in por_revisar:
                    por_revisar.append((revisar[0] - 1, revisar[1]))

                if revisar[1] - 1 > 0:
                    if matrix[revisar[1] - 1][
                                revisar[0] - 1] == color_base and (
                        revisar[0] - 1, revisar[1] - 1) not in checked and (
                        revisar[0] - 1, revisar[1] - 1) not in por_revisar:
                        por_revisar.append((revisar[0] - 1, revisar[1] - 1))

                if revisar[1] + 1 < len(matrix):
                    if matrix[revisar[1] + 1][
                                revisar[0] - 1] == color_base and (
                        revisar[0] - 1, revisar[1] + 1) not in checked and (
                        revisar[0] - 1, revisar[1] + 1) not in por_revisar:
                        por_revisar.append((revisar[0] - 1, revisar[1] + 1))

            if revisar[1] - 1 > 0:
                if matrix[revisar[1] - 1][revisar[0]] == color_base and (
                revisar[0], revisar[1] - 1) not in checked and (
                revisar[0], revisar[1] - 1) not in por_revisar:
                    por_revisar.append((revisar[0], revisar[1] - 1))

            i += 1

        new_idat_info = b''

        r = 0
        for row in matrix:
            p = 0
            new_row = [0]
            for pixel in row:
                if (p, r) in checked:
                    new_row.extend(color)
                else:
                    new_row.extend(matrix[r][p])
                p += 1
            r += 1

            new_idat_info += bytes(new_row)

        new_idat_info = zlib.compress(new_idat_info)

        new_length = len(new_idat_info).to_bytes(4, byteorder="big")
        type = "IDAT".encode()
        new_crc = zlib.crc32(type + new_idat_info).to_bytes(4, byteorder="big")

        with open("Imagenes/{}".format(img), "wb") as file:
            f = dicc["firm"] + dicc[
                "IHDR"] + new_length + type + new_idat_info + new_crc + dicc[
                    "IEND"]
            file.write(f)

        message = self.request_img_update(img)
        for user in self.clients:
            self.send(message, user[1])

    def group_by(self, row_bytes, n):
        row_bytes = row_bytes[1:]
        row = [row_bytes[i:i + n] for i in range(0, len(row_bytes), n)]
        return row

    def save_new_image(self, img_data):
        img_name = img_data[0]

        with open("Imagenes/{}".format(img_name), "wb") as file:
            file.write(bytes(img_data[1]))


if __name__ == '__main__':
    server = Server()

    while True:
        pass
