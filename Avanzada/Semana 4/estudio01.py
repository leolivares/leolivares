class Isla :

    def __init__(self,nombre=None):
        self.siguiente = None
        self.nombre = nombre
        self.conexiones = list()

    def __repr__(self):
        return self.nombre

class Archipielago :

    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar_isla(self,nombre):
        if not self.cabeza :
            self.cabeza = Isla(nombre)
            self.cola = self.cabeza
        else :
            self.cola.siguiente = Isla(nombre)
            self.cola = self.cola.siguiente

    def buscar(self,nombre):
        revisar = [self.cabeza]
        existe = False
        while len(revisar) > 0 :
            isl = revisar.pop()
            if isl.nombre == nombre :
                existe = True
            else :
                revisar.append(isl.conexiones)
        return existe

    def conexiones(self,origen,destino):
        existe = self.buscar(destino)

        if not existe :
            self.agregar_isla(destino)

        revisar = [self.cabeza]
        while len(revisar) > 0:
            isla = revisa.pop()
            if isla.nombre == origen:
                agregado = False
                for i in isla.conexiones:
                    if i.nombre == destino:
                        agregado = True
                if not agregado:
                    isla.conexiones.append(destino)

            else:
                revisar.append(isla.conexiones)
