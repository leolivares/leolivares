import datetime as dt
from abc import ABCMeta,abstractmethod
from decimal import Decimal

class Usuario(metaclass=ABCMeta) :

    def __init__(self,usuario,nombre,apellido,fecha,orders_id,balance,merc_regis) :
        self.usuario = usuario
        self.nombre = nombre
        self.apellido = apellido
        self.fecha = fecha
        self.orders_id = orders_id
        self.balance = balance
        self.mercados_registrados = merc_regis

    #Esta es distinta para cada tipo de cliente
    @abstractmethod
    def informacion_entrada(self,app):
        pass

    #Se encarga de calcular si el cliente tiene los recursos financieros
    #para ingresar un order
    def revisar_balance(self,currencies,monto,simbolo):
        aceptado = True
        i = 0
        for curr in currencies :
            if curr.lower() == simbolo.lower() :
                num = i
            i += 1
        if self.balance[num] < monto :
            aceptado = False
        return aceptado

    #Realiza el cambio de Trader a Investor
    def upgrade_investor(self):
        if float(self.balance[-1]) >= 300000 :
            self.balance[-1] -= 300000
            usuario = self.usuario
            nombre = self.nombre
            apellido = self.apellido
            fecha = self.fecha
            orders_id = self.orders_id[:]
            balance = self.balance[:]
            merc_regis = self.mercados_registrados
            cliente = Investor(usuario,nombre,apellido,fecha,orders_id,balance,merc_regis)
            return cliente


        else :
            print("   ")
            print("No tienes suficientes monedas DCC para realizar el upgrade a Investor")
            print("   ")


    #Realiza una transferencia de monedas, de un usuario a otro
    def transferencia(self,cliente,currencies):
        comision = Decimal("0.95")
        simbol = input("Ingresa el simbolo de la moneda que deseas transferir: ")
        i = 0
        num = None
        for curr in currencies :
            if curr.lower() == simbol.lower() :
                num = i
            i += 1

        if not num :
            print("  ")
            print("Lo sentimos, pero la moneda {} no existe.".format(simbol))
            print("   ")

        elif self.balance[num] > 0 :
            cantidad = Decimal(input("Ingresa la cantidad de monedas que deseas transferir: "))
            if cantidad > 0 :
                if cantidad <= self.balance[num] :
                    self.balance[num] -= cantidad
                    cliente.balance[num] += cantidad * comision
                    print("  ")
                    print("La transaccion se ha realizado exitosamente!")
                    print("El usuario {} ha recibido {} {}".format(cliente.usuario,cantidad,simbol))
                    print("   ")

                else :
                    print("  ")
                    print("Lo sentimos, pero solo tienes {} {} para transferir.".format(self.balance[num],simbol))
                    print("   ")

            else :
                print("  ")
                print("Lo sentimos, pero es imposible transferir esta cantidad.")
                print("   ")

        else :
            print("  ")
            print("Lo sentimos, pero no tienes monedas {}.".format(simbol))
            print("   ")

    #Muestra el saldo de un cliente
    def consultar_saldo(self,currencies):
        print("   ")
        print("Tu saldo disponible es el siguiente: ")
        i = 0
        for balance in self.balance :
            print("{}: {}".format(currencies[i],balance))
            i += 1



class Underaged(Usuario) :

    def __init__(self,usuario,nombre,apellido,fecha,orders_id,balance=None,merc_regis=list()):
        super().__init__(usuario,nombre,apellido,fecha,orders_id,balance,merc_regis)
        self.tipo = "Underaged"
        self.permisos = False

    def informacion_entrada(self,app):
        curr = app.obtener_currencies()

        print("   ")
        print("Por ser un usuario Underaged no puedes tener orders activas" "\n"
              "Tu balance es el siguiente: ")
        i = 0
        for balance in self.balance :
            print("   {}: {}".format(curr[i],balance))
            i += 1
        print("   ")



class Trader(Usuario) :

    def __init__(self,usuario,nombre,apellido,fecha,orders_id,balance,merc_regis):
        super().__init__(usuario,nombre,apellido,fecha,orders_id,balance,merc_regis)
        self.tipo = "Trader"
        self.limites = 15
        self.max_activos = 5
        self.permisos = True

    def informacion_entrada(self,app):
        curr = app.obtener_currencies()

        print("   ")
        print("Por ser un usuario Underaged no puedes tener orders activas" "\n"
              "Tu balance es el siguiente: ")
        i = 0
        for balance in self.balance :
            print("   {}: {}".format(curr[i],balance))
            i += 1
        print("   ")


class Investor(Usuario) :

    def __init__(self,usuario,nombre,apellido,fecha,orders_id,balance,merc_regis):
        super().__init__(usuario,nombre,apellido,fecha,orders_id,balance,merc_regis)
        self.tipo = "Investor"
        self.permisos = True

    def informacion_entrada(self,app):
        curr = app.obtener_currencies()
        print("   ")
        print("Eres un usuario de tipo Investor" "\n"
              "Tu balance es el siguiente:")
        i = 0
        for balance in self.balance :
            print("   {}: {}".format(curr[i],balance))
            i += 1
        print("   ")

