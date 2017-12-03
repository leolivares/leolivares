import re
import json
import requests


URL = "https://westCentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=gender,glasses,hair,smile,facialHair"
HEADER = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': '01486c3ae8fc4d9297872385f18cab58'}

personas = []

class Persona:

    def __init__(self, url, gender, glasses, hair, smile, facial_hair, descripcion):
        self.url = url
        self.gender = gender
        self._glasses = glasses
        self.hair_color = hair
        self._smile = smile
        self.facial_hair = facial_hair
        self.descripcion = descripcion

    @property
    def smile(self):
        if self._smile > 0.5:
            return True
        return False

    @property
    def glasses(self):
        if self._glasses != "NoGlasses":
            return True
        return False



def read_faces():
    with open("faces.txt", "r") as file:
        parser = lambda x: x.strip().split(";")
        faces = {parser(linea)[0]: parser(linea)[1] for linea in file.readlines()}

    return faces


def primer_cambio(faces):
    for descripcion in faces:
        pattern = "[$][0-9]+"
        faces[descripcion] = re.sub(pattern, " ", faces[descripcion])
    return faces


def segundo_cambio(faces):
    for descripcion in faces:
        pattern = "[$][A-Z]{2}"
        faces[descripcion] = re.sub(pattern, "", faces[descripcion])
    return faces


def save_new(faces):
    with open("faces_clean.txt", "w") as file:
        for face in faces:
            print(face, faces[face], file=file, sep=";")


def request_url(url):
    data = {"url": url}
    data = json.dumps(data)

    value = requests.post(URL, headers=HEADER, data=data)
    value = value.json()

    info_necesaria = [url, value[0]["faceAttributes"]["gender"], value[0]["faceAttributes"]["glasses"]]

    max = 0
    color_hair = ""
    for color in value[0]["faceAttributes"]["hair"]["hairColor"]:
        if color["confidence"] > max:
            color_hair = color["color"]
            max = color["confidence"]
    info_necesaria.append(color_hair)

    info_necesaria.append(value[0]["faceAttributes"]["smile"])

    max = 0
    facial_hair = ""
    for facial in value[0]["faceAttributes"]["facialHair"]:
        if value[0]["faceAttributes"]["facialHair"][facial] > max:
            facial_hair = facial
            max = value[0]["faceAttributes"]["facialHair"][facial]
    info_necesaria.append(facial_hair)

    return info_necesaria

def buscar_match(datos):
    genero = datos[0]
    hair_color = datos[1]
    glasses = datos[2]
    smile = datos[3]
    facial_hair = datos[4]

    posible = list(filter(lambda x: x.gender == genero and
                                    x.hair_color == hair_color and
                                    x.glasses == glasses and
                                    x.smile == smile and
                                    x.facial_hair == facial_hair, personas))


    print("------------------------")
    print("ESTOS SON LOS MATCHES")
    for p in posible:
        print(p.url, p.descripcion)

    print("------------------------")


if __name__ == '__main__':
    faces = read_faces()
    faces = primer_cambio(faces)
    faces = segundo_cambio(faces)
    save_new(faces)

    info_total = []

    print("Realizando Requests...")
    for face in faces:
        info = request_url(face)
        info_total.append(info)
        info.append(faces[face])
        per = Persona(*info)
        personas.append(per)


    while True:
        datos = []
        print("Hola! Elije atributos:")
        print("   Gender:")
        print("[1] Male")
        print("[2] Female")
        selecc = input("Eleccion: ")

        if selecc == "1":
            datos.append("male")
        elif selecc == "2":
            datos.append("female")

        print("  ")
        print("   Hair Color:")
        print("[1] Blond")
        print("[2] Brown")
        print("[3] Black")
        selecc = input("Eleccion: ")

        if selecc == "1":
            datos.append("blond")
        elif selecc == "2":
            datos.append("brown")
        elif selecc == "3":
            datos.append("black")

        print("  ")
        print("   Glasses:")
        print("[1] True")
        print("[2] False")
        selecc = input("Eleccion: ")

        if selecc == "1":
            datos.append(True)
        elif selecc == "2":
            datos.append(False)

        print("  ")
        print("   Smile:")
        print("[1] True")
        print("[2] False")
        selecc = input("Eleccion: ")

        if selecc == "1":
            datos.append(True)
        elif selecc == "2":
            datos.append(False)

        print("  ")
        print("   Facial Hair:")
        print("[1] beard")
        print("[2] sideburns")
        print("[3] none")
        selecc = input("Eleccion: ")

        if selecc == "1":
            datos.append("beard")
        elif selecc == "2":
            datos.append("sideburns")
        elif selecc == "3":
            datos.append("")

        buscar_match(datos)
