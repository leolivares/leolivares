def ordenar_pag(libro):
    return libro[0].pag

class Biblioteca :

    def __init__(self):
        self.estantes = []

    def agregar_estantes(self,estante):
        self.estantes += [estante]

    def imprimir_topicos(self) :
        topicos = []
        for estante in self.estantes :
            if estante.topico not in topicos :
                topicos += [estante.topico]
        for topic in topicos :
            print(topic)


class Estante :

    num = 1

    def __init__(self,max,topico):
        self.id = Estante.num
        self.max = max
        self._topico = topico
        self._libros = []
        Estante.num += 1

    @property
    def topico(self):
        return self._topico

    @topico.setter
    def topico(self,value):
        self._topico = value

    @property
    def libros(self):
        return self._libros

    @libros.setter
    def libros(self,libro):
        cant = 0
        for lib in self.libros :
            cant += lib[1]
        if cant == self.max :
            print("Estante lleno")
        else :
            self.agregar_libros(libro)

    def agregar_libros(self,libro):
        seguir = True
        while seguir :
            for lib in self._libros :
                print(lib)
                if lib[0].titulo == libro.titulo and lib[0].autor == libro.autor :
                    lib[1] += 1
                    seguir = False
                    print("w")
            if seguir :
                self._libros += [[libro,1]]
                seguir = False
                print("o")


    def ordenar_pag(self,libro):
        return libro.pag

    def ordenar(self):
        self.libros = sorted(self.libros, key=ordenar_pag)


class Libro :

    num = 1

    def __init__(self,titulo,pag,topico,autor=None):
        self.id = Libro.num
        self.titulo = titulo
        self.pag = pag
        self.topico = topico
        self.autor = autor



libreria = Biblioteca()
est1 = Estante(3,"Filosofia")
est2 = Estante(40,"Biologia")
est3 = Estante(10,"Biologia")
est4 = Estante(34,"Aleman")
libreria.agregar_estantes(est1)
libreria.agregar_estantes(est2)
libreria.agregar_estantes(est3)
libreria.agregar_estantes(est4)
libreria.imprimir_topicos()
lib1 = Libro("s",12,"wd")
lib2 = Libro("m",43,"wd")
lib3 = Libro("n",1,"wd")
lib4 = Libro("s",23,"wd")

#est1.agregar_libros(lib1)
#est1.agregar_libros(lib2)
#est1.agregar_libros(lib3)
#est1.agregar_libros(lib4)

est1.libros = lib1
est1.libros = lib2

for lib in est1._libros :
    print(lib[0].titulo)




