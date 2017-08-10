import random

class Mezclador:
    def __init__ (self):
        self.lista_palabras = []
        self.palabras_validas = []
        self.palabras_entregadas = []
        self.palabras_usuario = []
        self.leer_palabras()

    def reordenar_letras(self,palabra):
        lista_nueva = list(palabra)
        random.shuffle(lista_nueva)
        return ''.join(lista_nueva)

    def es_palabra_valida(self,palabra):
        return palabra in self.palabras_validas

    def leer_palabras(self):
        f = open('palabras.txt',encoding="utf-8")
        for linea in f:
            self.lista_palabras.append(linea.strip())

        f.close()

        random.shuffle(self.lista_palabras)

        f2 = open('palabras_validas.txt',encoding="utf-8")
        for linea in f2:
            self.palabras_validas.append(linea.strip("\n"))

        f2.close()

    def get_palabra(self,n):
        for p in self.lista_palabras:
            if len(p) == n and not(p in self.palabras_entregadas):
                self.palabras_entregadas.append(p)
                return p

        return ""

    def limpiar_lista(self):
        self.palabras_usuario = []

    def palabra_usada(self,p):
        return p in self.palabras_usuario

    def agregar_palabra_usada(self,p):
        self.palabras_usuario.append(p)
        

    


mezclador = Mezclador()

def existe_palabra(palabra):
    return mezclador.es_palabra_valida(palabra)

def obtener_palabra(cant_letras):
    return mezclador.get_palabra(cant_letras)

def limpiar_lista():
    mezclador.limpiar_lista()

def palabra_usada(palabra):
    return mezclador.palabra_usada(palabra)

def agregar_palabra(palabra):
    mezclador.agregar_palabra_usada(palabra)

def reordenar_palabra(palabra):
    return mezclador.reordenar_letras(palabra)
