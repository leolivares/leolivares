
class Sonia :

    def __init__(self):
        self.productos = []


class Audifono :

    def __init__(self,min,max,impe,intensidad):
        self.min = min
        self.max = max
        self.impe = impe
        self.intensidad = intensidad

    def reproducir(self,cancion):
        print("La cancion {} esta siendo reproducida desde un audifono")


class Circumaurales(Audifono) :

    def __init__(self,min,max,impe,intensidad):
        super().__init__(min,max,impe,intensidad)


class Intraaurales(Audifono):
    def __init__(self, min, max, impe, intensidad):
        super().__init__(min, max, impe, intensidad)


class Inalambrico(Audifono):
    def __init__(self, min, max, impe, intensidad):
        super().__init__(min, max, impe, intensidad)

    def reproducir(self,cancion):
        print("La cancion {} esta siendo reproducida desde un audifono inalambrico")

class Bluetooth()
