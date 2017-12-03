import socket

#Hacer un cliente basico

HOST = "localhost"
PORT = 1235

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_cliente.connect((HOST, PORT))

data = ""
while data != "fin":
    data = input()
    msg = "{}".format(data).encode()

    socket_cliente.send(msg)

    datos2 = socket_cliente.recv(1024)
    print(datos2.encode())

print("desconectado")
socket_cliente.close()