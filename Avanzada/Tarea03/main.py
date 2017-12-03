from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
import libreria as lib
import exceptions as ex


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()
        self.gen_pro = lib.n_generador1
        self.gen_save = lib.n_generador2

    def process_query(self, query_array):
        for consulta in query_array:
            try:
                respuesta = lib.procesar_consulta(consulta)

            except ex.BadRequest as err:
                respuesta = "BadRequest: {}".format(err)

            except IndexError as err:
                respuesta = "BadRequest: Debes Ingresar una consulta"\
                    .format(err)

            except TypeError as err:
                respuesta = "TypeError: Debes ingresar los argumentos" \
                            " correctos"

            except ex.NotFound as err:
                respuesta = "NotFound: {}".format(err)

            except ex.GenomeError as err:
                respuesta = "GenomeError: {}".format(err)

            except ex.NotAcceptable as err:
                respuesta = "NotAcceptable: {}".format(err)

            finally:
                self.add_answer("------------ Consulta {} --------------\n".
                                format(str(next(self.gen_pro))))
                if isinstance(respuesta, list):
                    for r in respuesta:
                        self.add_answer(r + "\n")
                else:
                    self.add_answer(str(respuesta) + "\n")

    def save_file(self, query_array):

        for consulta in query_array:
            try:
                if len(consulta) != 0 and consulta[0] == "visualizar":
                    respuesta = "Bubblechart"
                else:
                    respuesta = lib.procesar_consulta(consulta)

            except ex.BadRequest as err:
                respuesta = "BadRequest: {}".format(err)

            except IndexError as err:
                respuesta = "BadRequest: Debes Ingresar una consulta" \
                    .format(err)

            except TypeError as err:
                respuesta = "TypeError: Debes ingresar los argumentos" \
                            " correctos"

            except ex.NotFound as err:
                respuesta = "NotFound: {}".format(err)

            except ex.GenomeError as err:
                respuesta = "GenomeError: {}".format(err)

            except ex.NotAcceptable as err:
                respuesta = "NotAcceptable: {}".format(err)

            finally:
                with open("ultados.txt", "a") as archivo:
                    print("------------ Consulta {} --------------"
                          .format(next(self.gen_save)), file=archivo)
                    if isinstance(respuesta, list):
                        for r in respuesta:
                            print(r, file=archivo)
                    else:
                        print(str(respuesta), file=archivo)
                    archivo.close()

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)


    sys.__excepthook__ = hook

    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
