from abc import ABCMeta, abstractmethod
import random


class DT :

    def __init__(self,equipo):
        self.equipo = equipo

    def alentar(self) :
        for atleta in self.equipo.atletas :
            atleta.energia += 3

class Equipo :

    def __init__(self,tipo):
        self.director = DT(self)
        self.tipo = tipo
        self.atletas = []

    def agregar_atleta(self,atleta):

        if isinstance(atleta,self.tipo) :
            self.atletas += [atleta]
        else :
            print("No es apto para el equipo")

    def __add__(self,other):
        if self.tipo == other.tipo :
            nuevo_equipo = Equipo(self.tipo)
            nuevo_equipo.atletas = self.atletas + other.atletas
            return nuevo_equipo
        else :
            print("No se suman equipos de distinto tipo")
            return None


class Atleta(metaclass=ABCMeta) :

    def __init__(self,nombre,energia,velocidad):
        self.nombre = nombre
        self._energia = energia
        self.velocidad = velocidad
        self.registro = [1,2,3,4]

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self,value):
        if value <= 0 :
            self._energia = 0
        elif value >= 100 :
            self._energia = value
        else :
            self._energia = value

    def descansar(self):
        self.energia += 1


    def __eq__(self, other):
        if type(self) == type(other) :
            igual = min(self.registro) == min(other.registro)
        else :
            print("No se pueden comparar")
            return None
        return igual

    @abstractmethod
    def entrenar(self):
        pass

    @abstractmethod
    def competir(self):
        pass



class Ciclista(Atleta,metaclass=ABCMeta) :

    def __init__(self,nombre,energia,velocidad):
        super().__init__(nombre,energia,velocidad)

    def entrenar(self):
        if self.energia == 0 :
            print("Nivel de energia no es suficiente")
        else :
            self.energia -= 1
            self.velocidad += 1


class Nadador(Atleta):

    def __init__(self, nombre, energia, velocidad):
        super().__init__(nombre, energia, velocidad)

    def entrenar(self):
        if self.energia == 0 :
            print("Nivel de energia no es suficiente")
        else :
            self.energia -= 1
            self.velocidad += 2

    def competir(self):
        tiempo = random.gauss(1000/self.velocidad,1)
        print("El nadador {} esta nadando".format(self.nombre))
        self.registro += [tiempo]
        self.energia -= 1


class Corredor(Atleta):

    def __init__(self, nombre, energia, velocidad):
        super().__init__(nombre, energia, velocidad)

    def entrenar(self):
        if self.energia == 0 :
            print("Nivel de energia no es suficiente")
        else :
            self.energia -= 1
            self.velocidad += 3

    def competir(self):
        tiempo = random.gauss(1000/self.velocidad,1)
        print("El corredor {} esta corriendo".format(self.nombre))
        self.registro += [tiempo]
        self.energia -= 1


class Montana(Ciclista) :

    def __init__(self,nombre,energia,velocidad):
        super().__init__(nombre,energia,velocidad)

    def competir(self):
        tiempo = random.gauss(1000/self.velocidad,1)
        print("El ciclista {} esta pedaleando una Mountain Bike".format(self.nombre))
        self.registro += [tiempo]
        self.energia -= 1


class Pista(Ciclista) :

    def __init__(self,nombre,energia,velocidad):
        super().__init__(nombre,energia,velocidad)

    def competir(self):
        tiempo = random.gauss(1000/self.velocidad,1)
        print("El ciclista {} esta pedaleando por la pista".format(self.nombre))
        self.registro += [tiempo]
        self.energia -= 1


class Triatleta(Corredor,Nadador,Pista) :

    def __init__(self,nombre,energia,velocidad):
        super().__init__(nombre,energia,velocidad)
        self.registro_corredor = []
        self.registro_nadador = []
        self.registro_pista = []

    def competir(self):
        tiempo = random.gauss(1000/self.velocidad,1)
        print("El triatleta {} esta compitiendo en una triatlon".format(self.nombre))
        self.registro += [tiempo]
        self.energia -= 3


tri= Triatleta("leo",1,2)
equi = Equipo(Triatleta)
nada1 = Nadador("leo", 3, 4)

print(tri.nombre)
print(tri.energia)
tri.descansar()
print(tri.energia)


equi.agregar_atleta(tri)
print(equi.atletas)
print(type(equi))
print(type(tri))
print(type(nada1))
print(type(nada1) == type(tri))



nada1.competir()
print(nada1.energia)
nada1.competir()
print(nada1.energia)
nada1.competir()
print(nada1.energia)
nada1.competir()
print(nada1.energia)
nada1.competir()
print(nada1.energia)
print(nada1.velocidad)
