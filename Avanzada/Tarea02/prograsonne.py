import grafo
import lista as ls
import gui
import sys
from random import choice
import random



class Prograsonne(gui.GameInterface) :

    def __init__(self,turno=None):
        self.graph = grafo.Grafo()
        self.historial = ls.Lista()
        self.partida_actual = ls.Lista()
        self._turno = turno
        self.piezas = ls.Lista()
        self.pieza_actual = None
        self.cerradas = ls.Lista()
        self.abiertas = ls.Lista()
        self.puntos_red = 0
        self.puntos_blue = 0

    @property
    def turno(self):
        return self._turno

    @turno.setter
    def turno(self,value):
        if value == "red" or value == "blue" :
            self._turno = value
        else :
            print("Este no es un turno posible.")

    # Crea y Guarda en las EDD a las piezas
    def obtener_piezas(self):
        archivo = open("pieces.csv","r")
        lineas = archivo.readlines()
        archivo.close()
        listas_legales = ls.Lista()
        for linea in lineas :
            linea = linea.strip().split(",")
            lista_legal = ls.Lista()
            for dato in linea :
                lista_legal.append(dato)
            listas_legales.append(lista_legal)

        for lista_legal in listas_legales :
            nodo = lista_legal.valor[1]
            cant = int(nodo.valor)
            nodo2 = lista_legal.valor[0]
            tipo = nodo2.valor
            while cant > 0 :
                pieza = grafo.Pieza(tipo)
                self.piezas.append(pieza)
                cant -= 1

    # Realiza la primera jugada al azar del juego
    def situacion_inicial(self):
        self.obtener_piezas()
        pieza = self.elegir_pieza()
        self.pieza_actual = pieza
        i, j, col = self.coordenadas_random()
        self.turno = col
        pieza.color = self.turno
        pieza.pertenece_a = self.turno
        gui.nueva_pieza(self.turno,pieza.tipo_permanente)
        gui.add_piece(i,j)
        pieza.i = i
        pieza.j = j
        self.partida_actual.append(pieza)
        self.graph.agregar_pieza(pieza)
        self.cambiar_turno()

        nueva = self.elegir_pieza()
        nueva.color = self.turno
        nueva.pertenece_a = self.turno
        self.pieza_actual = nueva
        gui.nueva_pieza(self.turno,nueva.tipo_permanente)

        self.calcular_puntaje()

    # Retorna coordenadas al azar
    def coordenadas_random(self):
        i = random.randint(0,7)
        j = random.randint(0,7)
        color = ls.Lista()
        color.append("red")
        color.append("blue")
        c = random.randint(0,1)
        col = color[c].valor
        self.turno = col
        return i , j , col

    # Cambia de turno
    def cambiar_turno(self):
        if self.turno == "red" :
            self.turno = "blue"
        else :
            self.turno = "red"

    # Elige y retorna una pieza dispnible al azar
    def elegir_pieza(self):
        num = len(self.piezas) - 1
        n = random.randint(0,num)
        pieza = self.piezas[n].valor
        return pieza

    def run(self):
        def hook(type, value, traceback):
            print(type)
            print(value)
            print(traceback)

        sys.__excepthook__ = hook


        gui.set_scale(False)  # Any float different from 0
        gui.init()
        gui.set_quality("ultra")  # low, medium, high ultra
        gui.set_animations(False)
        gui.set_game_interface(Prograsonne())  # GUI Listener
        gui.init_grid()
        gui.run()

    #Retorna las coordenadas adyacentes a una posicion en especifico
    def obtener_adyacentes(self,i,j):
        adyacentes = ls.Lista()
        lista1 = ls.Lista()
        lista2 = ls.Lista()
        lista3 = ls.Lista()
        lista4 = ls.Lista()
        lista5 = ls.Lista()
        lista6 = ls.Lista()
        if j == 0 or j % 2 == 0 :
            lista1.append(i - 1)
            lista1.append(j)
            lista2.append(i)
            lista2.append(j + 1)
            lista3.append(i + 1)
            lista3.append(j + 1)
            lista4.append(i + 1)
            lista4.append(j)
            lista5.append(i + 1)
            lista5.append(j - 1)
            lista6.append(i)
            lista6.append(j - 1)
        else :
            lista1.append(i - 1)
            lista1.append(j)
            lista2.append(i - 1)
            lista2.append(j + 1)
            lista3.append(i)
            lista3.append(j + 1)
            lista4.append(i + 1)
            lista4.append(j)
            lista5.append(i)
            lista5.append(j - 1)
            lista6.append(i - 1)
            lista6.append(j - 1)

        adyacentes.append(lista1)
        adyacentes.append(lista2)
        adyacentes.append(lista3)
        adyacentes.append(lista4)
        adyacentes.append(lista5)
        adyacentes.append(lista6)
        return adyacentes

    # Verifica que la jugada sea posible
    def verificar_jugada(self,i,j):
        adyacentes = self.obtener_adyacentes(i,j)
        n = 0
        m = 3

        existe_pieza_adyacente = False
        permiso = True

        for ad in adyacentes :

            if permiso :

                if m == 6 :
                    m = 0

                pieza = self.graph.buscar_pieza(ad.valor[0].valor,ad.valor[1].valor)
                if pieza and pieza.color :

                    existe_pieza_adyacente = True

                    if pieza.tipo[m] != self.pieza_actual.tipo[n] :
                        permiso = False

            n += 1
            m += 1

        permiso_final = False
        if existe_pieza_adyacente and permiso :
            permiso_final =True
            self.pieza_actual.i = i
            self.pieza_actual.j = j

        return permiso_final

    def colocar_pieza(self, i, j):
        print("Presionaste" , i , j)

        if len(self.piezas) == 0 :
            print("Las piezas se han acabado")
            self.terminar_juego()

        else :

            if not self.graph.raiz :
                self.cambiar_turno()
                return True

            else :
                permiso = self.verificar_jugada(i, j)

                if permiso :
                    gui.add_piece(i,j)

                    existent = self.graph.buscar_pieza(i,j)
                    if existent :
                        self.partida_actual = self.partida_actual.remove(existent)


                    self.partida_actual.append(self.pieza_actual)
                    self.piezas = self.piezas.remove(self.pieza_actual)
                    self.devolver_grafo()
                    self.cambiar_turno()
                    color = self.turno

                    self.calcular_puntaje(self.pieza_actual)

                    pieza = self.elegir_pieza()
                    pieza.color = self.turno
                    pieza.pertenece_a = self.turno
                    self.pieza_actual = pieza
                    gui.nueva_pieza(color,pieza.tipo_permanente)

                    return True

    # Rota la pieza y el string que la representa
    def rotar_pieza(self, orientation):
        tipo = self.pieza_actual.tipo
        ultima = tipo[-1]
        resto = tipo[:-1]
        rotada = ultima + resto
        self.pieza_actual.tipo = rotada


    #Retrocede la ultima jugada pertenciente a un jugador, si es posible
    def retroceder(self):
        print("Presionaste retroceder")


        color = self.turno
        num = len(self.partida_actual) - 1
        nodo = self.partida_actual[num].valor

        seguir = True
        logrado = False


        while seguir :

            if nodo == self.partida_actual[0].valor :
                seguir = False
                logrado = False

            elif nodo.color == color :
                logrado = True
                gui.pop_piece(nodo.i,nodo.j)
                nodo.color = None

                seguir = False

                nueva = self.elegir_pieza()
                self.cambiar_turno()
                gui.nueva_pieza(self.turno,nueva.tipo_permanente)
                self.pieza_actual = nueva
                nueva.color = self.turno
                nueva.pertenece_a = self.turno

            num = num - 1
            nodo = self.partida_actual[num].valor

        if logrado :
            self.calcular_puntaje()

        if not logrado :
            print("No se puede retroceder bajo estas circunstancias!")


    # Revisaa si los segmentos de Ciudad de una pieza estan cerrados
    def revisar_cerrada(self,pieza):

        adyacentes = self.obtener_adyacentes(pieza.i,pieza.j)
        cerrada = True
        cantidad = 0
        cumplen = 0
        conex = ls.Lista()

        i = 0
        for ad in adyacentes :

            if pieza.tipo[i] == "C" :

                cantidad += 1

                if ad.valor[0].valor < 0 or ad.valor[1].valor < 0 :

                    cumplen += 1

                elif ad.valor[0].valor > 7 or ad.valor[1].valor > 7 :

                    cumplen += 1

                else :

                    union = self.graph.buscar_pieza(ad.valor[0].valor, ad.valor[1].valor)
                    if not union or not union.color:
                        cerrada = False
                    else :
                        cumplen += 1
                        conex.append(union)

            i += 1

        if cantidad == cumplen :
            cerrada = True
        else :
            cerrada = False

        return cerrada , conex

    # Calcula el puntaje en base a las piezas en el tablero
    def calcular_puntaje(self, pieza_jugada=None):

        ciudades_abiertas = ls.Lista()
        ciudades_cerradas = ls.Lista()
        puntos_red = 0
        puntos_blue = 0


        revisar = ls.Lista()
        revisadas = ls.Lista()


        for p in self.partida_actual :
            revisada = False
            for q in revisadas :

                if p.valor.i == q.valor.i and p.valor.j == q.valor.j :
                    revisada = True

            if not revisada and p.valor.color:
                revisar.append(p.valor)


            if len(revisar) != 0 :

                cerrada = False

                cant = 0
                posibles = ls.Lista()
                while len(revisar) != 0 :

                    for pieza in revisar :

                        if "C" in pieza.valor.tipo and pieza.valor.color:

                            cant += 1

                            cerrada , conexas = self.revisar_cerrada(pieza.valor)

                            revisadas.append(pieza.valor)
                            revisar = revisar.remove(pieza.valor)

                            posibles.append(pieza.valor)


                            if cerrada :

                                for c in conexas :
                                    revisada = False

                                    for rev in revisadas :

                                        if rev.valor.i == c.valor.i and rev.valor.j == c.valor.j :
                                            revisada = True

                                    if not revisada and c.valor.color:
                                        revisar.append(c.valor)

                        else :

                            revisar = revisar.remove(pieza.valor)
                            revisadas.append(pieza.valor)

                if cerrada :

                    if pieza_jugada :

                        plot_twist = False

                        for m in posibles :

                            ciudades_cerradas.append(m.valor)

                            if m.valor.i == pieza_jugada.i and m.valor.j == pieza_jugada.j :
                                plot_twist = True


                        if plot_twist :

                            for m in posibles:
                                m.valor.pertenece_a = pieza_jugada.pertenece_a

                            if pieza_jugada.pertenece_a == "red":
                                puntos_red += len(posibles) * 30
                                puntos_red += 40
                                gui.set_points(1, puntos_red)
                            elif pieza_jugada.pertenece_a == "blue":
                                puntos_blue += len(posibles) * 30
                                puntos_blue += 40
                                gui.set_points(2, puntos_blue)

                            for p in self.partida_actual:
                                if p.valor.color:
                                    gui.pop_piece(p.valor.i, p.valor.j)

                            for p in self.partida_actual:
                                if p.valor.color:
                                    gui.nueva_pieza(p.valor.pertenece_a, p.valor.tipo_permanente)

                                    pieza_actual = self.pieza_actual
                                    perma = p.valor.tipo_permanente
                                    tipo = p.valor.tipo

                                    self.pieza_actual = p.valor

                                    self.pieza_actual.tipo_permanente = tipo
                                    self.pieza_actual.tipo = perma

                                    while self.pieza_actual.tipo != self.pieza_actual.tipo_permanente:
                                        gui.rotate_piece()

                                    gui.add_piece(p.valor.i, p.valor.j)

                                    self.pieza_actual.tipo_permanente = perma
                                    self.pieza_actual.tipo = tipo

                    else :

                        piece = posibles[0].valor.color

                        if piece == "red":
                            puntos_red += len(posibles) * 30
                            puntos_red += 40
                            gui.set_points(1, puntos_red)
                        elif piece == "blue":
                            puntos_blue += len(posibles) * 30
                            puntos_blue += 40
                            gui.set_points(2, puntos_blue)


                elif not cerrada :

                    for posible in posibles :

                        ciudades_abiertas.append(posible.valor)

                        if posible.valor.pertenece_a == "red" :
                            puntos_red += 10
                            gui.set_points(1, puntos_red)
                        elif posible.valor.pertenece_a == "blue" :
                            puntos_blue += 10
                            gui.set_points(2, puntos_blue)


        caminos_cerrados = ls.Lista()
        revisar = ls.Lista()
        revisadas = ls.Lista()

        for cerrada in ciudades_cerradas :
            ciudad = cerrada.valor

            revisada = False
            for re in revisadas :
                if re.valor.i == ciudad.i and re.valor.j == ciudad.j :
                    revisada = True

            if not revisada :
                revisar.append(ciudad)

            while len(revisar) != 0 :

                ciudad = revisar[0].valor

                if "P" in ciudad.tipo and ciudad.color :

                    adyacentes = self.obtener_adyacentes(ciudad.i,ciudad.j)

                    i = 0
                    for ad in adyacentes :

                        pieza = self.graph.buscar_pieza(ad.valor[0].valor,ad.valor[1].valor)

                        if pieza and pieza.color and ciudad.tipo[i] == "P" :

                            revi = False
                            for pi in revisadas :

                                if pi.valor.i == pieza.i and pi.valor.j == pieza.j :
                                    revi = True

                            caminos_cerrados.append(pieza)

                            if not revi:
                                revisar.append(pieza)

                        i += 1

                revisar = revisar.remove(ciudad)
                revisadas.append(ciudad)


        for camino in caminos_cerrados :

            adyacentes = self.obtener_adyacentes(camino.valor.i,camino.valor.j)

            for ad in adyacentes :

                grilla = False
                con_cerrada = False

                if ad.valor[0].valor > 7 or ad.valor[1].valor > 7 :
                    grilla = True
                    color = ciudades_cerradas[0].valor.color
                    if color == "blue":
                        puntos_blue += 10
                    elif color == "red":
                        puntos_red += 10

                elif ad.valor[0].valor < 0 or ad.valor[1].valor < 0 :
                    grilla = True
                    color = ciudades_cerradas[0].valor.color
                    if color == "blue":
                        puntos_blue += 10
                    elif color == "red":
                        puntos_red += 10

                else :

                    pieza = self.graph.buscar_pieza(ad.valor[0].valor,ad.valor[1].valor)

                    for piece in ciudades_cerradas :
                        if pieza.i == piece.valor.i and pieza.j == piece.valor.j :
                            con_cerrada = True
                            color = ciudades_cerradas[0].valor.color
                            if color == "blue":
                                puntos_blue += 30
                            elif color == "red":
                                puntos_red += 30

                if grilla :
                    color = ciudades_cerradas[0].valor.color
                    if color == "blue" :
                        puntos_blue += 20
                    elif color == "red" :
                        puntos_red += 20

                elif con_cerrada :
                    color = ciudades_cerradas[0].valor.color
                    if color == "blue":
                        puntos_blue += 50
                    elif color == "red":
                        puntos_red += 50

        self.puntos_red = puntos_red
        self.puntos_blue = puntos_blue

    # Informa quien es el ganador de la partida
    def terminar_juego(self):
        print("Presionaste terminar juego")
        self.piezas = ls.Lista()
        self.calcular_puntaje()
        if self.puntos_red > self.puntos_blue :
            print("----------------------------------------")
            print("El ganador es el Jugador 1 (red)" "\n"
                  "Puntos Jugador 1: {}\n"
                  "Puntos Jugador 2: {}".format(self.puntos_red,self.puntos_blue))
            print("----------------------------------------")
        elif self.puntos_blue > self.puntos_red :
            print("----------------------------------------")
            print("El ganador es el Jugador 2 (blue)" "\n"
                  "Puntos Jugador 1: {}\n"
                  "Puntos Jugador 2: {}".format(self.puntos_red, self.puntos_blue))
            print("----------------------------------------")
        else :
            print("----------------------------------------")
            print("Empate!")
            print("----------------------------------------")

    #Muestra una posible jugada en la interfaz
    def hint_asked(self):

        seguir = True

        while seguir:

            for pieza in self.partida_actual :

                if seguir:

                    jugada_valida = True

                    adyacentes = self.obtener_adyacentes(pieza.valor.i,pieza.valor.j)

                    for ad in adyacentes :

                        jugada_valida = True

                        if seguir :

                            piece = self.graph.buscar_pieza(ad.valor[0].valor,ad.valor[1].valor)

                            if not piece :

                                adya = self.obtener_adyacentes(ad.valor[0].valor,ad.valor[1].valor)

                                n = 0
                                m = 3

                                for i in range(6) :

                                    if m == 6 :
                                        m = 0

                                    pi = self.graph.buscar_pieza(adya[i].valor[0].valor,adya[i].valor[1].valor)

                                    if pi and pi.color :

                                        if self.pieza_actual.tipo[n] != pi.tipo[m] :
                                            jugada_valida = False

                                    n += 1
                                    m += 1

                                if jugada_valida :

                                    if ad.valor[0].valor < 0 or ad.valor[1].valor < 0 :
                                        jugada_valida = False

                                    elif ad.valor[0].valor > 7 or ad.valor[1].valor > 7 :
                                        jugada_valida = False

                                    else :
                                        gui.add_hint(ad.valor[0].valor,ad.valor[1].valor)
                                        seguir = False

            if not jugada_valida :
                print("En esa posicion no hay jugadas posibles")
                seguir = False

    #Devuelve la partida a un estado previamente guardado
    def click_number(self, number):

        volver_a = self.historial[int(number)-1]
        anterior = volver_a.valor
        actual = self.partida_actual

        iguales = True
        if len(anterior) == len(actual) :
            i = 0
            for p in anterior :
                if p.valor.tipo != actual[i].valor.tipo or p.valor.i != actual[i].valor.i or p.valor.j != actual[i].valor.j :
                    iguales = False
                if p.valor.color != actual[i].valor.color :
                    iguales = False
                i += 1

        else :
            iguales = False

        if not iguales :

            for p in actual:
                if p.valor.color :
                    gui.pop_piece(p.valor.i,p.valor.j)

            for p in anterior:
                if p.valor.color:
                    gui.nueva_pieza(p.valor.pertenece_a, p.valor.tipo_permanente)

                    act = p.valor.tipo
                    guardar_pieza = self.pieza_actual
                    perma = p.valor.tipo_permanente

                    self.pieza_actual = p.valor
                    p.valor.tipo = perma
                    p.valor.tipo_permanente = act
                    while p.valor.tipo != p.valor.tipo_permanente :
                        gui.rotate_piece()

                    p.valor.tipo = act
                    p.valor.tipo_permanente = perma

                    gui.add_piece(p.valor.i, p.valor.j)

            nueva_pieza = self.elegir_pieza()
            nueva_pieza.color = self.turno
            nueva_pieza.pertenece_a = self.turno
            self.pieza_actual = nueva_pieza
            gui.nueva_pieza(self.turno,nueva_pieza.tipo_permanente)



            self.devolver_historial(number)
            self.devolver_grafo()

            self.calcular_puntaje()

    # Devuelve el historial al estado en que se encontraba cuando se guardo la partida
    def devolver_historial(self,number):

        n = int(number) - 1
        i = 0
        lista_n = ls.Lista()

        for p in self.historial[n].valor :
            pieza = grafo.Pieza(p.valor.tipo_permanente,p.valor.i,p.valor.j,p.valor.color)
            pieza.pertenece_a = p.valor.pertenece_a
            pieza.tipo = p.valor.tipo
            pieza.id = p.valor.id
            lista_n.append(pieza)
        self.partida_actual = lista_n



        lista = ls.Lista()
        while i <= n :
            lista.append(self.historial[i].valor)
            i += 1
        m = len(self.historial)
        self.historial = lista

        i = 0
        m = m - int(number)
        while i < m :
            gui.pop_number()
            i += 1

    # Modifica el grafo segun las piezas de la partida actual
    def devolver_grafo(self):
        nuevo_grafo = grafo.Grafo()

        for p in self.partida_actual :
            p.valor.conexiones = ls.Lista()

            if not nuevo_grafo.raiz :
                nuevo_grafo.agregar_pieza(p.valor)

            else :
                adyacentes = self.obtener_adyacentes(p.valor.i,p.valor.j)
                for ad in adyacentes :
                    pieza = nuevo_grafo.buscar_pieza(ad.valor[0].valor,ad.valor[1].valor)
                    if pieza :
                        nuevo_grafo.agregar_pieza(p.valor,pieza)

            self.graph = nuevo_grafo


    # Guarda la partida actual para permitir ser posteriormente recuperada
    def guardar_juego(self):

        numero = len(self.historial) + 1

        gui.add_number(numero, self.turno)
        print("Presionaron guardar")
        lista = ls.Lista()
        for p in self.partida_actual :
            act = p.valor
            nueva_pieza = grafo.Pieza(act.tipo_permanente,act.i,act.j,act.color)
            nueva_pieza.pertenece_a = act.pertenece_a
            nueva_pieza.tipo = p.valor.tipo
            nueva_pieza.id = act.id
            lista.append(nueva_pieza)


        i = 0
        for act in self.partida_actual :

            conexiones = act.valor.conexiones

            for conexion in conexiones :

                for p in lista :

                    if conexion.valor.i == p.valor.i and conexion.valor.j == p.valor.j :

                        lista[i].valor.conexiones.append(p.valor)

            i += 1

        self.historial.append(lista)


if __name__ == "__main__" :
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)


    sys.__excepthook__ = hook
    progra = Prograsonne()
    gui.set_scale(False)  # Any float different from 0
    gui.init()
    gui.set_quality("ultra")  # low, medium, high ultra
    gui.set_animations(False)
    gui.set_game_interface(progra)  # GUI Listener
    gui.init_grid()
    progra.situacion_inicial()
    gui.run()