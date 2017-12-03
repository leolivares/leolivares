import socket
import threading
import sys
import json
from battleship import Battleship

class Server:

    def __init__(self):
        self.host = "localhost"
        self.port = 5555

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(2)

        thread = threading.Thread(target=self.accept_connections, daemon=True)
        thread.start()

        self.jugadores = {}
        self.socket_jugadores = {1: None, 2: None}
        self.maps = {1: None, 2: None}
        self.ataques = {1: None, 2: None}
        self.posiciones = ["a1", "a2", "a3", "a4", "a5",
                           "b1", "b2", "b3", "b4", "b5",
                           "c1", "c2", "c3", "c4", "c5",
                           "d1", "d2", "d3", "d4", "d5",
                           "e1", "e2", "e3", "e4", "e5"]

    def accept_connections(self):
        while True:
            client_socket, address = self.socket_server.accept()

            if len(self.jugadores) == 0:
                self.jugadores[client_socket] = "jugador1"
                self.socket_jugadores[1] = client_socket
                num_jugador = 1

            elif len(self.jugadores) == 1:
                self.jugadores[client_socket] = "jugador2"
                self.socket_jugadores[2] = client_socket
                num_jugador = 2

            thread = threading.Thread(target=self.listen_client, daemon=True, args=(client_socket,))
            thread.start()

            if len(self.jugadores) == 2:
                self.comenzar_partida()
                break
        print("BREAKEADO")


    def listen_client(self, client_socket):
        while True:
            length_bytes = client_socket.recv(4)
            length = int.from_bytes(length_bytes, byteorder="big")

            respuesta = bytearray()
            while len(respuesta) < length:
                respuesta += client_socket.recv(256)

            respuesta = respuesta.decode()
            decoded = json.loads(respuesta)

            self.analizar_mensaje(decoded, client_socket)

    def comenzar_partida(self):


        i = 1
        for jugador in self.jugadores:
            battle = Battleship(boardsize=5, max_ships=5, loaded=True)
            self.maps[i] = battle

            if i == 1:
                map_message = {"status": "mapa", "data": battle.p1.board.__dict__}
            elif i == 2:
                map_message = {"status": "mapa",
                               "data": battle.p2.board.__dict__}

            self.send(map_message, self.socket_jugadores[i])

            i += 1


    def analizar_mensaje(self, decoded, client_socket):
        print(decoded)
        if decoded["status"] == "disparo":
            print(decoded["data"])
            if self.jugadores[client_socket] == "jugador1":
                self.maps[2].attack("P1", str(decoded["data"]))
                self.ataques[1] = decoded["data"]
            elif self.jugadores[client_socket] == "jugador2":
                self.maps[1].attack("P2", str(decoded["data"]))
                self.ataques[2] = decoded["data"]

            if self.ataques[1] is not None and self.ataques[2] is not None:
                self.send({"status": "mapa", "data": self.maps[1].p1.board.__dict__}, self.socket_jugadores[1])
                self.send({"status": "mapa", "data": self.maps[2].p2.board.__dict__}, self.socket_jugadores[2])

                i = 1
                loser = []
                for mapa in self.maps:
                    alive = False
                    if i == 1:
                        for fila in self.maps[mapa].p1.board.__dict__["board"]:
                            print(fila)
                            if "O" in fila:
                                alive = True

                        if not alive:
                            loser.append(i)

                    elif i == 2:
                        for fila in self.maps[mapa].p2.board.__dict__["board"]:
                            print(fila)
                            if "O" in fila:
                                alive = True

                        if not alive:
                            loser.append(i)
                    i += 1

                print(loser)
                if len(loser) != 0:
                    self.culminar_partida(loser)

                self.ataques[1] = None
                self.ataques[2] = None

    @staticmethod
    def send(value, socket):

        print(value)
        msg_json = json.dumps(value)
        msg_bytes = msg_json.encode()

        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        socket.send(msg_length + msg_bytes)

    def culminar_partida(self, loser):
        for jugador in self.socket_jugadores:
            message = {"status": "resultados", "data": loser}
            self.send(message, self.socket_jugadores[jugador])

if __name__ == '__main__':
    server = Server()

    while True:
        pass

