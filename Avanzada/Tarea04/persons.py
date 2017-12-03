from random import randint, expovariate, random, triangular, normalvariate
from collections import deque

class Persona:

    def __init__(self, nombre, apellido, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

    def __eq__(self, other):
        return True

class Alumno(Persona):

    def __init__(self, base_mesada, limite, preferencia, traslado,
                 moda, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_mesada = float(base_mesada)
        self.limite = [int(x) for x in limite.split(";")]
        self.preferencias = [x.strip() for x in preferencia.split("-")]
        self.llegada = float(moda)
        self.tasa_traslado = float(traslado)
        self.dinero = 0
        self._limite_paciencia = 0
        self.en_campus = False
        self.horario_almuerzo = None
        self.decidio = False
        self.almorzo = False
        self.traslado = False
        self.siendo_atendido = False


    @property
    def limite_paciencia(self):
        return self._limite_paciencia

    @limite_paciencia.setter
    def limite_paciencia(self, value):
        if self._limite_paciencia - value < 0:
            self._limite_paciencia = 0
        else:
            self._limite_paciencia -= value

    @property
    def calcular_mesada(self):
        self.mesada = self.base_mesada * (1 + (random()) ** random()) * 20

    @property
    def calcular_paciencia(self):
        self._limite_paciencia = randint(self.limite[0], self.limite[1])

    @property
    def tiempo_llegada(self):
        return triangular(0, 240, self.llegada)

    @property
    def tiempo_decision(self):
        return normalvariate(0, 10)


class Funcionario(Persona):

    def __init__(self, dinero, moda, preferencias, traslado, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dinero = float(dinero)
        self.base_dinero = float(dinero)
        self.llegada = float(moda)
        self.preferencias = [x.strip() for x in preferencias.split("-")]
        self.tasa_traslado = float(traslado)
        self.en_campus = False
        self.limite_paciencia = float("Inf")
        self.horario_almuerzo = None
        self.almorzo = False
        self.decidio = False
        self.traslado = False
        self.siendo_atendido = False

    @property
    def tiempo_llegada(self):
        return triangular(0, 240, self.llegada)

    @property
    def tiempo_decision(self):
        return normalvariate(0, 10)


class Vendedor(Persona):

    def __init__(self, tipo, velocidades, stock, permiso, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo_comida = tipo.strip()
        self.velocidad = randint(int(velocidades[0]), int(velocidades[1]))
        self.stock = [int(x) for x in stock.split(";")]
        self.permiso = True if random() <= float(permiso) else False
        self.precios = list()
        self.cola = deque()
        self.productos = list()
        self.cantidad_sin_stock = 0
        self.cant_todo_stock = 0
        self.dias_sin_vender = 0
        self.t_atencion = 0
        self.asustados = 0
        self.aumento_concha = 0
        self.bancarrota = False
        self.instalado = False
        self.atendiendo = None
        self.revisado = False

    @property
    def calcular_stock(self):
        return randint(self.stock[0], self.stock[1])

    @property
    def hora_instalacion(self):
        return normalvariate(0, 30)


class Carabinero(Persona):

    def __init__(self, personalidad, tasa, probabilidad, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.personalidad = personalidad
        self.prob_engano = float(probabilidad)
        self.tasa_productos = float(tasa)
        self.revisando_a = None


class QuickDevil:

    def __init__(self):
        self.utilidades = 0
        self.tasa_llamada = None

    @property
    def calcular_llamada(self):
        return (round(expovariate(self.tasa_llamada)) * 1440) + 1






