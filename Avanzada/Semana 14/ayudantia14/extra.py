import threading

def bind_and_listen(self):
    self.socket_servidor.bind((self.host, self.port))
    self.socket_servidor.listen()

def accept_connections(self):

    thread = threading.Thread(target=self.accepting(self))


def accepting(self):

    while True:
        socket, _ = self.socket_servidor.accept()

        # if ....

        thread = threading.Thread(target=listening, daemon=True, args=(socket,))
        thread.start()

def listening(self, socket):
    while True:
        data = socket.recv(1024)
        # Recibir de tamano y luego por chunks


        response_bytes_length = socket.recv(4)
        response__length = 2
