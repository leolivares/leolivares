import re
import requests


with open("ay15.txt", "r", encoding="utf-8") as file:
    texto = file.read()

    parrafos = re.split("\n\n", texto)


def validar_primero(s):
    pattern = "[0-9]"
    return not bool(re.search(pattern, s))

def validar_segundo(s):
    pattern = "[a-zA-Z0-9]*(\.correcta)[a-zA-Z0-9]*"
    return bool(re.search(pattern, s))

def validar_tercero(s):
    pattern = "[a-z]*(\.)[a-z]*"
    return bool(re.match(pattern, s))

def filtrar_palabras(parrafo, criterio):
    palabras = re.split("@", parrafo)

    for palabra in palabras:
        if criterio(palabra):
            yield palabra

def nice_format(palabra):
    if palabra[-1] == "\n":
        return palabra[:-1] + " "
    else:
        return palabra + " "

with open("ayu15.txt", "w", encoding="utf-8") as file:
    enunciado = []

    for palabra in filtrar_palabras(parrafos[0], validar_primero):
        enunciado.append(palabra)

    for palabra in filtrar_palabras(parrafos[1], validar_segundo):
        palabra_nueva = re.sub("\.correcta", "", palabra)
        enunciado.append(palabra_nueva)

    for palabra in filtrar_palabras(parrafos[2], validar_tercero):
        palabra_nueva = re.sub("\.", "", palabra)
        enunciado.append(palabra_nueva)


    file.write(" ".join(enunciado))