import socket

# Hacer un servidor basico

HOST = "localhost" #O direcc ip
PORT = 1235

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_servidor.bind((HOST, PORT))

socket_servidor.listen(5)

socket_conectado, adress = socket_servidor.accept()
print("cliente aceptado")

print(adress)

data = ""
while data != "fin":
    data = socket_conectado.recv(1024)
    data = data.decode()
    print(data)

    socket_conectado.send("server: {}".format(data).encode())



print("desconectado")
socket_conectado.close()
socket_servidor.close()
