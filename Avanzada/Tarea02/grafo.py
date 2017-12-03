import lista as ls

class Pieza :

    id = 1

    def __init__(self,tipo,i=None,j=None,color=None):
        self.id = Pieza.id
        self.tipo = tipo
        self.tipo_permanente = tipo
        self.i = i
        self.j = j
        self.color = color
        self.pertenece_a : None
        self.conexiones = ls.Lista()
        Pieza.id += 1

    def buscar_pieza(self,i,j):
        if self.i == i and self.j == j :
            return self
        else :

            if len(self.conexiones) != 0 :
                for p in self.conexiones :
                    pieza = p.valor.buscar_pieza(i,j)
                    if pieza :
                        return pieza
                return None
            else :
                return None


class Grafo :

    def __init__(self,valor=None):
        self.raiz = valor
        self.historial = ls.Lista()

    def buscar_pieza(self,i,j):
        pieza_encontrada = None
        if self.raiz.i == i and self.raiz.j == j :
            pieza_encontrada = self.raiz
            return pieza_encontrada
        else :

            if len(self.raiz.conexiones) != 0 :
                for p in self.raiz.conexiones :
                    pieza_encontrada = p.valor.buscar_pieza(i,j)

                    if pieza_encontrada :
                        return pieza_encontrada

        if not pieza_encontrada :
            return None

    def agregar_pieza(self,pieza,padre=None):

        if not self.raiz :
            self.raiz = pieza

        if padre :
            padre.conexiones.append(pieza)
