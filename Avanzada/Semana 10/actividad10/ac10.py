import random
import threading
import time


class Tecnico:

    lock = threading.Lock()

    def __init__(self):
        self.nombre = "Tecnico"

    def reparar(self, bicicleta):
        wait = random.randint(2, 5)
        time.sleep(wait)
        bicicleta.averiada = False
        print("[Tecnico]: He reparado la bicicleta {}".format(bicicleta.nombre))
        print("Tecnico comienza a reparar en {}".format(bicicleta.tiempo))
        bicicleta.tiempo += wait
        print("Tecnico termino de reparar en {}".format(bicicleta.tiempo))


class Bicicleta(threading.Thread):

    tecnico = Tecnico()

    def __init__(self, nombre, genio):
        super().__init__()
        self.nombre = nombre
        self.velocidad = random.randint(20, 60)
        self.posicion = 0
        self.genio = genio
        self.averiada = False
        self.velocidad_reducida = False
        self.tiempo = 0

    def reducir_velocidad(self):
        if self.posicion >= 200 and not self.velocidad_reducida:
            reducir = random.randint(0, 5)
            if self.velocidad - reducir >= 15:
                self.velocidad -= random.randint(0, 5)
            else:
                self.velocidad = 15
            print("La velocidad de {} fue reducida a {}".format(self.nombre,
                                                                self.velocidad))
            self.velocidad_reducida = True


    @property
    def prox_averia(self):
        if self.posicion >= 300:
            num = random.randint(1, 10)
            if num == 1:
                self.averiada = True
        return self.averiada

    def run(self):
        while self.posicion < 600:
            self.tiempo += 1
            self.posicion += self.velocidad
            self.reducir_velocidad()
            if self.prox_averia:
                with Bicicleta.tecnico.lock:
                    Bicicleta.tecnico.reparar(self)


    def __str__(self):
        return "Bicleta: {}".format(self.nombre)


class Rescate:

    id = 1

    def __init__(self):

        self.participantes = []
        self.tecnico = Tecnico()
        self.tiempo_actual = 0
        self.finalizar = False

    def verificar_meta(self):
        while not self.finalizar:
            for ciclista in self.participantes:
                if ciclista.genio.resuelto and ciclista.posicion >= 600:
                    self.finalizar = True
                    ganador = ciclista

        print("El ganador a ha sido {}".format(ciclista.nombre))
        print("El genio ganador fue {}".format(ciclista.genio.nombre))
        print("El tiempo de demora fue de {}".format(ciclista.tiempo))
        print("Presentacion de Ciclista")
        for i in self.participantes:
            print('El nombre del ciclista es {}, quedamos en la posicion {},'
                  ' el nombre del genio es {} '
                  'and its {} that we resolved the problem'.format(i.nombre,
                                                                   i.posicion,
                                                                   i.genio.nombre,
                                                                   i.genio.resuelto))



    def agregar_participante(self, participante):
        self.participantes.append(participante)


    def run(self):
        print("Ha comenzado el Rescate!")

        for participante in self.participantes:
            participante.setDaemon(True)
            participante.genio.setDaemon(True)

            participante.genio.start()
            participante.start()

        watch = threading.Thread(target=self.verificar_meta())
        watch.start()


class Genio(threading.Thread):

    lock = threading.Lock()

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.resuelto = False

    def __str__(self):
        return "Nombre: {}".format(self.nombre)

    @staticmethod
    def murcielago(text):
        diccionario = {0: "M", 1: "U", 2: "R", 3: "C", 4: "I", 5: "E",
                       6: "L", 7: "A", 8: "G", 9: "O"}

        solucion = []
        for parrafo in text:

            parr_solucion = ""

            for linea in parrafo:

                for caract in linea:

                    if caract.isdigit():
                        parr_solucion += diccionario[int(caract)].lower()
                    else:
                        parr_solucion += caract.lower()

            solucion.append(parr_solucion)

        return solucion



    def abrir_sobre(self):
        time.sleep(random.randint(15, 25))


    def run(self):
        while not self.resuelto:
            self.abrir_sobre()
            with open("Problema.txt", "r") as archivo:
                texto = [linea.strip().split(";") for linea in archivo]
            solucion = self.murcielago(texto)
            self.resuelto = True

        print("{}: Lo he resuelto!".format(self.nombre))

        with Genio.lock:
            with open("solucion.txt", "w") as arch:
                for parrafo in solucion:
                    print(parrafo, file=arch)


if __name__ == "__main__":
    rescate = Rescate()
    rescate.agregar_participante(Bicicleta("Ciclista 1", Genio("Genio 1")))
    rescate.agregar_participante(Bicicleta("Ciclista 2", Genio("Genio 2")))
    rescate.agregar_participante(Bicicleta("Ciclista 3", Genio("Genio 3")))
    rescate.run()