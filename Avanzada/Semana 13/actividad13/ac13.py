import os
import pickle
import json


class Cliente:

    def __init__(self, rut, nombre, apellido, fecha_nacimiento, _id, tipo_cuenta, clave, balance):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nac = fecha_nacimiento
        self.num_cuenta = _id
        self.tipo_cuenta = tipo_cuenta
        self.clave = clave
        self.balance = balance

    def __getstate__(self):
        nueva = self.__dict__.copy()
        real = {}
        for attr in nueva:
            real[encriptar(attr)] = encriptar(nueva[attr])

        return real


    def __setstate__(self, state):
        nuevo_dict = {}
        for attr in state:
            nuevo_dict[desencriptar(attr)] = desencriptar(state[attr])
        self.__dict__ = nuevo_dict


class ClienteEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, Cliente):
            return {"Rut": obj.rut,
                    "Nombre": obj.nombre,
                    "Apellido": obj.apellido,
                    "Fecha de Nacimiento": obj.fecha_nac,
                    "Numero de Cuenta": obj.num_cuenta,
                    "Tipo de cuenta": obj.tipo_cuenta,
                    "Clave": obj.clave,
                    "Balance": obj.balance}


def obtener_ruts():
    with open("ruts_para_leer.txt", "r") as file:
        ruts = [linea.strip() for linea in file]
    return ruts

def buscar_paths(ruts):
    paths_a_considerar = list()

    archivos = os.listdir("base_de_datos_banco")
    for archivo in archivos:
        archivos_internos = os.listdir(os.path.join("base_de_datos_banco", archivo))
        for arch in archivos_internos:
            ult_archivos = os.listdir(os.path.join("base_de_datos_banco", archivo, arch))
            for rut in ruts:
                rut_necesario = rut + ".json"
                if rut_necesario in ult_archivos:
                    paths_a_considerar.append(
                        os.path.join("base_de_datos_banco",
                                     archivo, arch, rut_necesario))

    return paths_a_considerar

def buscar_clientes(paths):
    clientes = list()
    for path in paths:
        with open(path, "r") as file:
            cliente = json.load(file, object_hook=lambda dict_obj: funcion_hook(dict_obj))
            clientes.append(Cliente(**cliente))
    return clientes

def funcion_hook(dict_obj):
    parametros_necesarios = ["rut", "nombre", "apellido", "fecha_nacimiento",
                             "_id", "tipo_cuenta", "clave", "balance"]
    nuevo_dict = dict()
    for para in parametros_necesarios:
        nuevo_dict.update({para: dict_obj[para]})
    return nuevo_dict

def nuevos_json(clientes):
    for cliente in clientes:
        with open("bd_json/{}.json".format(cliente.rut), "w") as file:
            json.dump(cliente, file, cls=ClienteEncoder, indent=4)

def encriptar(string):
    new = ""

    if isinstance(string, str):
        for caracter in string:
            value = ord(caracter)
            v = value + 22
            if v > 127:
                v = v % 127
            new += chr(v)
        return new

    return string

def desencriptar(string):
    new = ""
    if isinstance(string, str):
        for caracter in string:
            value = ord(caracter)
            v = value - 22
            if v < 0:
                v = 127 + v
            new += chr(v)
        return new

    return string


#Para los siguientes dos metodos, debe existir el directorio bd_segura
def guardar_pickle(clientes):
    for cliente in clientes:
        with open("bd_segura/{}.txt".format(cliente.rut), "wb") as file:
            a = pickle.dump(cliente, file)

def leer_pickles():
    clientes = []
    for archivo in os.listdir("bd_segura"):
        with open("bd_segura/{}".format(archivo), "rb") as file:
            cliente = pickle.load(file)
            clientes.append(cliente)

    return clientes


if __name__ == '__main__':
    ruts = obtener_ruts()
    paths = buscar_paths(ruts)
    clientes = buscar_clientes(paths)

    #Se crean los nuevos archivos json
    nuevos_json(clientes)

    #Se guardan las instancias encriptadas en bd_segura
    guardar_pickle(clientes)
    # Se leen las instancias anteriores. A continuacion se encuentran en
    # una lista
    clientes = leer_pickles()


