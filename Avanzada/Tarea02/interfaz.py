import gui
from random import choice
import grafo
import lista as ls
import sonne as progra

def get_next_number():
    num = 1
    while True:
        yield num
        num += 1


a = get_next_number()
print(a)


class MyInterface(gui.GameInterface):
    def __init__(self):
        self.graph = grafo.Grafo()
        self.historial = ls.Lista()
        self.pieza_actual = None
        self.progra = progra.Prograsonne

    def verificar_jugada(self,i,j):

        permitido = False
        if not self.graph.raiz :
            permitido = True
            self.graph.agregar_pieza()

        else :
            pass

        return permitido

    def colocar_pieza(self, i, j):
        print("Presionaste", (i, j))
        print(self.graph.raiz)
        permitido = self.verificar_jugada(i,j)
        if permitido :
            gui.add_piece(i, j)
            gui.nueva_pieza() #Ojo con esto si no utilizan una nueva pieza obtendran un error
        else :
            gui.add_piece(i, j)

    def rotar_pieza(self, orientation):
        print(orientation)

    def retroceder(self):
        print("Presionaste retroceder")

    def terminar_juego(self):
        print("Presionaste terminar juego")

    def hint_asked(self):
        print("Me pediste una pista y no te la dare :P")

    def click_number(self, number):
        print(number)

    def guardar_juego(self):
        gui.add_number(next(a), choice(["red", "blue"]))
        print("Presionaron guardar")