class Cofre:

    def __init__(self,tesoro):
        self.__tesoro = tesoro

    def __metodo_secreto(self):
        return "Nadie me abrira"

    def decir_secreto(self):
        return self.__metodo_secreto()

cofre = Cofre("Dolares")
#print(cofre.__tesoro)

print(cofre.decir_secreto())


class Jugador :

    def __init__(self,vida):
        self.vida = vida

    @property
    def vida(self):
        return self.vida

    @vida.setter
    def vida(self,value):
