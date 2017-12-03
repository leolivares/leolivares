import numpy
import exceptions as ex
import matplotlib.pyplot as plt
from functools import reduce
from collections import namedtuple, defaultdict


Persona = namedtuple("Persona", ["nombre", "apellido",
                                 "nombre_completo", "adn"])

caracteristicas = {"GTC": "Ojos", "GGA": "Pelo", "GTA": "Nariz",
                   "AAG": "Altura", "CTC": "Pies", "TCT": "Piel",
                   "TGG": "Guata", "CGA": "Vello Corporal", "TAG": "Vision"}

determinista = {"GTC": "Ojos", "GGA": "Pelo", "GTA": "Nariz"}
continua = {"AAG": "Altura", "CTC": "Pies", "TCT": "Piel", "TGG": "Guata"}
complementaria = {"CGA": "Vello Corporal", "TAG": "Vision"}

valores = {"Altura": {"AGT": "Alto", "ACT": "Bajo"},
           "Ojos": {"CCT": "Cafes", "AAT": "Azules", "CAG": "Verdes"},
           "Pelo": {"GTG": "Negro", "AAT": "Rubio", "CCT": "Pelirrojo"},
           "Piel": {"AAT": "Clara", "GCG": "Oscura"},
           "Nariz": {"TCG": "Aguilena", "CAG": "Respingada", "TAC": "Recta"},
           "Pies": {"GTA": "Grandes", "CCA": "Chicos"},
           "Vello Corporal": {"TGC": "Pecho", "GTG": "Axila",
                              "CCT": "Espalda"},
           "Guata": {"AGT": "Grande", "ACT": "Chica"},
           "Vision": {"TTC": "Daltonismo", "ATT": "Miopia"}}

mediterranea = {"Pelo": "Negro", "Vello Corporal": "Pecho", "Nariz": "Recta"}
africana = {"Piel": "Negra", "Pelo": "Negro", "Pies": 44}
estadounidense = {"Guata": "Guaton Parrillero", "Vello Corporal": "Espalda"}


# Se encarga de entregar los numeros que se encuentran en el codigo genetico
def funcion_generadora(texto):
    numero, i = ("", 0)
    while i != len(texto):
        caracter = texto[i]
        if caracter.isdigit() or caracter == " ":
            numero += caracter
            i += 1
        else:
            yield int(numero)
            numero = ""
            while not caracter.isdigit() and i != len(texto):
                i += 1
                if i != len(texto):
                    caracter = texto[i]
    yield int(numero)


# Se encarga de entregar los genes correspondientes a una posicion
def generador_pos(posiciones, letras):
    i = 0
    actual = 0
    while i < len(posiciones):
        gen = next(letras) + next(letras) + next(letras)
        if actual == int(posiciones[i]):
            yield gen
            if i+1 < len(posiciones) and\
                            int(posiciones[i]) == int(posiciones[i+1]):
                yield gen
                i += 1
            i += 1
        actual += 1


# Se encarga de crear las namedtuples a partir del codigo genetico
def crear_persona(codigo):

    numeros, letras = obtener_info(codigo)

    nombre, apellido = obtener_nombre(letras, numeros)
    nombre_completo = nombre + " " + apellido

    caracteristicas = obtener_caracteristicas(letras, numeros)
    adn = obtener_adn(letras, caracteristicas)

    return Persona(nombre, apellido, nombre_completo, adn)


# Se encarga de realizar un conteo de los genes codificantes
# de una caracteristica
def analizar_caracteristica(caract, persona):
    if persona.adn[caract] != [""]:
        seleccionados = persona.adn[caract]
        set = {verificar(k, persona) for k in seleccionados}
        conteo = [seleccionados.count(k) for k in set]
        datos = {k: v for k, v in zip(set, conteo)}
        return datos
    return dict()


# Se encarga de separar las letras y los numeros del codigo genetico
# En generadores, para ocupar menos memoria
def obtener_info(codigo):
    generador = funcion_generadora(codigo)
    numeros = (next(generador) for _ in range(11))
    letras = (x for x in codigo if not x.isdigit())
    return numeros, letras


# Se encarga de retornar el nombre y apellido
def obtener_nombre(letras, numeros):
    nombre = "".join(list((next(letras) for _ in range(next(numeros)))))
    apellido = "".join(list(next(letras) for _ in range(next(numeros))))
    print(nombre, len(nombre))
    print(apellido, len(apellido))
    return nombre, apellido


