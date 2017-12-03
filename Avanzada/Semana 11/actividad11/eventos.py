class Ingreso:

    def __init__(self, nombre):
        self.usuario = nombre

class Apostar:
    def __init__(self, usuario, cant, imagenes=None):
        self.cant = cant
        self.usuario = usuario
        self.imagenes = imagenes