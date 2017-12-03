from collections import deque, namedtuple
from random import expovariate, randint, seed


class Restaurant:

    def __init__(self, mesas, tiempo_simulacion, tasa_llegada):
        # Guardamos en atributos al tiempo actual y el máximo
        self.tiempo_actual = 0
        self.tiempo_maximo = tiempo_simulacion

        # generamos una lista con las mesas, las cuales van a tener un id único
        #  y 2 atributos:
        # "grupo", que almacenará al grupo y "comiendo" para ver si en esa mesa
        #  el grupo está comiendo
        self.mesas = [{"_id": i, "grupo": None, "comiendo": False} for i in
                      range(mesas)]

        # Creamos la cola que está inicialmente vacía
        self.cola = deque()

        # guardamos la tasa de llegada para ser utilizada después y generamos
        # altiro el tiempo de la próxima llegada
        self.tasa_llegada = tasa_llegada
        self.proximo_grupo_llega = expovariate(self.tasa_llegada)

        # Inicializamos las Estadísticas
        self.dinero_ganado = 0
        self.dinero_perdido = 0
        self.personas_abandono_fila = 0
        self.personas_abandono_mesa = 0
        self.personas_satisfechos = 0
        self.tiempo_espera_cola = list()
        self.tiempo_espera_pedido = list()

        self.grupos_terminan_cola = 0
        self.grupos_llega_pedido = 0

    @property
    def mesas_ocupadas(self):
        # Es útil poder tener acceso "fácil" a las mesas ocupadas. Esta es sólo
        #  utilizada internamente
        # Esto ayuda a que el código sea más entendible y no tener más de una
        # lista con las mesas
        return list(filter(lambda x: x["grupo"] is not None, self.mesas))

    @property
    def mesas_disponibles(self):
        # Es útil poder tener acceso "fácil" a las mesas libres
        return list(filter(lambda x: x["grupo"] is None, self.mesas))

    @property
    def mesas_esperando_pedido(self):
        # Esta property ayuda a obtener las mesas ocupadas pero que no estén
        # comiendo
        return list(filter(lambda x: not x["comiendo"], self.mesas_ocupadas))

    @property
    def mesas_comiendo(self):
        # Esta property ayuda a obtener las mesas ocupadas pero que están
        # comiendo
        return list(filter(lambda x: x["comiendo"], self.mesas_ocupadas))

    @property
    def proximo_grupo_abandona_cola(self):
        # Esta property nos entrega el próximo grupo que abandona la cola,
        # con su tiempo asociado
        # Retorna una tupla.. ojo!
        if len(self.cola) > 0:
            grupo = sorted(self.cola,
                           key=lambda x: x.tiempo_abandono_cola)[0]
            return (grupo, grupo.tiempo_abandono_cola)
        # Si no hay ningún grupo que esté esperando en la fila
        # retorna None con un tiempo infinito (para que no sea elegido)
        return (None, float("Inf"))

    @property
    def proximo_grupo_abandona_mesa(self):
        # Esta property nos entrega la mesa que será abandonada próxima,
        #  con su tiempo asociado
        if len(self.mesas_esperando_pedido) > 0:
            mesa = sorted(self.mesas_esperando_pedido,
                          key=lambda x: x["grupo"].tiempo_abandono_mesa)[0]
            return (mesa, mesa["grupo"].tiempo_abandono_mesa)
        # Si no hay ninguna mesa que esté esperando comida
        # retorna None con un tiempo infinito (para que no sea elegido)
        return (None, float("Inf"))

    @property
    def proximo_grupo_llega_pedido(self):
        # Esta property nos entrega próxima mesa que le llegará el pedido,
        #  con su tiempo asociado
        if len(self.mesas_esperando_pedido) > 0:
            mesa = sorted(self.mesas_esperando_pedido,
                          key=lambda x: x["grupo"].tiempo_preparacion_platos)[
                0]
            return (mesa, mesa["grupo"].tiempo_preparacion_platos)
        # Si no hay ninguna mesa que esté esperando comida
        # retorna None con un tiempo infinito (para que no sea elegido)
        return (None, float("Inf"))

    @property
    def proximo_grupo_termina_comer(self):
        # Esta la próxima mesa que terminará de comer, con su tiempo asociado
        if len(self.mesas_comiendo) > 0:
            mesa = sorted(self.mesas_comiendo,
                          key=lambda x: x["grupo"].tiempo_comer_plato)[0]
            return (mesa, mesa["grupo"].tiempo_comer_plato)
        # Si no hay ninguna mesa que esté comiendo
        # retorna None con un tiempo infinito (para que no sea elegido)
        return (None, float("Inf"))

    @property
    def proximo_evento(self):
        # Este método es muy importante. Nos retorna el evento que viene
        # después
        # A continuación tenemos una lista con los tiempos de todos los
        # posibles eventos
        tiempos = [self.proximo_grupo_llega,
                   self.proximo_grupo_abandona_cola[1],
                   self.proximo_grupo_abandona_mesa[1],
                   self.proximo_grupo_llega_pedido[1],
                   self.proximo_grupo_termina_comer[1]]
        print(tiempos)

        # Se elige el tiempo más pequeño, es decir, el tiempo del evento
        # que viene
        tiempo_prox_evento = min(tiempos)

        # Se chequea que no se pase del tiempo máximo. Esto puede ser un
        # "problema" de la simulación DES.
        if tiempo_prox_evento >= self.tiempo_maximo:
            return "fin"

        # Si no se ha pasado del tiempo, debemos ver a qué evento correspondía
        #  ese tiempo.
        # Para esto, tenemos una lista con strings que representan a los
        # eventos.
        eventos = ["llegada_grupo",
                   "abandono_cola",
                   "abandono_mesa",
                   "llegada_pedido",
                   "termino_comida"]

        # Retornamos el string que está en el mismo índice que el tiempo
        #  escogido, es decir, el evento correspondiente
        return eventos[tiempos.index(tiempo_prox_evento)]

    @property
    def promedio_llega_pedido(self):
        # Creamos esto para sacar las estadísticas.
        return sum(map(lambda x: x, self.tiempo_espera_pedido)) / len(
            self.tiempo_espera_pedido)

    @property
    def promedio_espera_cola(self):
        # Creamos esto para sacar las estadísticas.
        return sum(map(lambda x: x, self.tiempo_espera_cola)) / len(
            self.tiempo_espera_cola)

    def llegada_grupo(self):
        print('Ha llegado un grupo!')
        # Primero actualizamos el tiempo_actual al tiempo asociado a la llegada
        self.tiempo_actual = self.proximo_grupo_llega
        # Generamos el tiempo de la próxima llegada
        self.proximo_grupo_llega = self.tiempo_actual + expovariate(
            self.tasa_llegada)
        # Creamos el grupo
        grupo = Grupo(randint(2, 5), self.tiempo_actual)

        # Vemos si hay mesas disponibles
        if len(self.mesas_disponibles) > 0:
            # Si hay, se saca una y se le asigna este grupo
            mesa = self.mesas_disponibles[0]
            self.grupo_sienta_mesa(mesa, grupo)
            print('El grupo alcanzó una mesa y ha hecho su pedido')
        else:
            # Si no, se une a la cola y se genera el tiempo de abandono de
            #  los integrantes
            self.cola.append(grupo)
            grupo.generar_tiempo_abandono_cola(self.tiempo_actual)
            print(
                'No hay mesas disponibles, el grupo tendrá que esperar en la '
                'cola')

    def abandono_cola(self):
        # Primero obtenemos el grupo y su tiempo cuando abandonan la cola
        grupo, tiempo = self.proximo_grupo_abandona_cola
        # Actualizamos el tiempo_actual
        self.tiempo_actual = tiempo
        # Los sacamos de la cola
        self.cola.remove(grupo)

        # Registramos las personas que abandonan la cola para las estadísticas
        self.personas_abandono_fila += len(grupo)
        print('Un grupo se ha aburrido de esperar en la cola y se fue')

    def abandono_mesa(self):
        # Primero obtenemos la mesa y su tiempo cuando abandonan la mesa
        mesa, tiempo = self.proximo_grupo_abandona_mesa
        # Actualizamos el tiempo_actual
        self.tiempo_actual = tiempo
        # Guardamos al grupo que estaba en la mesa en una variable auxiliar
        # para sacar estadísticas
        grupo_abandona = mesa["grupo"]

        # Registramos las personas que abandonan la mesa para las estadísticas
        self.personas_abandono_mesa += len(grupo_abandona)
        print(
            'El grupo se aburrió de esperar el pedido y se ha ido de la mesa')
        print('Pérdida para el Restorán')

        # Registramos el dinero ganado por el grupo que termino de comer
        self.dinero_perdido += grupo_abandona.costo_total_platos

        # Ahora, cuando la mesa queda disponible, vemos si hay gente esperando
        if len(self.cola) > 0:
            # Si hay, el próximo grupo la utiliza
            print('La mesa ha quedado desocupada')
            grupo = self.cola.popleft()
            self.grupo_sienta_mesa(mesa, grupo)
        else:
            # Si no, la mesa queda disponible
            mesa["grupo"] = None
            print(
                'La mesa ha quedado desocupada, pero no hay nadie en la cola')

    def llegada_pedido(self):
        # Primero obtenemos la mesa y su tiempo cuando le llega el pedido
        mesa, tiempo = self.proximo_grupo_llega_pedido
        # Actualizamos el tiempo_actual
        self.tiempo_actual = tiempo
        # Ponemos que la mesa comenzó a comer
        mesa["comiendo"] = True
        # Generamos el tiempo en que termina de comer ese grupo
        mesa["grupo"].generar_tiempo_comer_plato(self.tiempo_actual)

        # Registramos para las estadísticas
        self.tiempo_espera_pedido.append(tiempo)
        print('Ha llegado un pedido a una mesa! El grupo comienza a comer')

    def termino_comida(self):
        # Primero obtenemos la mesa y su tiempo cuando termina de comer
        mesa, tiempo = self.proximo_grupo_termina_comer
        # Actualizamos el tiempo_actual
        self.tiempo_actual = tiempo
        # Guardamos al grupo que estaba en la mesa en una variable auxiliar
        # para sacar estadísticas
        grupo_abandona = mesa["grupo"]
        # Ponemos que la mesa ya no está comiendo
        mesa["comiendo"] = False

        # Registramos las personas satisfechas para las estadísticas
        self.personas_satisfechos += len(grupo_abandona)

        # Registramos el dinero ganado por el grupo que termino de comer
        self.dinero_ganado += grupo_abandona.costo_total_platos

        print(
            'Un grupo ha quedado satisfecho y ha pagado por su comida y se va')

        # Ahora, cuando la mesa queda disponible, vemos si hay gente esperando
        if len(self.cola) > 0:
            # Si hay, el próximo grupo la utiliza
            print('La mesa ha quedado desocupada')
            grupo = self.cola.popleft()
            self.grupo_sienta_mesa(mesa, grupo)
        else:
            # Si no, la mesa queda disponible
            mesa["grupo"] = None
            print(
                'La mesa ha quedado desocupada, porque no hay nadie en la '
                'cola')

    def grupo_sienta_mesa(self, mesa, grupo):
        # Como estas líneas de código se repiten mucho, creamos un método para
        # optimizar el código
        # Le asignamos a la mesa el grupo
        mesa["grupo"] = grupo
        # Generamos el tiempo de abandono de mesa del grupo
        grupo.generar_tiempo_abandono_mesa(self.tiempo_actual)

        # Creamos el pedido y se lo pasamos al grupo.
        # De esta manera se crea "por detrás" el tiempo de preparación de los
        # platos y su costo total
        pedido = Pedido(len(grupo))
        grupo.pedido = pedido

        # Guardamos los tiempos de espera en la cola para las estadísticas
        self.tiempo_espera_cola.append(
            self.tiempo_actual - grupo.tiempo_llegada)
        print('Ha llegado un grupo a la mesa')

    def run(self):

        # Aquí se pueden inicializar variables o cosas antes de que comience

        while self.tiempo_actual < self.tiempo_maximo:
            # Aquí ya estamos en plena simulación. Debemos ver cuál es el
            # próximo evento
            evento = self.proximo_evento

            # Una vez identificado el evento, debemos realizar las acciones
            # correspondientes
            if evento == "fin":
                self.tiempo_actual = self.tiempo_maximo
            elif evento == "llegada_grupo":
                self.llegada_grupo()
            elif evento == "abandono_cola":
                self.abandono_cola()
            elif evento == "abandono_mesa":
                self.abandono_mesa()
            elif evento == "llegada_pedido":
                self.llegada_pedido()
            elif evento == "termino_comida":
                self.termino_comida()

        # A esta altura ya terminó la simulación
        self.show_estadisticas()

    def show_estadisticas(self):
        # Imprimimos las estadísticas
        print("\n")
        print("-" * 50)
        print("Estadísticas:\n")
        print('Dinero ganado: ${}'.format(self.dinero_ganado))
        print('Pérdidas por platos no entregados: ${}'.format(
            self.dinero_perdido))
        print('Personas que se fueron por demora en el plato: {}'.format(
            self.personas_abandono_mesa))
        print('Personas se fueron por demora la fila: {}'.format(
            self.personas_abandono_fila))
        print('Personas satisfechas: {}'.format(self.personas_satisfechos))

        print('Promedio de espera en fila para recibir mesa: {}'.format(
            self.promedio_espera_cola))
        print('Tasa de espera promedio de los platos: {}'.format(
            self.promedio_llega_pedido))