# Se encarga de asignar a cada caracteristica su lista correspondiente
def obtener_caracteristicas(letras, numeros):
    numeros = list(numeros)
    tipos = (next(letras) + next(letras) + next(letras)
             for _ in range(len(numeros)))
    caracteristicas = {k: v for k, v in zip(tipos, numeros)}
    return caracteristicas


# Se encarga de seleccionar los genes codificantes de cada caracteristica
def obtener_adn(letras, caracteristicas):
    posiciones = filter(lambda x: x != "",
                        reduce(lambda x, y: x+y,
                               [listas[x] for x in caracteristicas.values()]))
    posiciones = sorted(posiciones, key=lambda x: int(x))
    generador_posiciones = generador_pos(posiciones, letras)
    seleccionados = [next(generador_posiciones)
                     for _ in range(len(posiciones))]
    conjunto = list(zip(posiciones, seleccionados))
    adn = {k: obtener_genes(listas[caracteristicas[k]],
                            conjunto) for k in caracteristicas}
    return adn


# Asigna los genes a las caracteristicas
def obtener_genes(lista, conjunto):
    genes = map(lambda x: x[1], filter(lambda x: x[0] in lista, conjunto))
    return list(genes)


# Lee el archivo de genomas y crea una lista de namedtuples
def leer_personas(nombre):
    with open(nombre) as file:
        personas = [crear_persona(line.strip()) for line in file]
    return personas


# Lee el archivo de listas y crea un diccionario
def leer_listas(nombre):
    with open(nombre) as file:
        l = [line.strip().split(";") for line in file]
        listas = {int(x[0]): x[1].strip().split(",") for x in l}
    return listas


# Determina los fenotipos de cada caracteristica
def fenotipo(person):
    datos = analisis(person)
    valores = {caract: determinar_fenotipo(dicc, caract)
               for caract, dicc in datos.items()}
    return valores


# Obtiene los conteos de genes de cada caaracteristica
def analisis(person):
    datos = {caract: analizar_caracteristica(caract, person)
             for caract in person.adn}
    return datos


# Retorna la ascendencia de una persona
def ascendencia(persona):
    person = buscar_persona(persona)
    if len(person) != 0:
        person = person[0]
        valores = fenotipo(person)
        ascendencias = obtener_ascendecias(valores, person)
        if len(ascendencias) == 0:
            raise ex.NotAcceptable
        return ascendencias


# Retorna una lista con las ascendencias que cumplen
def obtener_ascendecias(valores, person):
    lista_asc = []
    if checkear_med(valores):
        lista_asc.append("Mediterranea")
    if checkear_afr(valores):
        lista_asc.append("Africana")
    if checkear_est(valores):
        lista_asc.append("Estadounidense")
    if checkear_alb(person):
        lista_asc.append("Albina")
    return lista_asc


# Las siguientes funciones verifican que los fenotipos cumplan con los
# requerimientos para formar parte de una ascendencia
def checkear_med(valores):
    valores = {k: v for k, v in valores.items() if
               caracteristicas[k] in mediterranea}
    cumple = True
    if "GGA" not in valores \
            or valores["GGA"] != mediterranea[caracteristicas["GGA"]]:
        cumple = False
    if "GTA" not in valores \
            or valores["GTA"] != mediterranea[caracteristicas["GTA"]]:
        cumple = False
    if "CGA" not in valores \
            or mediterranea[caracteristicas["CGA"]] not in valores["CGA"]:
        cumple = False
    return cumple


def checkear_afr(valores):
    valores = {k: v for k, v in valores.items() if
               caracteristicas[k] in africana}
    cumple = True
    if "GGA" not in valores \
            or valores["GGA"] != africana[caracteristicas["GGA"]]:
        cumple = False
    if "TCT" not in valores \
            or valores["TCT"] != africana[caracteristicas["TCT"]]:
        cumple = False
    if "CTC" not in valores \
            or africana[caracteristicas["CTC"]] > valores["CTC"]:
        cumple = False
    return cumple


def checkear_est(valores):
    valores = {k: v for k, v in valores.items() if
               caracteristicas[k] in estadounidense}
    cumple = True
    if "TGG" not in valores \
            or valores["TGG"] != estadounidense[caracteristicas["TGG"]]:
        cumple = False
    if "CGA" not in valores \
            or estadounidense[caracteristicas["CGA"]] not in valores["CGA"]:
        cumple = False
    return cumple


