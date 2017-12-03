class NodoLista :

    def __init__(self,valor):
        self.valor = valor
        self.siguiente = None


class Lista:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def append(self, item):
        if not self.cabeza:
            self.cabeza = NodoLista(item)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = NodoLista(item)
            self.cola = self.cola.siguiente

    def remove(self,pieza):
        lista = Lista()
        for p in self :
            if p.valor.id != pieza.id :
                lista.append(p.valor)
        return lista

    def __iter__(self):
        return Iterador(self.cabeza)

    def __repr__(self):
        msj = ""
        nodo = self.cabeza
        while nodo :
            msj += "{} \n".format(nodo.valor)
            nodo = nodo.siguiente
        return msj.strip()

    def __len__(self):
        cant = 0
        nodo = self.cabeza
        while nodo :
            cant += 1
            nodo = nodo.siguiente
        return cant

    def __getitem__(self, item):
        n = 0
        nodo = self.cabeza
        if item == -1 :
            item = len(self)-1
        while n < item :
            nodo = nodo.siguiente
            n += 1
        return nodo

    def sort(self):
        lista = Lista()
        fila = 0
        while fila <= 7 :
            for p in self :
                if p.valor.i == fila :
                    lista.append(p.valor)
            fila += 1

        lista2 = Lista()
        columna = 0
        while columna <= 7 :
            for p in lista :
                if p.valor.j == columna :
                    lista2.append(p.valor)
            columna += 1

        return lista2

    def buscar(self,i,j):
        for pieza in self :
            if pieza.valor.i == i and pieza.valor.j == j :
                return pieza.valor


class Iterador :

    def __init__(self,lista):
        self.iterable = lista

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterable is None:
            raise StopIteration
        else:
            to_return = self.iterable
            self.iterable = self.iterable.siguiente
            return to_return
