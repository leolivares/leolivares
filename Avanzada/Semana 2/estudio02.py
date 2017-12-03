from abc import ABCMeta, abstractmethod

class Asosiacion :

    def __init__(self):
        self.animales = []

    def agregar_animal(self,animal):
        self.animales += [animal]

    def estadisticas(self) :
        min_sueno = 400000000
        min_ind = 400000000
        max_grup = 0
        suma_comid = 0
        sum_regal = 0

        for animal in self.animales :

            if animal.sueno < min_sueno :
                min_sueno = animal.sueno

            if animal.j_ind < min_ind :
                min_ind = animal.j_ind

            if animal.j_grup > max_grup :
                max_grup = animal.j_grup

            print(animal.comidas)
            suma_comid += animal.comidas

            sum_regal += animal.regaloneo

        print(min_sueno,min_ind,max_grup,suma_comid,sum_regal)



class Animal(metaclass=ABCMeta) :


    def __init__(self,expresion,nombre,color,sexo,**kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.color = color
        self.sexo = sexo
        self.expresion = expresion



    def __str__(self):
        return "Me llamo {}, soy {} y tengo el pelo {}".format(self.nombre,self.sexo,self.color)

class Perro(Animal,metaclass=ABCMeta) :

    @abstractmethod
    def __init__(self,expresion,nombre,color,sexo,**kwargs):
        super().__init__(expresion,nombre,color,sexo,**kwargs)

    def comer(self):
        print("Mami :) Quiero comer!!")

    def accion(self):
        print("Tirame la pelota")

    def hablar(self):
        print("Guau Guau")

    def jugar(self):
        print("Tirame la pelota")


class Gato(Animal) :

    def __init__(self,expresion,nombre,color,sexo):
        super().__init__(expresion,nombre,color,sexo)

    def comer(self):
        print("El pellet es horrible. Dame atun")

    def accion(self):
        print("Humano,ahora,juguemos")

    def hablar(self):
        print("Miau Miau")

    def jugar(self):
        print("Humano,ahora,juguemos")


class Personalidad(metaclass=ABCMeta) :

    @abstractmethod
    def __init__(self,sueno,j_ind,j_grup,comidas,regaloneo,**kwargs):
        super().__init__(**kwargs)
        self.sueno = sueno
        self.j_ind = j_ind
        self.j_grup = j_grup
        self.comidas = comidas
        self.regaloneo = regaloneo

class Jugueton(Personalidad,metaclass=ABCMeta) :

    def __init__(self,**kwargs):
        super().__init__(8,1,7,4,4,**kwargs)

    @abstractmethod
    def jugar(self):
        print("Quiero jugar")
        self.jugar()
        print("w")
        self.hablar()
        print("w")

    @abstractmethod
    def comer(self):
        print("Quiero comida")


class Egoista(Personalidad) :

    def __init__(self,**kwargs):
        super().__init__(12,5,1,4,2,**kwargs)

    @abstractmethod
    def comer(self):
        print("Quiero comida")
        self.comida()
        self.hablar()


class GoldenPUC(Perro,Jugueton) :

    def __init__(self,expresion,nombre,color,sexo):
        super().__init__(expresion,nombre,color,sexo)
        if self.sexo == "Macho" :
            self.expresion = self.expresion * 1.1
        elif self.sexo == "Hembra" :
            self.expresion = self.expresion * 0.9
        self.sueno = self.sueno * self.expresion
        self.j_ind = self.j_ind * self.expresion
        self.j_grup = self.j_grup * self.expresion
        self.regaloneo = self.regaloneo * self.expresion
        self.comidas = self.comidas * self.regaloneo



class PUCTerrier(Perro,Egoista) :

    def __init__(self,expresion,nombre,color,sexo):
        super().__init__(expresion,nombre,color,sexo)
        if self.sexo == "Macho" :
            self.expresion = self.expresion * 1.2
        elif self.sexo == "Hembra" :
            self.expresion = self.expresion * 1
        self.sueno = self.sueno * self.expresion
        self.j_ind = self.j_ind * self.expresion
        self.j_grup = self.j_grup * self.expresion
        self.regaloneo = self.regaloneo * self.expresion
        self.comidas = self.comidas * self.regaloneo


class SiamePUC(Gato,Egoista) :

    def __init__(self,expresion,nombre,color,sexo):
        super().__init__(expresion,nombre,color,sexo)
        if self.sexo == "Macho" :
            self.expresion = self.expresion * 1
        elif self.sexo == "Hembra" :
            self.expresion = self.expresion * 1.5
        self.sueno = self.sueno * self.expresion
        self.j_ind = self.j_ind * self.expresion
        self.j_grup = self.j_grup * self.expresion
        self.regaloneo = self.regaloneo * self.expresion
        self.comidas = self.comidas * self.regaloneo

if __name__ == '__main__':
    animals = list()
    animals.append(GoldenPUC(expresion=0.5, nombre="Mara", color="Blanco", sexo="Hembra"))
    animals.append(GoldenPUC(expresion=0.9, nombre="Eddie", color="Rubio", sexo="Macho"))
    animals.append(SiamePUC(expresion=0.9, nombre="Felix", color="Naranjo", sexo="Hembra"))
    animals.append(PUCTerrier(expresion=0.8, nombre="Betty", color="Café", sexo="Hembra"))
    aso = Asosiacion()

    for a in animals:
        aso.agregar_animal(a)
        print(a)
        a.jugar()
        a.comer()

    aso.estadisticas()

