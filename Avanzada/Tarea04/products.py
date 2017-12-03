from math import exp

class Producto:

    def __init__(self, nombre, tipo, precio, calorias, tasa):
        self.nombre = nombre
        self.tipo = tipo
        self.tasa_putrefaccion = float(tasa)
        self.precio = float(precio)
        self.calorias = float(calorias)

    def calcular_putrefaccion(self, tiempo, temp):
        if temp == "Calor":
            putre = (1 - (exp((tiempo * (-1)) / self.tasa_putrefaccion))) * 2
            if putre > 1:
                putre = 1
            return putre
        return 1 - (exp((tiempo * (-1)) / self.tasa_putrefaccion))

    def calcular_calidad(self, putre, temp, precio=None):
        if not precio:
            precio = self.precio
        if temp == "Frio":
            calidad = ((self.calorias * ((1 - putre) ** 4)) / ((precio) ** (4/5))) / 2
            return calidad
        return ((self.calorias * ((1 - putre) ** 4)) / ((precio) ** (4/5)))