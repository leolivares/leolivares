from collections import namedtuple
from functools import reduce
import random

Pais = namedtuple("Pais", ["sigla","nombre"])

Ciudad = namedtuple("Ciudad", ["sigla_pais","nombre"])

Persona = namedtuple("Persona", ["nombre", "apellido", "edad", "sexo", "ciudad", "profesion", "sueldo"])





# 1 Ciudades por pais
def ciudad_por_pais(nombre_pais, paises, ciudades):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param ciudades: lista de Ciudades (instancias)
    :return: generador
    '''

    s_pais = list(filter(lambda x: x.nombre == nombre_pais, paises))[0].sigla
    return filter(lambda x: x.sigla_pais == s_pais, ciudades)



# 2 Personas por pais
def personas_por_pais(nombre_pais, paises, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    ciudades_p = ciudad_por_pais(nombre_pais,paises,ciudades)
    set = {ciudad.nombre for ciudad in ciudades_p}

    return filter(lambda persona: persona.ciudad in set, personas)

# 3 Personas por ciudad
def personas_por_ciudad(nombre_ciudad, personas):
    '''
    filtramos a las personas por ciudad que queremos
    :param nombre_ciudad: str
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    return filter(lambda persona: persona.ciudad == nombre_ciudad, personas)


# 4 Personas con sueldo mayor a x
def personas_con_sueldo_mayor_a(personas, sueldo):
    '''
    :param personas: lista de Personas (instancias)
    :param sueldo: int
    :return: generador
    '''
    return filter(lambda persona: int(persona.sueldo) > sueldo, personas)



# 5 Personas ciudad y sexo dado
def personas_por_ciudad_sexo(nombre_ciudad, sexo, personas):
    '''
    :param nombre_ciudad: str
    :param sexo: str
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    return filter(lambda persona: persona.sexo == sexo,filter(lambda persona: persona.ciudad == nombre_ciudad, personas))


# 6 Personas por pais sexo y profesion
def personas_por_pais_sexo_profesion(nombre_pais, paises, sexo, profesion,
                                     ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param sexo: str
    :param profesion: str
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: generador
    '''
    ciudades_p = ciudad_por_pais(nombre_pais, paises, ciudades)
    set = {ciudad.nombre for ciudad in ciudades_p}

    return filter(lambda persona : persona.profesion == profesion,
                     filter(lambda persona: persona.sexo == sexo,filter(lambda persona: persona.ciudad in set, personas)))




# 7 Sueldo promedio mundo
def sueldo_promedio(personas):
    '''
    :param personas: lista de Personas (lista de instancias)
    :return: promedio (int o float)
    '''

    return reduce(lambda x,y: x+y, map(lambda persona: float(persona.sueldo), personas)) / len(personas)


# 8 Sueldo promedio de una ciudad x
def sueldo_ciudad(nombre_ciudad, personas):
    '''
    :param nombre_ciudad: str
    :param personas: lista de Personas (instancias)
    :return: promedio (int o float)
    '''

    per = list(filter(lambda persona: persona.ciudad == nombre_ciudad, personas))

    return reduce(lambda x,y : x+y ,map(lambda persona: float(persona.sueldo), per)) / len(per)




