from random import uniform, randint, expovariate, choice

# Estos parametros son algunos de los definidos en el enunciado.
WEIGHT_FACTOR = 1000  # se usa para sacar B
MAX_PERSON_SPEED = 3
MIN_PERSON_SPEED = 1
MAX_PERSON_WEIGHT = 200
MIN_PERSON_WEIGHT = 40

ANIMAL_SPAWN_MIN = 160
ANIMAL_SPAWN_MAX = 200
ANIMAL_RANGE = 90

PEOPLE = 500

MAX_SIMULATION_TIME = 10000
SIMULATIONS = 20


class Zoologico:

    def __init__(self, tiempo_maximo):
        self.tiempo_actual = 0
        self.tiempo_maximo = tiempo_maximo
        self.tasa_aparicion = 1 / randint(160, 200)
        self.tiempo_aparicion = expovariate(self.tasa_aparicion)


        self.especies = {"Leon": [0.2, 0.9, 0.6],
                         "Hipopotamo": [0.01, 0.95, 0.8],
                         "Yeti": [0.4, 0.1, 0.5],"Panda Rojo": [0.8, 1, 0.05]}


        self.personas = [Person() for _ in range(500)]
        self.animales = list()

        self.sobrevivientes = list()
        self.num_victi = {"Leon": 0, "Hipopotamo": 0, "Yeti": 0,
                          "Panda Rojo": 0}
        self.tiempo_prom = 0


    def proximo_evento(self):
        resultados = [self.tiempo_aparicion,
                        self.proximo_ataque,
                        self.salvarse]

        tiempos = [resultados[0],
                   resultados[1][1],
                   resultados[2][1]]


        tiempo_prox_evento = min(tiempos)


        if tiempo_prox_evento >= self.tiempo_maximo:
            return "fin"

        eventos = ["aparicion", "ataque", "se salva"]
        evento = eventos[tiempos.index(tiempo_prox_evento)]

        if evento == "aparicion":
            return (evento, (None, resultados[0]))
        elif evento == "ataque":
            return (evento, resultados[1])
        else:
            return (evento, resultados[2])


    @property
    def proximo_ataque(self):
        if len(self.animales) != 0:
            tiempos = [(animal, animal.prox_tiempo_ataque)
                       for animal in self.animales]
            tiempos = sorted(tiempos, key=lambda x: x[1])[0]
            return tiempos
        return (None, float("Inf"))

    @property
    def salvarse(self):
        tiempos = [(persona, persona.tiempo_salvarse)
                   for persona in self.personas]
        tiempos = sorted(tiempos, key=lambda x: x[1])[0]
        if tiempos[1] == 0.0:
            tiempos = (tiempos[0], float("Inf"))
        return tiempos

    def aparicion_animal(self):
        especie = choice(["Leon", "Hipopotamo", "Yeti", "Panda Rojo"])
        prob = self.especies[especie]
        self.animales.append(Animal(prob[0], prob[1], prob[2], especie))
        print("[SPAWN] Aparecio un {}".format(especie))

    def atacar(self, animal):
        opciones = list(filter(lambda x: animal.puede_atacar(x), self.personas))
        persona = choice(opciones)

        probabilidad_ataque = animal.prob_ataque * persona.coef
        if persona.sex == "M":
            probabilidad_ataque *= randint(1, 3)

        num = randint(0, 100) / 100
        if num <= probabilidad_ataque:
            print(
                "[ATAQUE] Persona siendo atacada por {}".format(animal.especie))
            num_escape = randint(0, 100) / 100
            if num_escape <= animal.prob_escape_ataque:
                print("[ESCAPE] Persona escapo de {}".format(animal.especie))
            else:
                num_sobrevivir = randint(0, 100) / 100
                if num_sobrevivir <= animal.prob_letal:
                    persona.is_dead = True
                    self.num_victi[animal.especie] += 1
                    print(
                        "[MUERTO] Persona murio debido a ataque de {}".format(
                            animal.especie))
                else:
                    print("Persona sobrevivio a ataque de {}".format(
                        animal.especie))

    def moverse(self, tiempo):
        for persona in self.personas:
            if not persona.is_dead and persona.pos_actual < 100:
                persona.pos_actual += persona.velocity * tiempo


    def run(self):

        while self.tiempo_actual < self.tiempo_maximo:

            evento = self.proximo_evento()

            if evento == "fin":
                self.tiempo_actual = self.tiempo_maximo

            elif evento[0] == "aparicion":
                self.aparicion_animal()

            elif evento[0] == "ataque":
                self.atacar(evento[1][0])

            elif evento[0] == "se salva":
                evento[1][0].has_survived()


            self.tiempo_actual += evento[1][1]
            self.moverse(evento[1][1])

        print("Estadisticas")
        print("Victimas por especie: {}".format(self.num_victi))



# Pueden modificar y crear las clases que se les antoje.
class Animal:
    # Identificador unico para cada animal.
    # No tiene niguna utilidad mas que para probar el programa
    id = 0

    def __init__(self, prob_ataque, prob_letal, prob_escape_ataque, especie):
        self.especie = especie
        self.prob_ataque = prob_ataque
        self.prob_escape_ataque = prob_escape_ataque
        self.prob_letal = prob_letal
        self.kills = 0
        self.pos_actual = randint(0, 100)
        self.tasa_ataque = 1 / randint(2, 6)
        self.prox_tiempo_ataque = expovariate(self.tasa_ataque)

    def puede_atacar(self, persona):
        # Retorna True si la persona esta dentro del rango de ataque
        if abs(persona.pos_actual - self.pos_actual) <= 90:
            return True
        return False


    def __str__(self):
        pass


class Person:
    def __init__(self):
        self.pos_inicial = randint(0, 100)  # km
        self.pos_actual = self.pos_inicial
        self.sex = choice(["M", "F"])
        self.weight = uniform(40, 200)
        self.safe = False
        self.is_dead = False

        if self.sex == "M":
            self.coef = self.weight * randint(1, 3) / WEIGHT_FACTOR
        else:
            self.coef = self.weight / WEIGHT_FACTOR

        self.velocity = randint(MIN_PERSON_SPEED, MAX_PERSON_SPEED) * self.coef

    @property
    def tiempo_salvarse(self):
        distancia = 100 - self.pos_actual
        return distancia / self.velocity

    def has_survived(self):
        # Retorna True si la persona esta en un km mayor a 100
        if self.pos_actual > 100:
            print("[SAFE] Persona de sexo {} se salvo!".format(self.sex))
            return True
        return False

    def move(self, dist):
        # Metodo para avanzar
        self.pos_actual += dist



if __name__ == "__main__":
    zoo = Zoologico(10000)
    zoo.run()