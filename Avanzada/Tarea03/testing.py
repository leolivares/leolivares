import unittest
import libreria as lib
import exceptions as ex


class LibreriaTest(unittest.TestCase):

    def setUp(self):
        lib.listas = lib.leer_listas("listas_testing.txt")
        lib.personas = lib.leer_personas("genomas_testing.txt")

    def tearDown(self):
        lib.personas = None
        lib.listas = None

    def test_ascendecia(self):
        self.assertEqual(lib.ascendencia("Henry Boys"), ["Estadounidense"])

    def test_indice_de_tamano(self):
        self.assertEqual(lib.indice_de_tamano("Paula Salvo"), "0.408248290464")

    def test_pariente_de(self):
        self.assertEqual(lib.pariente_de(0, "Hernán Valdivieso"),
                         ["Marcelo Lagos"])

    def test_gemelo(self):
        self.assertEqual(lib.gemelo_genetico("El Chuña"), ['Rick Sánchez'])
        self.assertEqual(lib.gemelo_genetico("Henry Boys"),
                         ['Alejandro Kaminetzky'])

    def test_valor_caracteristica(self):
        self.assertEqual(lib.valor_caracteristica("TCT", "Stephanie Chau"),
                         "Moreno")
        self.assertEqual(lib.valor_caracteristica("CTC", "Marcelo Lagos"), 43)

    def test_min(self):
        self.assertEqual(lib.minimo_estadistica("AAG"), "1.4")

    def test_max(self):
        self.assertEqual(lib.maximo_estadistica("TCT"), "Moreno")

    def test_prom(self):
        self.assertEqual(lib.prom("AAG"), "1.7264672364672364")

    def test_errores(self):
        self.assertRaises(ex.BadRequest, lib.procesar_consulta,
                          ["pariente", 1, "Sterling Archer"])
        self.assertRaises(ex.NotFound, lib.ascendencia, "Leonardo Olivares")
        self.assertRaises(ex.NotAcceptable, lib.pariente_de, 0, "Paula Salvo")
        lib.personas.append(lib.Persona(nombre='Leo', apellido='Olivares',
                                        nombre_completo='Leo Olivares',
                                        adn={"AAG": ["ACT", "A A"],
                                             "TCT": ["MGT"]}))
        self.assertRaises(ex.GenomeError, lib.valor_caracteristica,
                          "TCT", "Leo Olivares")
        self.assertRaises(ex.GenomeError, lib.valor_caracteristica,
                          "AAG", "Leo Olivares")

if __name__ == "__main__":
    unittest.main()
