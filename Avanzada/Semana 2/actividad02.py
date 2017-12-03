
from abc import ABCMeta , abstractmethod
import datetime as dt
from datetime import date


def calcular_edad():
    today = date.today()
    return today.year - born.year - (
        (today.month, today.day) < (born.month, born.day))


class SuperMercado :

    def __init__(self):
        self.productos = []
        self.trabajadores = []


    def agregar_producto(self,producto):
        self.productos.append(producto)

    def agregar_trabajadores(self,trabajador):
        self.trabajadores.append(trabajador)


class Persona(metaclass=ABCMeta) :

    def __init__(self,nombre,fecha):
        self.nombre = nombre
        self.fecha = fecha

    @abstractmethod
    def saludar(self):
        pass

    @property
    def anios(self):

        year, month, day = self.fecha.split("-")
        r = dt.datetime(int(year), int(month), int(day))
        anios_hoy = edad(r)

        return anios_hoy



class Cliente(Persona) :

    def __init__(self,nombre=None,fecha=None,monto=None):
        super().__init__(nombre,fecha)
        self.__monto = monto
        self.carro = []

    def saludar(self):
        print("Hola! Soy un cliente")

    def agregar_producto(self,producto):
        encontrado = False
        for pro in self.carro :
            if pro.nombre == producto.nombre :
                pro[1] += 1
                encontrado = True

        if not encontrado :
            self.carro += [[producto,1]]

    def verificar(self,pago):

        puedo = True
        if pago > self.__monto :
            puedo = False
        return puedo

    def pagar(self,monto):
        self.__monto -= monto



class Cajero(Persona) :

    def saludar(self):
        print("Hola! Buenos dias! Soy un cajero! ")


    def cobrar(self,cliente):

        pagar = self.calcular_boleta(cliente)

        puede_pagar = cliente.verificar(pagar)

        if puede_pagar :
            cliente.pagar(pagar)

        else :
            print("Lo siento. No puede pagar")


    def calcular_boleta(self,cliente):
        cant = 0
        for prod in cliente.carro :
            i = prod[1]
            while i > 0 :
                cant += prod[0].precio
                i -= 1

        edad = cliente.anios
        if edad >= 60 :
            cant = cant * 0.9

        return cant



class Producto(metaclass=ABCMeta) :

    id = 0

    def __init__(self,nombre=None,precio=None):
        self.nombre = nombre
        self.sku = Producto.id
        self.precio = precio
        Producto.id += 1


    @abstractmethod
    def __str__(self):
        pass



class Comida(Producto,metaclass=ABCMeta) :

    def __init__(self,nombre=None,precio=None,info_nutri=None):
        super().__init__(nombre,precio)
        self.info_nutri = info_nutri

    def __str__(self):
        msj = a=""" [{}] {} $ {}
        calorias = {} (kcal)
        proteinas= {}(g)
        carh={}(g)
        Grasa={} (g)""".format(self.sku, self.nombre , self.precio,self.info_nutri[0],self.info_nutri[1],self.info_nutri[2],self.info_nutri[3])

        return msj

class Lacteos(Comida) :

    def __init__(self,nombre,precio,info_nutri,calcio):
        super().__init__(nombre,precio,info_nutri)
        self.calcio = calcio

    def __str__(self):
        msj = a=""" [{}] {} $ {}
        calorias = {} (kcal)
        proteinas= {}(g)
        carh={}(g)
        Grasa={} (g)
        Calcio = {} (mg)""".format(self.sku, self.nombre , self.precio,self.info_nutri[0],self.info_nutri[1],self.info_nutri[2],self.info_nutri[3],self.calcio)

        return msj


class Verduras(Comida) :


    def __init__(self, nombre, precio, info_nutri, vit_c):
        super().__init__(nombre, precio, info_nutri)
        self.vit_c = vit_c

    def __str__(self):
        msj = a = """ [{}] {} $ {}
        calorias = {} (kcal)
        proteinas= {}(g)
        carh={}(g)
        Grasa={} (g)
        Vitamina C = {} (mg)""".format(self.sku, self.nombre, self.precio, self.info_nutri[0], self.info_nutri[1],
                                   self.info_nutri[2], self.info_nutri[3], self.vit_c)
        return msj



class Carnes(Comida) :

    def __init__(self, nombre, precio, info_nutri, animal):
        super().__init__(nombre, precio, info_nutri)
        self.animal = animal

    def __str__(self):
        msj = a = """ [{}] {} $ {}
        calorias = {} (kcal)
        proteinas= {}(g)
        carh={}(g)
        Grasa={} (g)
        Proviene de = {} """.format(self.sku, self.nombre, self.precio, self.info_nutri[0], self.info_nutri[1],
                                   self.info_nutri[2], self.info_nutri[3], self.animal)
        return msj

class Vestuario(Producto) :

    def __init__(self,nombre=None,precio=None,info=None):
        super().__init__(nombre,precio)
        self.info = info

    def __str__(self):
        msj = a = """ [{}] {} $ {}
        Talla = {}
        Categoria = {}""".format(self.sku, self.nombre, self.precio,self.info[0],self.nombre[1])
        return msj


class Otros(Vestuario,Comida) :

    def __init__(self,**kwargs) :
        super().__init__(**kwargs)




pep_marino= Otros(nombre="Pepino Marino" , precio= 1000, info= ["Informacion","xs"])
pantalon_queso=Otros(nombre="Pantalon Queso" , precio=1000 , info=["Informacion sobre los pantalones de queso..."])
cajero=Cajero("Cajero Luis", "1990-02-02")
cliente_1=Cliente(nombre= "Javier", fecha = "1997-02-02", monto=10000)
cliente_3edad=Cliente(nombre =" Tatita Javier", fecha = "1920-02-02", monto=20000)
lacteo=Lacteos("Leche",990,[40,40,40,40],20)
verdura=Verduras("Zapalo",100,[10,10,10,10],20)
carne=Carnes("Lomo Vetdado", 2000, [200,200,200,200],"Kanguro")
otro=Otros(nombre="pantalon-queso" , precio=12 , info=["XL","F"])
camisa=Vestuario("Camisa",19990,["L.txt", "M"])
panti=Vestuario("Panti",7990,["L.txt", "F"])
polero=Vestuario("Poleron",9990,["XL", "M"])

print(pep_marino)

