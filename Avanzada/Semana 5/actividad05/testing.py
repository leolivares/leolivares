import unittest
import form as f
import exceptions as es

class Testeo(unittest.TestCase) :

    def setUp(self):
        self.form = f.FormRegister()

    def test_rut_1(self):
        self.assertFalse(self.form.check_rut("19657850-8"))

    def test_rut_2(self):
        self.assertRaises(es.PuntoExcepcion, self.form.check_rut,"19.657.850-1")
        self.assertTrue(self.form.check_rut("19657850-1"))

    def test_registro(self):
        self.form.register_people_info( "Leo", "Masculino", "Algo")
        self.form.register_people_info( "Ivania", "Femenino", "Algo2")

        self.assertEqual(["Ivania","Femenino","Algo2"],self.form.register_list[-1])

    def test_save(self):
        archivo = open("result.txt","r")
        lineas = archivo.readlines()
        limpio = []
        for l in lineas :
            limpio.append(l.strip().split(","))

        self.assertEqual([['Student: Hugo Navarrete'], ['Gender: Masculino'],['Comment: Necesito ese curso']],[limpio[0],limpio[1],limpio[2]])




if __name__ == "__main__" :
    unittest.main()

