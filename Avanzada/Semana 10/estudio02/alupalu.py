import ast
import threading


class Matriz:

    def __init__(self, archivo):
        with open(archivo) as arch:
            self.matriz = [ast.literal_eval(linea.strip()) for linea in arch]

    def __len__(self):
        return len(self.matriz)

    def __getitem__(self, item):
        return self.matriz[item]


class Generador(threading.Thread):

    def __init__(self, a, b):
        super().__init__()
        self.matriz_a = [[5, -2, 3], [-5, 5, 2], [2, -3, 5]]
        self.matriz_b = [[5, -3, 2], [-2, 3, 5], [4, 3, 1]]

        self.respuesta = []

        self.start()

    def run(self):
        i = 0
        j = 0

        while i < len(self.matriz_a):

            nueva_fila = []

            while j < len(self.matriz_a):

                fila = self.matriz_a[i]
                columna = list(map(lambda x: x[j], self.matriz_b))
                multi = Multiplicacion(fila, columna)
                nueva_fila.append(multi.resultado)

                j += 1

            self.respuesta.append(nueva_fila)

            i += 1
            j = 0

        print(self.respuesta)


class Multiplicacion(threading.Thread):

    def __init__(self, a, b):
        super().__init__()
        self.fila = a
        self.columna = b
        self.resultado = None

        self.start()

    def run(self):
        while self.resultado is None:
            self.resultado = sum(map(lambda x: x[0] * x[1],
                                zip(self.fila, self.columna)))


if __name__ == "__main__":
    matriz_a = Matriz("L.txt")
    matriz_b = Matriz("Pinv.txt")
    generador = Generador(matriz_a, matriz_b)

