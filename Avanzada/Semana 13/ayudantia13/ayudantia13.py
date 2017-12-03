import pickle
import json
import os
from random import randint
from datetime import datetime


class Usuario:
    def __init__(self, name, contacts, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.contacts = contacts


class Mensaje:
    def __init__(self, send_to, content, send_by, date, last_view_date):
        self.send_to = send_to
        self.content = content
        self.send_by = send_by
        self.last_view_date = last_view_date
        self.date = date

    def __getstate__(self):
        dict_mensaje = self.__dict__.copy()
        dict_mensaje["content"] = caesarCipher(dict_mensaje["content"],
                                               dict_mensaje["send_by"])

        return dict_mensaje

    def __setstate__(self, diccionario):
        d = datetime.now()
        diccionario["last_view_date"] = "{}/{}/{}-{}:{}".format(d.year,
                                                                d.month, d.day,
                                                                d.hour,
                                                                d.minute)
        self.__dict__ = diccionario


def readUsers():
    users = []
    for path in os.listdir("db/usr"):
        with open("db/usr/" + path, "r") as f:
            user = json.load(f,
                             object_hook=lambda dict_obj: Usuario(**dict_obj))
        users.append(user)
    print(users)
    return users


def readMessages():
    mensajes = []
    for path in os.listdir("db/msg"):
        with open("db/msg/" + path, "r") as f:
            msg = json.load(f,
                            object_hook=lambda dict_obj: Mensaje(**dict_obj))
        mensajes.append(msg)

    return mensajes

def updateUsers(usarios, mensajes):
    users = {user.phone_number: user for user in usuarios}
    for mensaje in mensajes:
        u_envio = mensaje.send_by
        u_recive = mensaje.send_to
        if u_recive not in users[u_envio].contacts:
            users[u_envio].contacts.append(u_recive)


def saveUsers(usuarios):
    for usuario in usuarios:
        path = "secure_db/usr/{}".format(str(usuario.phone_number))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(usuario.__dict__, f)


def saveEncriptedMessages(mensajes):
    for msg in mensajes:
        # el randint es solo pa crear el nombre del archivo en donde se va a guardar
        path = "secure_db/msg/{}".format(str(randint(0, 99999999)))
        with open(path, "wb") as f:
            pickel.dump(msg, f)


def caesarCipher(string, key):
    new = ""
    for caracter in string:
        if caracter.isalpha():
            # 97 = orden de la a
            ascii_value = ord(caracter) - 97
            value = ascii_value + key
            value = value % 26
            nuevo_caracter = chr(value + 97)

            new += nuevo_caracter

    return new


if __name__ == '__main__':
    usuarios = readUsers()
    mensajes = readMessages()
    updateUsers(usuarios, mensajes)
