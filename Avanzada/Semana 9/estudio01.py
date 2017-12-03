from random import expovariate, randint, choice


class CalleLarga:

    def __init__(self, tiempo_maximo):
        self.tasa = 1 / randint(4, 10)
        self.genera_replica = expovariate(self.tasa)
        self.tiempo_maximo = tiempo_maximo
        self.tiempo_actual = 0
        self.personas = [self.crear_persona() for _ in range(100)]
        self.vehiculos = [Vehiculo(choice(["Auto", "Camioneta"]))
                                   for _ in range(25)]
        self.asignar_vehiculos()

        # Estadisticas

        self.base_vehiculo = 0
        self.base_pie = 0
        self.base_generoso = 0
        self.base_egoista = 0
        self.vic_tsunami = 0
        self.vic_replica = 0

    def personas_total(self):
        return self.base_pie + self.base_vehiculo + self.vic_replica + self.vic_tsunami

    def crear_persona(self):
        personalidad = choice(["Generoso", "Egoista"])
        if personalidad == "Generoso":
            persona = Persona("Generoso")
        else:
            persona = Persona("Egoista")
        return persona


    def asignar_vehiculos(self):
        vehiculos = self.vehiculos[:]
        while len(vehiculos) != 0:
            num = randint(0, 100)
            if self.personas[num].vehiculo is None:
                self.personas[num].vehiculo = vehiculos[0]
                vehiculos[0].dueño = self.personas[num]
                vehiculos.pop(0)


    def genera_replica(self):
        print("Se genero una replica!")
        replica = Replica()
        self.observar_daños(replica)


    def tiempo_a_base(self, persona):
        if persona.vehiculo:
            tiempo = (100 - persona.punto) / persona.vehiculo.rapidez
        else:
            tiempo = (100 - persona.punto) / persona.rapidez
        return tiempo



    def proximo_evento(self):
        eventos = {"Replica", "Base"}
        tiempos = [self.genera_replica,
                   self.]

    def run(self):

        while self.tiempo_actual < self.tiempo_maximo and \
                        self.personas_total != 100:

            evento = self.proximo_evento()


class Replica:

    def __init__(self):
        self.tsunami = None
        num = randint(0, 100)/100
        if num <= 0.7:
            self.intensidad = "Debil"
        else:
            self.intensidad = "Fuerte"
        tsu = randint(0, 100)
        if tsu >= 70:
            self.tsunami = Tsunami()


class Tsunami:

    def __init__(self):
        self.potencia = randint(3, 8)
        self.centro = randint(0, 100)

    @property
     def alcance(self):
        return self.potencia * 4



class Persona:

    def __init__(self, personalidad):
        self.personalidad = personalidad
        self.rapidez = randint(5, 8)
        self.punto = randint(0, 60)
        self.vehiculo = None


class Vehiculo:

    tipos = {"Auto": 5, "Camioneta": 8}

    def __init__(self, tipo):
        self.tipo = tipo
        self.capacidad = Vehiculo.tipos[tipo]
        self.rapidez = randint(12, 60)
        self.cantidad_actual = 0
        self.dueño = None
        self.personas = list()

    def agregar_persona(self, persona):
        if self.cantidad_actual < self.capacidad:
            self.personas.append(persona)
            self.cantidad_actual += 1



if __name__ == "__main__":
    calle = CalleLarga(50)
    for per in calle.personas:
        print(per.vehiculo)
        calle.tiempo_a_base(per)
