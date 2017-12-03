from collections import deque
from collections import defaultdict , namedtuple


class CentroDeDistribucion :

    def __init__(self):
        self.fila = deque()
        self.bodega = defaultdict(int)
        self._parametro = None
        self.produtos = list()

    @property
    def parametro(self):
        return self._parametro

    @parametro.setter
    def parametro(self,value):
        if value < 0 :
            self._parametro = 0
        elif value > 100 :
            self._parametro = 100
        else :
            self._parametro = value


    def recibir_camion(self,camion):
        i = 0
        for cam in self.fila :
            if cam.urgencia == camion.urgencia :
                self.fila.insert(i,camion)
            i += 1


    def rellenar_camion(self):
        camion = self.fila[0]


    def enviar_camion(self):
        camion = self.fila[0]
        kilos = 0
        for prod in camion.productos :
            kilos += prod.peso
        if camion.capacidad_maxima == kilos :
            self.fila.popleft()


    def mostrar_productos(self):
        tipos = set()
        for prod in self.produtos :
            tipos += prod.tipo

        for tipo in tipos :
            cant = 0
            for prod in self.produtos :
                if prod.tipo == tipo :
                    cant += 1
            print("Cantidad de {}: {}".format(tipo,cant))

    def recibir_donacion(self,*args):
        for prod in args :
            self.bodega[prod.nombre] += 1
            self.produtos.append(prod)



class Camion :

    def __init__(self,maxi,urgencia):
        self.capacidad_maxima = maxi
        self.urgencia = urgencia
        self.tipos = defaultdict(int)
        self.productos = list()

    def agregar_producto(self,producto):
        self.productos.append(producto)
        self.tipos[producto.nombre] += 1

    def __str__(self):
        msj = "El camion esta cargado con :" "\n"
        if len(self.tipos) != 0 :
            for key , value in self.tipos :
                msj += key +": " + value + "\n"
        else :
            msj = "El camion no tiene productos en el momento"
        return msj


class Producto :

    def __init__(self,nombre,tipo,peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso



cam = Camion(123,12)
print(cam)

dict = {"algo1" : 1 , "algo2" : 2}
for key in dict :
    print(key , dict[key])