def checkear_alb(person):
    cumple = True
    caract = ["GGA", "GTC", "TCT"]
    valores = {c: analizar_caracteristica(c, person) for c in caract}
    verificar = [True for x in valores if "AAT" in valores[x]]
    if len(verificar) != 3:
        cumple = False
    return cumple


# Verifica que los genomas a utilizar sean correctos
# Levanta error de genoma en caso de necesario
def verificar(tag, person):
    if not tag.isalpha():
        raise ex.GenomeError(person.nombre_completo)
    checkeo = [x for x in tag if x not in ["A", "C", "G", "T"]]
    if len(checkeo) != 0:
        raise ex.GenomeError(person.nombre_completo)
    return tag


# Dertermina el tipo de una caracterisitca
def determinar_tipo(caract):
    if caract in determinista:
        return "determinista"
    elif caract in continua:
        return "continua"
    elif caract in complementaria:
        return "complementaria"


# Determina el fenotipo de una caracteristica
def determinar_fenotipo(datos, caract):
    tipo = determinar_tipo(caract)
    caracteristica = caracteristicas[caract]
    fenotipo = ""
    if tipo == "determinista" and datos:
        fenotipo = datos_determinista(datos, caracteristica)
    elif tipo == "continua" and datos:
        fenotipo = datos_continua(datos, caracteristica)
    elif tipo == "complementaria":
        if datos:
            fenotipo = datos_complementaria(datos, caracteristica)
        else:
            fenotipo = "No tiene"
    return fenotipo


# Las siguientes funciones determinan el fenotipo segun el tipo
# de caracteristica
def datos_complementaria(datos, caracteristica):
    cantidad = reduce(lambda x, y: x+y, map(lambda x: datos[x], datos))
    val = map(lambda x: c_percent(x, cantidad), datos.items())
    val = map(lambda x: x[0], filter(lambda x: x[1] >= 0.2, val))
    val = list(map(lambda x: valores[caracteristica][x], val))
    return val


def c_percent(x, cantidad):
    porcentaje = x[1]/cantidad
    return (x[0], porcentaje)


def datos_determinista(datos, caracteristica):
    set = {x for x in datos}
    if caracteristica == "Ojos":
        valor = fenotipo_ojos(set)
    elif caracteristica == "Pelo":
        valor = fenotipo_pelo(set)
    elif caracteristica == "Nariz":
        valor = fenotipo_nariz(set)
    return valor


def fenotipo_ojos(set):
    if "CCT" in set:
        valor = "Cafes"
    elif "AAT" in set:
        valor = "Azules"
    elif "CAG" in set:
        valor = "Verdes"
    return valor


def fenotipo_pelo(set):
    if "GTG" in set:
        valor = "Negro"
    elif "AAT" in set:
        valor = "Rubio"
    elif "CCT" in set:
        valor = "Pelirrojo"
    return valor


def fenotipo_nariz(set):
    if "TCG" in set:
        valor = "Aguilena"
    elif "CAG" in set:
        valor = "Respingada"
    elif "TAC" in set:
        valor = "Recta"
    return valor


def datos_continua(datos, caracteristica):
    cantidad = reduce(lambda x, y: x+y, map(lambda x: datos[x], datos))
    porcentaje = 0
    tipos = {"Altura": "AGT", "Piel": "AAT", "Pies": "GTA", "Guata": "ACT"}

    if caracteristica in tipos and tipos[caracteristica] in datos:
        porcentaje = _porcentaje(datos, cantidad, tipos[caracteristica])

    return obtener_fenotipo(porcentaje, caracteristica)


def _porcentaje(datos, cantidad, tipo):
    porcentaje = (list(map(lambda x: x[1],
                           filter(lambda x: x[0] == tipo,
                                  datos.items())))[0] / cantidad) * 100
    return porcentaje


def obtener_fenotipo(porcentaje, caract):
    if caract == "Altura":
        valor = ((0.7 * porcentaje) / 100) + 1.4
    elif caract == "Piel":
        valor = fenotipo_piel(porcentaje)
    elif caract == "Pies":
        valor = round(((14 * porcentaje) / 100) + 34)
    elif caract == "Guata":
        valor = fenotipo_guata(porcentaje)
    return valor


