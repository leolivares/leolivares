import threading
import socket
import sys
import json


class Client:

    def __init__(self):

        self.host = "localhost"
        self.port = 5555
        self.connected = False
        self.map = None


        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:

            self.socket_client.connect((self.host, self.port))
            self.connected = True

            thread = threading.Thread(target=self.listen_server, daemon=True)
            thread.start()


        except ConnectionRefusedError:
            self.socket_cliente.close()
            exit()

    def listen_server(self):
        print("Bienvenido a Battleship")
        print("Esperando otro jugador")
        while self.connected:
            length_bytes = self.socket_client.recv(4)
            length = int.from_bytes(length_bytes, byteorder="big")

            respuesta = bytearray()
            while len(respuesta) < length:
                respuesta += self.socket_client.recv(256)

            respuesta = respuesta.decode()
            decoded = json.loads(respuesta)

            self.analizar_mensaje(decoded)

    def analizar_mensaje(self, decoded):
        print(decoded)
        if decoded["status"] == "mapa":
            map = decoded["data"]["board"]
            i = 1
            for fila in map:
                print(i, " ".join(fila))
                i += 1
            print("  a b c d e")

            self.ask_move()

        elif decoded["status"] == "resultados":
            print(decoded["data"])
            if len(decoded["data"]) != 2:
                print("El perdedor es el jugador {}".format(str(decoded["data"][0])))
                print("El ganador es el jugador {}".format("otro"))


    def ask_move(self):
        disparo = input("Ingresa la casilla que deseas disparar: ")
        message = {"status": "disparo", "data": disparo}
        self.send(message)

    def send(self, msg):

        msg_json = json.dumps(msg)
        msg_bytes = msg_json.encode()

        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        self.socket_client.send(msg_length + msg_bytes)





if __name__ == '__main__':

    client = Client()
    while True:
        pass
