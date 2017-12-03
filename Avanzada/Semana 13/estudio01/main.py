import pickle
import json
import clases
import os

def leer_jugadores(archivo):
    jugadores = {}
    with open(archivo, 'r') as file:
        _jugadores = json.load(file)
        for k, v in values.items():
            _player = Player(k, None)
            _player.update(**v)
            jugadores[k] = _player
    return jugadores

def obtener_equipos():
    lista = os.listdir("db/equipos")
    equipos = []
    for path in lista:
        with open("db/equipos/" + path, "rb") as file:
            equipo = pickle.load(file)
            equipos.append(equipo)
    return equipos


class CustomEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, clases.Team):
            dicc_equipo = {}
            for jugador in o.jugadores:
                dicc_equipo.update({jugador.id: jugador.__dict__})
        return dicc_equipo


def equipos_a_json(equipos):
    for equipo in equipos:
        with open("db/equipos_arreglados/"+equipo.nombre+".json", "w") as file:
            json.dump(equipo, fp=file, cls=CustomEncoder, indent=4)


def show_all():
    all_players = []
    for path in os.listdir("db/equipos_arreglados"):
        with open("db/equipos_arreglados/"+path) as file:
            jugadores_equipo = json.load(file)
            for jugador in jugadores_equipo:
                all_players.append(jugadores_equipo[jugador])
    print("Faltas   Amarillas")
    for player in all_players:
        print("{0}  {1}   {2}   {3}   {4}".format(player["faltas"], player["amarillas"], player["goles"], player["rojas"], player["nombre"]))

def funcion(x):
    for k, value in x.items():
        print((k, value))
    return x



def main():
    #jugadores = leer_jugadores(archivo)
    pass


if __name__ == '__main__':
    equipos = obtener_equipos()
    equipos_a_json(equipos)
    show_all()
