import threading


class Laberinto():

    def __init__(self):
        self.espacios = dict()

    def agregar_vertice(self, x):
        if x not in self.espacios:
            self.espacios[x] = set()

    def agregar_eje(self, x, y):
        if x in self.espacios:
            self.espacios[x].add(y)

    def leer_laberinto(self, archivo):
        with open(archivo) as arch:
            lineas = [linea.strip() for linea in arch]
            inicio = lineas.pop()
            final = lineas.pop()
            lineas = lineas[2:]
            conexiones = [(x.split(",")[0], x.split(",")[1]) for x in lineas]
        set = {x[0] for x in conexiones}
        for x in conexiones:
            set.add(x[1])
        for x in set:
            self.agregar_vertice(x)
        for y in conexiones:
            self.agregar_eje(y[0], y[1])
        print(self)

    def __str__(self):
        msj = ""
        for x in self.espacios:
            a = x + str(self.espacios[x]) + "\n"
            msj += a
        return msj




if __name__ == "__main__":
    lab = Laberinto()
    lab.leer_laberinto("laberinto.txt")