def fenotipo_piel(porcentaje):
    if porcentaje >= 0 and porcentaje <= 24.9999:
        valor = "Negro"
    elif porcentaje >= 25 and porcentaje <= 49.9999:
        valor = "Moreno"
    elif porcentaje >= 50 and porcentaje <= 74.9999:
        valor = "Blanco"
    elif porcentaje >= 75 and porcentaje <= 100:
        valor = "Albino"
    return valor


def fenotipo_guata(porcentaje):
    if porcentaje >= 0 and porcentaje <= 24.9999:
        valor = "Guaton Parrillero"
    elif porcentaje >= 25 and porcentaje <= 49.9999:
        valor = "Manana Empiezo la Dieta"
    elif porcentaje >= 50 and porcentaje <= 74.9999:
        valor = "Atleta"
    elif porcentaje >= 75 and porcentaje <= 100:
        valor = "Modelo"
    return valor


# Retorna el indice de tamaño
def indice_de_tamano(persona):
    person = buscar_persona(persona)

    if len(person) != 0:
        caract = ["AAG", "TGG"]
        datos = {c: analizar_caracteristica(c, person[0]) for c in caract}
        porcentajes = (calcular_porcentaje(x) for x in list(datos.values()))
        indice = numpy.sqrt(reduce(lambda x, y: x*y, porcentajes))
        return str(indice)


def calcular_porcentaje(datos):
    cantidad = reduce(lambda x, y: x+y, map(lambda x: datos[x], datos))
    porcentaje = 0
    if "AGT" in datos:
        porcentaje = (datos["AGT"] / cantidad)
    return porcentaje


# Retorna el fenotipo de cierta caracterisica
def valor_caracteristica(tag_identificador, persona):
    person = buscar_persona(persona)

    if len(person) != 0:
        analisis = {caract: analizar_caracteristica(caract, person[0])
                    for caract in person[0].adn}
        valores = {caract: determinar_fenotipo(dicc, caract)
                   for caract, dicc in analisis.items()}
        if valores[tag_identificador] == "":
            raise ex.NotAcceptable
        return valores[tag_identificador]


# Filtra a las personas y retorna a la que tenga cierto nombre
def buscar_persona(persona):
    person = list(filter(lambda pers: pers.nombre_completo == persona,
                         personas))
    if len(person) == 0:
        raise ex.NotFound(persona, "Persona")
    return person


# Dependiendo del grado, retorna a los parientes
def pariente_de(grado, persona):
    busquedas = {-1: parientes_menos_uno, 0: parientes_cero, 1: parientes_uno,
                 2: parientes_dos, "n": parientes_n}
    person = buscar_persona(persona)
    if len(person) != 0:
        person = person[0]
        if grado in busquedas:
            parientes = busquedas[grado](person)
            if len(parientes) == 0:
                raise ex.NotAcceptable
            return parientes
        else:
            raise ex.NotFound(grado, "Grado")


def parientes_menos_uno(person):
    datos = fenotipo(person)
    conjunto = fenotipo_otros(person)
    parientes = list(filter(lambda x: x, (distintos(datos, x)
                                          for x in conjunto)))
    return parientes


def parientes_cero(person):
    datos = fenotipo(person)
    conjunto = fenotipo_otros(person)
    parientes = list(filter(lambda x: x, (iguales(datos, x)
                                          for x in conjunto)))
    return parientes


def parientes_uno(person):
    datos = fenotipo(person)
    conjunto = fenotipo_otros(person)
    parientes = list(filter(lambda x: x, (grado_uno(datos, x)
                                          for x in conjunto)))
    return parientes


def parientes_dos(person):
    datos = fenotipo(person)
    conjunto = fenotipo_otros(person)
    parientes = list(filter(lambda x: x, (grado_dos(datos, x)
                                          for x in conjunto)))
    return parientes


def parientes_n(person):
    datos = fenotipo(person)
    conjunto = fenotipo_otros(person)
    parientes = list(filter(lambda x: x, (grado_n(datos, x)
                                          for x in conjunto)))
    return parientes


def grado_uno(datos, conjunto):
    dicc = conjunto[1]
    if dicc["GTC"] == datos["GTC"] and dicc["TCT"] == datos["TCT"] \
            and dicc["GGA"] == datos["GGA"] and dicc["TAG"] == datos["TAG"] \
            and dicc["GTA"] == datos["GTA"]:
        dif_altura = valor_absoluto(float(dicc["AAG"]) - float(datos["AAG"]))
        dif_pies = valor_absoluto(int(dicc["CTC"]) - int(datos["CTC"]))
        if dif_altura <= 0.2 and dif_pies <= 2:
            return conjunto[0]