class Persona:

    _id = 1

    def __init__(self):
        self.id = Persona._id
        Persona._id += 1

        self.tiempo_abandono_cola = None
        self.tiempo_abandono_mesa = None
        self.tiempo_comer_plato = None

    def generar_tiempo_abandono_cola(self, tiempo_actual):
        # Esto genera el tiempo de abandono de la cola (Uniforme entre 15 y 25)
        self.tiempo_abandono_cola = tiempo_actual + randint(15, 25)

    def generar_tiempo_abandono_mesa(self, tiempo_actual):
        # Esto genera el tiempo de abandono de la mesa (Uniforme entre 6 y 10)
        self.tiempo_abandono_mesa = tiempo_actual + randint(6, 10)

    def generar_tiempo_comer_plato(self, tiempo_actual):
        # Esto genera el tiempo que se demora en comer un plato (Uniforme
        # entre 20 y 30)
        self.tiempo_comer_plato = tiempo_actual + randint(20, 30)

    def __str__(self):
        # Ayuda a visualizar en caso de necesitarlo
        return "Persona {}".format(self._id)


class Pedido:

    def __init__(self, integrantes):
        # Generamos tantos pedidos como integrantes tiene el grupo
        self.platos = [Plato(randint(3500, 5600), randint(5, 8)) for _ in
                       range(integrantes)]

    @property
    def tiempo_preparacion(self):
        # El tiempo de preparación del plato que más se demora manda
        return max(map(lambda x: x.tiempo, self.platos))

    @property
    def costo_total(self):
        # El costo de los platos es la suma de todos.
        return sum(map(lambda x: x.precio, self.platos))


