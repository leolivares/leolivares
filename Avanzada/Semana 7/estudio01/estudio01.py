import random
from datetime import datetime


"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""


def verificar_transferencia(funcion):
    def transferir(self, origen, destino, monto, clave):
        if origen not in self.cuentas:
            raise AssertionError("La cuenta {} no existe".format(origen))
        elif destino not in self.cuentas:
            raise AssertionError("La cuenta {} no existe".format(destino))
        elif self.cuentas[origen].saldo < monto:
            raise AssertionError("El saldo de la cuenta {} no es suficiente".format(origen))
        elif clave != self.cuentas[origen].clave:
            raise AssertionError("La clave es incorrecta")
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto
    return transferir


def verificar_cuenta(funcion):
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        cant = rut.count("-")
        guion = [x for x in rut if x != "-"]
        digitos = list(filter(lambda x: x.isdigit(), rut))
        if numero in self.cuentas:
            raise AssertionError("Esta cuenta ya existe")
        elif len(clave) != 4:
            raise AssertionError("La clave debe ser de 4 digitos")
        elif not clave.isdigit():
            raise AssertionError("La clave solo puede tener digitos")
        elif cant != 1:
            raise AssertionError("El rut solo puede tener un guion")
        elif len(guion) != len(digitos):
            raise AssertionError("El rut solo puede tener digitos y guiones")
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta
    return crear_cuenta


def verificar_inversion(funcion):
    def invertir(self, cuenta, monto, clave):
        if cuenta not in self.cuentas:
            raise AssertionError("La cuenta no existe")
        elif self.cuentas[cuenta].saldo < monto:
            raise AssertionError("El saldo no es suficiente")
        elif clave != self.cuentas[cuenta].clave:
            raise AssertionError("La clave no es la correcta")
        elif (self.cuentas[cuenta].inversiones + monto) > 10000000:
            raise AssertionError("Con esta inversion se excede el limite de 10.000.000")
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto
    return invertir


def verificar_saldo(funcion):
    def saldo(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            raise AssertionError("La cuenta no existe")
        return self.cuentas[numero_cuenta].saldo
    return saldo


def log(nombre_archivo):
    def guardar_datos(funcion):
        def imprimir(*args,**kwargs):
            tiempo = datetime.now()
            with open(nombre_archivo,"a") as archivo:
                print(tiempo,funcion.__name__,args[1:],kwargs,file=archivo)
        return imprimir
    return guardar_datos


"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""


class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @log("saldo.txt")
    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @log("transferencias.txt")
    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @log("nueva_cuenta.txt")
    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @log("inversiones.txt")
    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    bco.crear_cuenta("Juan", "19231233-3", "1234", bco.crear_numero())

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """
    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    print("..............")

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    print("..............")

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    print("..............")

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    print("..............")

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    print("..............")


    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    print("..............")