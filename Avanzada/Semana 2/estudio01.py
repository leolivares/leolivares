__author__ = "cotehidalgov"

# Herencia
# -*- coding: utf-8 -*-

import random
from abc import ABCMeta, abstractmethod


class Plate:
    def __init__(self, food, drink):
        self.food = food
        self.drink = drink


class Food:
    def __init__(self,ingredients,nombre):
        self.ingredients = ingredients
        self.nombre = nombre
        self.calidad = random.randint(50, 200)


    @abstractmethod
    def check_ingredients(self):

        if self.nombre == "Pizza" :
            for ing in self.ingredients :
                if ing == "pepperoni" :
                    self.calidad += 50
                elif ing == "pina" :
                    self.calidad -= 50

        elif self.nombre == "Ensalada" :
            for ing in self.ingredients :
                if ing == "crutones" :
                    self.calidad += 20
                elif ing == "manzana" :
                    self.calidad -= 20

    @abstractmethod
    def check_time(self):
        if self.tiempo >= 30 :
            self.calidad -= 30



class Drink:
    def __init__(self,nombre):
        self.calidad = random.randint(50,150)
        self.nombre = nombre

    @abstractmethod
    def check_cal(self):
        if self.nombre == "Soda" :
            self.calidad -= 30
        elif self.nombre == "Jugo" :
            self.calidad += 30


class Pizza(Food) :
    def __init__(self,ingredients):
        super().__init__(ingredients,"Pizza")
        self.tiempo = random.randint(20,100)


class Salad(Food) :
    def __init__(self,ingredients):
        super().__init__(ingredients,"Ensalada")
        self.tiempo = random.randint(5,60)


class Soda(Drink) :
    def __init__(self):
        super().__init__("Soda")

class Juice(Drink) :
    def __init__(self):
        super().__init__("Jugo")

class Personality:

    @abstractmethod
    def react(self,quality):

        if quality >= 100 :
            self.im_happy()
        else :
            self.im_mad()


class Person:  # Solo los clientes tienen personalidad en esta actividad
    def __init__(self, name):
        self.name = name


class Restaurant:
    def __init__(self, chefs, clients):
        self.chefs = chefs
        self.clients = clients

    def start(self):
        for i in range(3):  # Se hace el estudio por 3 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Chef(Person):

    def __init__(self,nombre):
        super().__init__(nombre)

    def cook(self):
        comida = random.randint(0,1)
        bebestible = random.randint(0,1)
        ingredientes_pizza = ["pepperoni","pina","cebolla","tomate","jamon","pollo"]
        ingredientes_ensal = ["crutones","espinaca","manzana","zanahoria"]

        if comida == 0 :
            a = random.randint(0,5)
            b = random.randint(0, 5)
            c = random.randint(0, 5)
            ingredientes = [ingredientes_pizza[a],ingredientes_pizza[b],ingredientes_pizza[c]]
            plato = Pizza(ingredientes)

        else :
            a = random.randint(0,3)
            b = random.randint(0, 3)
            ingredientes = [ingredientes_ensal[a],ingredientes_ensal[b]]
            plato = Salad(ingredientes)

        if bebestible == 0 :
            bebida = Soda()
        else :
            bebida = Juice()


        plato.check_ingredients()
        plato.check_time()
        bebida.check_cal()

        return Plate(plato,bebida)



class Client(Person):

    def __init__(self,nombre,personalidad):
        super().__init__(nombre)
        self.personalidad = personalidad

    def eat(self,plate):
        comida = plate.food
        bebida = plate.drink

        calidad_f = (comida.calidad + bebida.calidad) / 2
        self.personalidad.react(calidad_f)

class Cool(Personality):

    def im_happy(self):
        print("Yumi! Que rico")

    def im_mad(self):
        print("Preguntare si puedo cambiar el plato")

class Hater(Personality) :

    def im_happy(self):
        print("No esta malo, pero prefiero otro lugar")

    def im_mad(self):
        print("Nunca mas vendre")



if __name__ == '__main__':
    chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]
    clients = [Client("Bastian", Hater()), Client("Flori", Cool()),
               Client("Antonio", Hater()), Client("Felipe", Cool())]

    restaurant = Restaurant(chefs, clients)
    restaurant.start()