class Mesa:
    def __init__(self):
        pass


class Grupo:

    _id = 0

    def __init__(self, tamano, tiempo):
        # Le damos un id único a cada grupo para poder distinguirlos
        self._id = Grupo._id
        Grupo._id += 1
        # Al comienzo no tiene un pedido asociado
        self.pedido = None
        # Generamos las personas según el tamaño del grupo
        self.personas = list(map(lambda x: Persona(), range(tamano)))
        # Guardamos el tiempo de llegada en el grupo para las estadísticas
        self.tiempo_llegada = tiempo

    @property
    def tiempo_abandono_cola(self):
        # Cada persona tiene un tiempo de abandono. El más impaciente manda
        return min(map(lambda x: x.tiempo_abandono_cola, self.personas))

    @property
    def tiempo_abandono_mesa(self):
        # Cada persona tiene un tiempo de abandono. El más impaciente manda
        return min(map(lambda x: x.tiempo_abandono_mesa, self.personas))

    @property
    def tiempo_comer_plato(self):
        # Cada persona tiene un tiempo para comer su plato. El más lento manda
        return max(map(lambda x: x.tiempo_comer_plato, self.personas))

    @property
    def tiempo_preparacion_platos(self):
        # Esta property ayuda a manejar de forma más entendible a los pedidos
        # Ayuda a que la clase restorán sólo trabaje con los grupos y mesas
        return self.pedido.tiempo_preparacion

    @property
    def costo_total_platos(self):
        # Esta property ayuda a manejar de forma más entendible a los pedidos
        return self.pedido.costo_total

    def generar_tiempo_abandono_cola(self, tiempo_actual):
        # Debemos generarle a cada persona del grupo el tiempo asociado
        for persona in self.personas:
            persona.generar_tiempo_abandono_cola(tiempo_actual)

    def generar_tiempo_abandono_mesa(self, tiempo_actual):
        for persona in self.personas:
            persona.generar_tiempo_abandono_mesa(tiempo_actual)

    def generar_tiempo_comer_plato(self, tiempo_actual):
        for persona in self.personas:
            persona.generar_tiempo_comer_plato(tiempo_actual)

    def __len__(self):
        # Es útil poder obtener de manera simple la cantidad de integrantes
        #  del grupo
        # Esto es mejor que haber guardado un atributo "numero_integrantes"
        # porque es dinámico
        return len(self.personas)

    def __repr__(self):
        # Creamos una representación en caso de necesitarla
        return "Grupo {}".format(self._id)


Plato = namedtuple("Plato", ["precio", "tiempo"])

if __name__ == "__main__":
    restaurant = Restaurant(6, 50, 0.7)
    restaurant.run()
