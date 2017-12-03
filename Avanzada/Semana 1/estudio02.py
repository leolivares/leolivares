class Automotora :

    def __init__(self,nombre):
        self.nombre = nombre
        self.sucursales = []

    def agregarSucursal(self,sucursal):
        self.sucursales += [sucursal]

    def resultados(self,autos):
        for auto in autos :
            print("ID = {}  Marca = {}  Precio = {}".format(auto.id,auto.marca,auto.precio))

    def sortear_anio(self,min,max):
        autos = []
        for sucursal in self.sucursales :
            for auto in sucursal.nuevos :
                if auto.anio >= min and auto.anio <= max :
                    autos +=[auto]
            for auto in sucursal.usados :
                if auto.anio >= min and auto.anio <= max :
                    autos +=[auto]
        self.resultados(autos)




class Sucursal :

    def __init__(self,nombre):
        self.nombre = nombre
        self.nuevos = []
        self.usados =[]

    def agregarAuto(self,auto):
        if auto.estado == "Nuevo" :
            self.nuevos += [auto]
        else :
            self.usados += [auto]

    @property
    def nuevoprecio(self):
        return (self.precio)

    @nuevoprecio.setter
    def nuevoprecio(self,lista):
        if lista[1] % 500000 == 0 :
            for auto in self.nuevos:
                if lista[0] == auto.id :
                    auto.precio = lista[1]
                    print("El nuevo precio del auto {} es {}".format(auto.id, auto.precio))

        if lista[1] % 500000 == 0 :
            for auto in self.usados:
                if lista[0] == auto.id :
                    auto.precio = lista[1]
                    print("El nuevo precio del auto {} es {}".format(auto.id,auto.precio))
        else :
            print("El precio ingresado no es valido")

    def cantidad_autos(self):
        cant = 0
        for auto in self.nuevos :
            cant += 1
        for auto in self.usados :
            cant += 1
        return cant



class Auto :

    def __init__(self,id,marca,anio,modelo,transmision,precio,estado,dueno = ""):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.transmision = transmision
        self.precio = precio
        self.estado = estado
        self.anio = anio
        self.dueno = dueno
        if self.estado == "Usado":
            self.dueno = dueno

class Dueno :

    def __init__(self,nombre,rut,telefono,correo):
        self.nombre = nombre
        self.rut = rut
        self.telefono = telefono
        self.correo = correo

class Menu :
    def __init__(self):
        self.automotoras = []

    def agregarAutomotora(self,automotora):
        self.automotoras += [automotora]

    def usuario(self):
        print("Bienvenido a automotoras " + automotora.nombre + " \n" + "Elige una opcion")
        print("1.Empleado")
        print("2.Cliente")
        accion = int(input("Seleccion: "))
        return accion

    def eleccion_empleado(self):
        print("1.Cambiar Precio")
        print("2.Autos a la Venta")
        accion = int(input("Seleccion: "))
        return accion






auto1 = Auto(1234,"Hyundai",2016,"Veloster","AT",16000000,"Usado","Leonardo")
automotora = Automotora("lEO")
print(auto1.precio)
auto1.precio = 1212
print(auto1.precio)
auto1.precio = 500000
print(auto1.precio)
print(auto1.dueno)
menu = Menu()
menu.agregarAutomotora(automotora)
print(menu)

suc1 = Sucursal("suucursal")
suc1.agregarAuto(auto1)
print(suc1.usados)
suc1.nuevoprecio = [1234,2000000]
print(suc1.usados[0].precio)
automotora.agregarSucursal(suc1)
print(automotora.sucursales)
automotora.sortear_anio(2000,3000)