def grado_dos(datos, conjunto):
    dicc = conjunto[1]
    if dicc["GGA"] == datos["GGA"] and dicc["TCT"] == datos["TCT"]\
            and dicc["TAG"] == datos["TAG"]:
        dif_altura = valor_absoluto(float(dicc["AAG"]) - float(datos["AAG"]))
        dif_pies = valor_absoluto(int(dicc["CTC"]) - int(datos["CTC"]))
        if dif_altura <= 0.5 and dif_pies <= 4:
            return conjunto[0]


def grado_n(datos, conjunto):
    dicc = conjunto[1]
    if dicc["TCT"] == datos["TCT"]:
        dif_altura = valor_absoluto(float(dicc["AAG"]) - float(datos["AAG"]))
        dif_pies = valor_absoluto(int(dicc["CTC"]) - int(datos["CTC"]))
        if dif_altura <= 0.7 and dif_pies <= 6:
            valores = {"Modelo": 1, "Atleta": 2, "Manana Empiezo la Dieta": 3,
                       "Guaton Parrillero": 4}
            dif_guata = valor_absoluto(valores[dicc["TGG"]]
                                       - valores[datos["TGG"]])
            if dif_guata <= 1:
                return conjunto[0]


def fenotipo_otros(person):
    otros = list(filter(lambda x: x.nombre_completo != person.nombre_completo,
                        personas))
    otros_nombres = list(map(lambda x: x.nombre_completo, otros))
    otros_fen = map(lambda x: fenotipo(x), otros)
    conjunto = list(zip(otros_nombres, otros_fen))
    return conjunto


def genotipo_otros(person):
    otros = list(filter(lambda x: x.nombre_completo != person.nombre_completo,
                        personas))
    otros_nombres = list(map(lambda x: x.nombre_completo, otros))
    otros_gen = map(lambda x: analizar)


def iguales(datos, conjunto):
    comparacion = [True if datos[x] == conjunto[1][x]
                   else False for x in datos]
    if False not in comparacion:
        return conjunto[0]


def distintos(datos, conjunto):
    comparacion = [True if datos[x] == conjunto[1][x]
                   else False for x in datos]
    if True not in comparacion:
        return conjunto[0]


def valor_absoluto(x):
    if x < 0:
        x *= -1
    return x


# Retorna a el/los gemelos geneticos
def gemelo_genetico(persona):
    person = buscar_persona(persona)
    if len(person) != 0:
        person = person[0]
        datos = analisis(person)
        otros = filter(lambda x: x.nombre_completo != person.nombre_completo,
                       personas)
        otros_datos = {x.nombre_completo: analisis(x) for x in otros}
        genes_iguales = {x: comparar_genes(datos, otros_datos[x])
                         for x in otros_datos}
        num = genes_iguales[max(genes_iguales, key=lambda x: genes_iguales[x])]
        gem = list(gemelos(num, genes_iguales))
        if len(gem) == 0:
            raise ex.NotAcceptable
        return gem
    else:
        raise ex.NotFound(persona, "Persona")


# Calcula la cantidad de genes en comun
def comparar_genes(datos, otros_datos):
    comun = reduce(lambda x, y: x+y, (minimo(datos[i], otros_datos[i])
                                      for i in otros_datos))
    return comun


def minimo(datos, otros_datos):
    set = {x for x in datos if x in otros_datos}
    mini = 0
    if len(set) != 0:
        mini = reduce(lambda x, y: x+y, (datos[x] if datos[x] <= otros_datos[x]
                                         else otros_datos[x] for x in set))
    return mini


def gemelos(num, dicc):
    return filter(lambda x: dicc[x] == num, dicc)


# Retorna el fenotipo menos presente de cierta caracteristica
def minimo_estadistica(tag):
    if tag not in caracteristicas:
        raise ex.NotFound(tag, "Tag")

    cantidades = list(map(lambda x:
                          valor_caracteristica(tag, x.nombre_completo),
                          personas))
    if tag == "AAG" or tag == "CTC":
        return str(min(cantidades))
    elif tag in determinista or tag == "TCT":
        sett = set(cantidades)
        conteo = {x: cantidades.count(x) for x in sett}
        return str(min(conteo, key=lambda x: conteo[x]))


