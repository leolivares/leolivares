import semester
import variables as var
from collections import defaultdict

class AnalisisEscenario:

    def __init__(self, repeticiones, medida):
        self.escenarios = []
        self.labels = []
        self.repeticiones = repeticiones
        self.medida = medida
        self.medidas = {1: "Promedio Dinero Confiscado",
                        2: "Cantidad Minima",
                        3: "Cantidad Maxima",
                        4: "Cantidad Promedio",
                        5: "Cantidad de confiscaciones por Dr. Jekyll",
                        6: "Cantidad de confiscaciones por Mr. Hyde",
                        7: "Numero de llamadas",
                        8: "Numero de Concha Estereo",
                        9: "Numero de Temperaturas Extremas",
                        10: "Cantidad de Luvias de Hamburguesas",
                        11: "Promedio de almuerzos de 12:00-12:59",
                        12: "Promedio de almuerzos de 13:00-13:59",
                        13: "Promedio de almuerzos de 14:00-15:00",
                        14: "Cantidad de alumnos sin almorzar",
                        15: "Calidad promedio de productos",
                        16: "Cantidad de miembros intoxicados",
                        17: "Cantidad de productos descompuestos",
                        18: "Promedio de abandonos de cola por dia",
                        19: "Cantidad promedio de vendedores sin stock",
                        20: "Cantidad de engaños a Dr. Jekyll",
                        21: "Cantidad de engaños a Mr. Hyde"}

        self.obtener_escenarios()

    def obtener_escenarios(self):
        """
        Guarda en una lista, los escenarios que se simularan
        """
        with open("escenarios.csv", "r") as archivo:
            self.escenarios = [linea.strip().split(",") for linea in archivo]
            self.labels = self.escenarios.pop(0)

        escenarios = []
        for escenario in self.escenarios:
            esc = {k: v for k, v in zip(self.labels, escenario)}
            escenarios.append(esc)
        self.escenarios = escenarios

    def comparar_escenarios(self):
        """
        Procede a correr la cantidad necesaria de simulaciones por escenario.
        Para esto se va modificando el archivo "parametros_iniciales.csv" y se
        corre la simulacion del archivo "semester.py".
        """

        i = 0
        resultados_globales = list()

        for escenario in self.escenarios:
            print("Analisis de Escenario {}".format(i))
            labels = []
            parametros = []
            resultados_escenario = defaultdict(int)

            with open("parametros_iniciales.csv", "w") as archivo:
                for parametro in escenario:
                    if parametro != "escenario":
                        labels.append(parametro)
                        parametros.append(escenario[parametro])

                print(",".join(labels), file=archivo)
                print(",".join(parametros), file=archivo)


            for _ in range(self.repeticiones):
                print("     Realizando simulacion #{}".format(_+1))

                simulacion = semester.Semestre()
                simulacion.obtener_parametros()
                simulacion.obtener_personas()
                simulacion.obtener_productos()

                resultados = simulacion.run(printear=False)

                for result in resultados:

                    resultados_escenario[result] += resultados[result]

            resultados_globales.append(resultados_escenario)
            print("   ")

            i += 1

        self.imprimir_resultados(resultados_globales)


    def top3(self, globales, medida):
        """
        A partir de los resultados de todas la simulaciones, selecciona los
        tres mas altos segun una medida de desempeño. Si la medida es None,
        determina el top 3 para todas las medidas.
        """
        resultados = list()
        i = 0
        for escenario in globales:
            resultados.append((i, escenario[medida]))
            i += 1
        resultados.sort(key=lambda x: x[1],reverse=True)
        top_3 = resultados
        if len(resultados) > 3:
            top_3 = resultados[:3]

        puestos = ["Primer", "Segundo", "Tercer"]
        for puesto, top in zip(puestos, top_3):
            print("     {} Lugar: Escenario #{}  Resultado: {}"
                  .format(puesto, top[0], top[1]))
        print("   ")

    def imprimir_resultados(self, globales):
        """
        Imprime los resultados de las comparaciones en consola.
        """
        if not self.medida:
            for medida in self.medidas:
                print("Top 3 escenarios para {}".format(self.medidas[medida]))
                self.top3(globales, medida)

        else:
            print("Top 3 escenarios para {}".format(self.medidas[self.medida]))
            self.top3(globales, self.medida)


if __name__ == '__main__':
    analisis = AnalisisEscenario(var.CANT_REPETICIONES, var.MEDIDA)
    analisis.comparar_escenarios()
