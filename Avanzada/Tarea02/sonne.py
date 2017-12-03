import grafo
import lista as ls
import interfaz
import gui
import sys
import random
from random import choice

class Prograsonne() :

    def __init__(self,turno=None):
        self.graph = grafo.Grafo()
        self.historial = ls.Lista()
        self._turno = turno
        self.piezas = ls.Lista()
        self.pieza_actual = None
        self.interfaz = interfaz.MyInterface()

    def obtener_piezas(self):
        archivo = open("pieces.csv", "r")
        lineas = archivo.readlines()
        archivo.close()
        listas_legales = ls.Lista()
        for linea in lineas:
            linea = linea.strip().split(",")
            lista_legal = ls.Lista()
            for dato in linea:
                lista_legal.append(dato)
            listas_legales.append(lista_legal)

        for lista_legal in listas_legales:
            nodo = lista_legal.valor[1]
            cant = int(nodo.valor)
            nodo2 = lista_legal.valor[0]
            tipo = nodo2.valor
            while cant > 0:
                pieza = grafo.Pieza(tipo)
                self.piezas.append(pieza)
                cant -= 1

    def run(self):
        def hook(type, value, traceback):
            print(type)
            print(value)
            print(traceback)

        sys.__excepthook__ = hook

        gui.set_scale(False)  # Any float different from 0
        gui.init()
        gui.set_quality("ultra")  # low, medium, high ultra
        gui.set_animations(False)
        gui.set_game_interface(self.interfaz)  # GUI Listener
        gui.init_grid()
        self.situacion_inicial()
        gui.run()

    def elegir_pieza(self):
        num = len(self.piezas) - 1
        n = random.randint(0, num)
        pieza = self.piezas[n].valor
        return pieza

    def coordenadas_random(self):
        i = random.randint(0,7)
        j = random.randint(0,7)
        color = ls.Lista()
        color.append("red")
        color.append("blue")
        c = random.randint(0,1)
        col = color[c].valor
        self.turno = col
        return i , j , col

    def cambiar_turno(self):
        print(len(self.piezas))
        if self.turno == "red" :
            self.turno = "blue"
        else :
            self.turno = "red"

    def situacion_inicial(self):
        self.obtener_piezas()
        pieza = self.elegir_pieza()
        self.pieza_actual = pieza
        i, j, col = self.coordenadas_random()
        print(pieza.tipo, col)
        gui.add_piece(i, j)
        gui.nueva_pieza(col, pieza.tipo)
        self.interfaz.colocar_pieza(i, j)
        pieza.i = i
        pieza.j = j
        self.historial.append(pieza)
        self.graph.agregar_pieza(pieza)
        self.cambiar_turno()




progra = Prograsonne()
progra.run()