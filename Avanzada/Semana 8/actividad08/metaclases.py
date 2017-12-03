from functions import peon_valid_move, alfil_valid_move, torre_valid_move,\
    caballo_valid_move, rey_valid_move, chess_valid_move, reina_valid_move
from collections import defaultdict
from functools import reduce

class MetaChess(type):
    instanciado = False

    def __new__(meta, name, base, clsdict):

        anterior = clsdict["__init__"]

        def init(self, *args, **kwargs):
            if len(args) == 0:
                return None
            anterior(self)
            for pieza in args:
                self.add_piece(pieza)

        def valid_move(self, i, j, x, y):
            verificar = chess_valid_move(self, i, j, x, y)
            return verificar

        def call(self, *args, **kwargs):
            if not MetaChess.instanciado:
                raise TypeError



        clsdict.update({"__init__": init})
        clsdict.update({"valid_move": valid_move})
        clsdict.update({"__call__": call})


        return super().__new__(meta, name, base, clsdict)

    def __call__(cls, *args, **kwargs):

        if len(args) == 0:
            return None

        pieces = dict()
        for a in args:
            if str(a) in pieces:
                pieces[str(a)] += 1
            else:
                pieces[str(a)] = 1

        def verificar(dicc):
            if dicc["P"] == 16 and dicc["R"] == 2 and dicc["F"] == 2 \
                    and dicc["A"] == 4 and dicc["T"] == 4 and dicc["C"] == 4:
                return True
            return False

        cantidad = list(map(lambda x: pieces[x], pieces))
        cantidad = reduce(lambda x, y: x+y, cantidad)
        if cantidad == 32:
            verificar = verificar(pieces)

        if verificar:
            if not MetaChess.instanciado:
                MetaChess.instanciado = True
                instance = super().__call__(*args, **kwargs)
                MetaChess.ins = instance
                return instance

        else:
            return MetaChess.ins


class MetaPiece(type):
    def MetaPiece(type):

        def __new__(meta, nombre, bases, diccionario):
            if nombre == "Peon":
                diccionario["valid_move"] = peon_valid_move
            elif nombre == "Alfil":
                diccionario["valid_move"] = alfil_valid_move
            elif nombre == "Torre":
                diccionario["valid_move"] = torre_valid_move
            elif nombre == "Caballo":
                diccionario["valid_move"] = caballo_valid_move
            elif nombre == "Rey":
                diccionario["valid_move"] = rey_valid_move
            else:
                diccionario["valid_move"] = reina_valid_move
            return super().__new__(meta, nombre, bases, dict)

        piezas = {"Peon": [16, 0, 0], "Rey": [2, 0, 0], "Reina": [2, 0, 0],
                  "Alfil": [4, 0, 0], "Torre": [4, 0, 0], "Caballo": [4, 0, 0]}
        # el 0,0 representa las piezas de c/u jugador
        # parto agregando a la izquierda, el cual representa las piezas True
        def __call__(cls, *args, **kwargs):
            if cls.nombre == "Peon":
                if len(piezas["Peon"][1]) and len(piezas["Peon"][2]) < 8:
                    if len(piezas["Peon"][1]) == len(piezas["Peon"][2]):
                        piezas["Peon"][1] += piezas["Peon"][1]
                        return super().__call__(*args, **kwargs)
                    else:
                        nuevo_booleano = False
                        piezas["Peon"][2] += piezas["Peon"][2]
                        return super().__call__(*args[:2], nuevo_booleano, **kwargs)
                else:
                    pass

            elif cls.nombre == "Rey":
                if len(piezas["Rey"][1]) and len(piezas["Rey"][2]) < 1:
                    if len(piezas["Rey"][1]) == len(piezas["Rey"][2]):
                        piezas["Rey"][1] += piezas["Rey"][1]
                        return super().__call__(*args, **kwargs)
                    else:
                        nuevo_booleano = FalseReina
                        piezas["Rey"][2] += piezas["Rey"][2]
                        return super().__call__(*args[:2], nuevo_booleano, **kwargs)
                else:
                    pass

            elif cls.nombre == "Reina":
                if len(piezas["Reina"][1]) and len(piezas["Reina"][2]) < 1:
                    if len(piezas["Reina"][1]) == len(piezas["Reina"][2]):
                        piezas["Reina"][1] += piezas["Reina"][1]
                        return super().__call__(*args, **kwargs)
                    else:
                        nuevo_booleano = False
                        piezas["Reina"][2] += piezas["Reina"][2]
                        return super(). __call__(*args[:2], nuevo_booleano, **kwargs)
                else:
                    pass

            elif cls.nombre == "Caballo":
                if len(piezas["Caballo"][1]) and len(piezas["Caballo"][2]) < 2:
                    if len(piezas["Caballo"][1]) == len(piezas["Caballo"][2]):
                        piezas["Caballo"][1] += piezas["Caballo"][1]
                        return super().__call__(*args, **kwargs)
                    else:
                        nuevo_booleano = False
                        piezas["Caballo"][2] += piezas["Caballo"][2]
                        return super().__call__(*args[:2], nuevo_booleano, **kwargs)
                else:
                    pass

            elif cls.nombre == "Torre":
                if len(piezas["Torre"][1]) and len(piezas["Torre"][2]) < 2:
                    if len(piezas["Torre"][1]) == len(piezas["Torre"][2]):
                        piezas["Torre"][1] += piezas["Torre"][1]
                        return super().__call__(*args, **kwargs)
                    else:
                        nuevo_booleano = False
                        piezas["Torre"][2] += piezas["Torre"][2]
                        return super().__call__(*args[:2], nuevo_booleano, **kwargs)
                else:
                    pass

            else:
                if len(piezas["Alfil"][1]) and len(piezas["Alfil"][2]) < 2:
                    if len(piezas["Alfil"][1]) == len(piezas["Alfil"][2]):
                        piezas["Alfil"][1] += piezas["Alfil"][1]
                        return super(). __call__(*args, **kwargs)
                    else:
                        nuevo_booleano = False
                        piezas["Alfil"][2] += piezas["Alfil"][2]
                        return super().__call__(*args[:2], nuevo_booleano, **kwargs)
                else:
                    pass