# Rertorna el fenotipo mas presente de cierta caracteristica
def maximo_estadistica(tag):
    if tag not in caracteristicas:
        raise ex.NotFound(tag, "Tag")

    cantidades = list(map(lambda x:
                          valor_caracteristica(tag, x.nombre_completo),
                          personas))
    if tag == "AAG" or tag == "CTC":
        return str(max(cantidades))
    elif tag in determinista or tag == "TCT":
        sett = set(cantidades)
        conteo = {x: cantidades.count(x) for x in sett}
        return str(max(conteo, key=lambda x: conteo[x]))


# Retorna el promedio de global de altura o talla de pies
def prom(tag):
    if tag not in caracteristicas:
        raise ex.NotFound(tag, "Tag")

    if tag == "AAG" or tag == "CTC":
        cantidades = list(map(lambda x:
                              valor_caracteristica(tag, x.nombre_completo),
                              personas))
        return str(reduce(lambda x, y: x+y, cantidades) / len(cantidades))


# Funcion generadora para numero de consultas
def num_consulta():
    i = 1
    while True:
        yield i
        i += 1


# BONUS: Se debe ingresar el tag de la caracteristica
def visualizar(tipo):
    tipos = {"GTC": ["Azules", "Verdes", "Cafes"],
             "GGA": ["Negro", "Rubio", "Pelirrojo"]}
    if tipo in tipos:
        areas = list(calcular_cantidad(tipo))
        posiciones_y = list((posicion_y(tipo, x) for x in tipos[tipo]))
        posiciones_x = list((posicion_x(tipo, x) for x in tipos[tipo]))
        n = [5, 500, 1000]
        plt.scatter(posiciones_x, posiciones_y, s=areas, c=n, alpha=0.5)
        [plt.annotate(tipos[tipo][i], (posiciones_x[i], posiciones_y[i]))
         for i in range(len(tipos[tipo]))]
        plt.xlabel('Promedio de Talla de Pies')
        plt.ylabel('Promedio de Altura')
        plt.title('BubbleChart: Proporcion de {} segun Altura y Tallas'
                  .format(tipo))
        plt.show(block=False)
        return "Bubblechart de {}".format(tipo)
    raise ex.NotFound(tipo, "Tipo")


def calcular_cantidad(tag):
    tipos = {"GTC": ["Azules", "Verdes", "Cafes"],
             "GGA": ["Negro", "Rubio", "Pelirrojo"]}
    datos = [valor_caracteristica(tag, per.nombre_completo)
             for per in personas]
    cantidades = (datos.count(tipo) * 150 for tipo in tipos[tag])
    return cantidades


def posicion_y(caract, valor):
    persons = filter(lambda x:
                     valor_caracteristica(caract, x.nombre_completo) == valor,
                     personas)
    tamanos = list(map(lambda x: valor_caracteristica("AAG",
                                                      x.nombre_completo),
                       persons))
    promedio = reduce(lambda x, y: x + y, tamanos) / len(tamanos)
    return promedio


def posicion_x(caract, valor):
    persons = filter(lambda x:
                     valor_caracteristica(caract, x.nombre_completo) == valor,
                     personas)
    tamano_pies = list(map(lambda x: valor_caracteristica("CTC",
                                                          x.nombre_completo),
                           persons))
    promedio = reduce(lambda x, y: x + y, tamano_pies) / len(tamano_pies)
    return promedio


# Se encarga de verificar que la consulta exista, y la llama
def procesar_consulta(consulta):

    if len(consulta) == 0:
        raise IndexError
    if consulta[0] not in consultas:
        raise ex.BadRequest(consulta[0])

    arguments = consulta[1:]
    return consultas[consulta[0]](*arguments)


n_generador1 = num_consulta()
n_generador2 = num_consulta()
listas = leer_listas("listas.txt")
personas = leer_personas("genomas.txt")

consultas = {"ascendencia": ascendencia,
             "índice_de_tamaño": indice_de_tamano,
             "pariente_de": pariente_de,
             "gemelo_genético": gemelo_genetico,
             "valor_característica": valor_caracteristica,
             "min": minimo_estadistica,
             "max": maximo_estadistica,
             "prom": prom,
             "visualizar": visualizar}
