import unittest
import main as ma

class TestearFormato(unittest.TestCase) :

    def setUp(self):
        self.codigo = ''
        with open("mensaje_marciano.txt", "r") as archivo:
            lineas = archivo.readlines()
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:
                self.codigo += caracter

    def test_cantidad_caracteres(self):
        cant = len(self.codigo)
        print(cant)
        self.assertEqual(cant,408)

    def test_string(self):
        self.assertTrue(isinstance(self.codigo,str))

    def test_sumatoria(self):
        suma = 0

        for a in self.codigo :
            if a != "a" and a != " ":
                suma += int(a)
        self.assertEqual(suma,253)

class TestearMensaje(unittest.TestCase) :

    def setUp(self):
        self.des = ma.Descifrador('mensaje_marciano.txt')

    def test_elimina_incorrectos(self):
        self.des.lectura_archivo()
        codigo = self.des.elimina_incorrectos().strip().split(" ")

        for chunk in codigo :

            self.assertLess(len(chunk),7)
            self.assertGreater(len(chunk),6)








if __name__ == "__main__" :
    unittest.main()