# 9 Sueldo promedio de un pais x
def sueldo_pais(nombre_pais, paises, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: promedio (int o float)
    '''
    ciudades_p = ciudad_por_pais(nombre_pais, paises, ciudades)
    set = {ciudad.nombre for ciudad in ciudades_p}
    persons = list(filter(lambda persona: persona.ciudad in set, personas))

    return reduce(lambda x,y: x+y ,map(lambda persona: float(persona.sueldo), persons)) / len(persons)



# 10 Sueldo promedio de un pais y profesion x
def sueldo_pais_profesion(nombre_pais, paises, profesion, ciudades, personas):
    '''
    :param nombre_pais: str
    :param paises: lista de Paises (instancias)
    :param profesion: str
    :param ciudades: lista de Ciudades (instancias)
    :param personas: lista de Personas (instancias)
    :return: promedio (int o float)
    '''
    ciudades_p = ciudad_por_pais(nombre_pais, paises, ciudades)
    set = {ciudad.nombre for ciudad in ciudades_p}

    persons = list(filter(lambda persona: persona.profesion == profesion,filter(lambda persona: persona.ciudad in set, personas)))

    return reduce(lambda x,y: x+y ,map(lambda persona: float(persona.sueldo), persons)) / len(persons)


if __name__ == '__main__':

    parser = lambda x: x.strip().split(",")

    """Abra los archivos y guarde en listas las instancias; paises, ciudades,
    personas"""
    with open('Ciudades.txt', 'r', encoding="utf-8") as file1:
        ciudades = [Ciudad(*parser(line)) for line in file1 ]

    with open('Informacion_personas.txt', 'r', encoding="utf-8") as file2:
        personas = [Persona(*parser(line)) for line in file2]

    with open('Paises.txt', 'r', encoding="utf-8") as file3:
        paises = [Pais(*parser(line)) for line in file3]



    """NO DEBE MODIFICAR CODIGO DESDE EL PUNTO (1) AL (10).
    EN (11) y (12) DEBEN ESCRIBIR SUS RESPUESTAS RESPECTIVAS."""

    #  (1) Ciudades en Chile
    ciudades_chile = ciudad_por_pais('Chile', paises, ciudades)
    count = 0
    for ciudad in ciudades_chile:
        print(ciudad.sigla_pais, ciudad.nombre)
        count += 1
        if count == 10:
            break

    # (2) Personas en Chile
    personas_chile = personas_por_pais('Chile', paises, ciudades, personas)
    count = 0
    for p in personas_chile:
        print(p.nombre, p.ciudad)
        count += 1
        if count == 10:
            break

    # (3) Personas en Osorno, Chile
    personas_stgo = personas_por_ciudad('Osorno', personas)
    for p in personas_stgo:
        print(p.nombre, p.ciudad)

    # (4) Personas en el mundo con sueldo mayor a 600
    p_sueldo_mayor_600 = personas_con_sueldo_mayor_a(personas, 600)
    count = 0
    for p in p_sueldo_mayor_600:
        print(p.nombre, p.sueldo)
        count += 1
        if count == 10:
            break

    # (5) Personas en ViñaDelMar, Chile de sexo femenino
    pxcs = personas_por_ciudad_sexo('ViñaDelMar', 'Femenino', personas)
    for p in pxcs:
        print(p.nombre, p.ciudad, p.sexo)

    # (6) Personas en Chile de sexo masculino y area Medica
    pxpsp = personas_por_pais_sexo_profesion('Chile', paises, 'Masculino',
                                             'Medica', ciudades, personas)
    for p in pxpsp:
        print(p.nombre, p.sexo, p.profesion)

    # (7) Sueldo promedio de personas del mundo
    sueldo_mundo = sueldo_promedio(personas)
    print('Sueldo promedio: ', sueldo_mundo)

    # (8) Sueldo promedio Osorno, Chile
    sueldo_santiago = sueldo_ciudad('Osorno', personas)
    print('Sueldo Osorno: ', sueldo_santiago)

    # (9) Sueldo promedio Chile
    sueldo_chile = sueldo_pais('Chile', paises, ciudades, personas)
    print('Sueldo Chile: ', sueldo_chile)

    # (10) Sueldo promedio Chile de un estudiante
    sueldo_chile_estudiantes = \
        sueldo_pais_profesion('Chile', paises, 'Estudiante', ciudades,
                              personas)
    print('Sueldo estudiantes Chile: ', sueldo_chile_estudiantes)

    # (11) Muestre a los 10 Chilenos con mejor sueldo con un indice de orden
    # desde 0.

    def top_sueldos(personas,pais) :

        per = personas_por_pais(pais, paises, ciudades, personas)

        sueldos = sorted(per, key= lambda persona: persona.sueldo, reverse=True)[:10]

        for i, sueldo in enumerate(sueldos) :
            print(i, sueldo.nombre, sueldo.sueldo)

    top_sueldos(personas,"Chile")



    # (12) Se pide seleccionar 10 personas al azar y generar tuplas con sus:
    # nombres, apellidos y sueldos.

    def seleccion_al_azar(personas) :

        persons = [x for x in personas]

        azar = random.sample(persons,10)

        variables = ["Nombre", "Apellido", "Sueldo"]
        p1 = [x.nombre for x in azar]
        p2 = [x.apellido for x in azar]
        p3 = [x.sueldo for x in azar]

        info = []
        for a in p1 ,p2, p3 :
            infor = zip(variables, p)
            info.append(dict(infor))

        print(info)


    seleccion_al_azar(personas)

