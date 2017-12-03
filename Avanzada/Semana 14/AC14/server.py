import socket
import threading
import sys
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
        se


    def accept_connections(self):
        while True:
