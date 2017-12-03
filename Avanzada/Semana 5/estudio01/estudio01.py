class CustomException(Exception) :

    def __init__(self):
        super().__init__("El indice esta fuera de rango")

class InvertirChunks(Exception) :

    def __init__(self,codigo):
        self.codigo = codigo

    def invertir(self):
        a = False
        nueva_lista = list()
        lista = self.codigo.strip().split(" ")
        for chunk in lista :
            if "a" in chunk :
                a = True

            if a :
                chunk = chunk[::-1]
                if "a" in chunk :
                    chunk = chunk[:len(chunk)-2]
            nueva_lista.append(chunk)
        nuevo_codigo = " ".join(nueva_lista)
        return nuevo_codigo



