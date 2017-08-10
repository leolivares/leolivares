#Estoy optando por el bonus. 
#La manera en que le di inteligencia al jugador, fue definiendo una nueva
#llamada "Computador". Dentro de esta clase, defini varios metodos destinados
#al analisis de los posibles movimientos. Cada metodo definido en la clase se
#tendra una explicacion con comentarios, pero de manera general, el criterio
#que seleccione para realizar las jugadas fue el siguiente :

#En el turno de el jugador no humano, la ficha a mover sera aquella que este
#mas encerrada, con el fin de que se traslade a un espacio con mas celdas proximas
#mayor o igual de libres. En el caso de que varias fichas tengan el mismo numero de
#casillas libres alrededor, se selecciona al azar cualquiera de ellas y se busca una
#mejor posicion.

#Para la seleccion del lanzamiento, se buscan las casillas que esten dentro de la linea
#de fuego de la ficha, y que a la vez esten proximas a una ficha enemiga. Si existen varias
#posibilidades de disparo, se elige disparar a la ficha enemiga que tenga menos celdas vecinas
#libres, con el fin de darle prioridad a encerrar a las fichas enemigas.
#En caso de no tener niguna opcion cerca de alguna ficha enemiga, se selecciona
#una casilla dentro de las posibilidades al azar.

#Inclui un modo de juego entre computadoras para observar su comportamiento de manera mas detallada.



#Codificamos las clases a utilizar

import random
import time

class Tablero :
    def __init__(self) :
        self.tablero = [[],[],[],[]]
        self.lineas = [["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "],["   ","   ","   ","   ","   ","   ","   ","   ","   ","   "]]

    def nuevo_tablero(self) :
        nueva_lista = [["a4" , "d1" , "g1" , "j4"],["a7" , "d10" , "g10" , "j7"],[],[1]]
        return nueva_lista
    
    def cargar_tablero(self) :
        abierto = open("tablero.txt")
        lista = abierto.readlines()
        abierto.close()
        lista_limpia = []
        for linea in lista :
            lista_limpia.append([linea.strip()])
        nueva_lista = []
        for lista in lista_limpia :
            for linea in lista :
                nueva_lista += [linea.split(",")]
        return nueva_lista

    def guardar_tablero(self) :
        abierto = open("tablero.txt","w")
        for lista in self.tablero :
            msg = ""
            for item in lista :
                msg += str(item) + ","
            a = msg.strip(",")
            print(a,file=abierto)
        abierto.close()

    def quitar_fichas(self) :
        for lista in self.lineas :
            n = 0
            while n < len(lista) :
                if lista[n] == " X " :
                    lista[n] = "   "
                elif lista[n] == " 0 " :
                    lista[n] = "   "
                n += 1

    def traducir(self,celda) :
        colum = celda[:1]
        fila = celda[1:]

        if colum == "0" :
            letra = "a"
        elif colum == "1" :
            letra = "b"
        elif colum == "2" :
            letra = "c"
        elif colum == "3" :
            letra = "d"
        elif colum == "4" :
            letra = "e"
        elif colum == "5" :
            letra = "f"
        elif colum == "6" :
            letra = "g"
        elif colum == "7" :
            letra = "h"
        elif colum == "8" :
            letra = "i"
        elif colum == "9" :
            letra = "j"

        fila = str(int(fila)+1)

        final = letra + fila
        return final

    
    def analizar_tablero(self) :
        for celda in self.tablero[0] :
            inicio_letra = celda[:1]
            num = int(celda[1:]) - 1
            if inicio_letra == "a" :
                letra = 0
            elif inicio_letra == "b" :
                letra = 1
            elif inicio_letra == "c" :
                letra = 2
            elif inicio_letra == "d" :
                letra = 3
            elif inicio_letra == "e" :
                letra = 4
            elif inicio_letra == "f" :
                letra = 5
            elif inicio_letra == "g" :
                letra = 6
            elif inicio_letra == "h" :
                letra = 7
            elif inicio_letra == "i" :
                letra = 8
            elif inicio_letra == "j" :
                letra = 9

            self.lineas[num][letra] = " 0 "

        for celda in self.tablero[1] :
            inicio_letra = celda[:1]
            num = int(celda[1:]) - 1

            if inicio_letra == "a" :
                letra = 0
            elif inicio_letra == "b" :
                letra = 1
            elif inicio_letra == "c" :
                letra = 2
            elif inicio_letra == "d" :
                letra = 3
            elif inicio_letra == "e" :
                letra = 4
            elif inicio_letra == "f" :
                letra = 5
            elif inicio_letra == "g" :
                letra = 6
            elif inicio_letra == "h" :
                letra = 7
            elif inicio_letra == "i" :
                letra = 8
            elif inicio_letra == "j" :
                letra = 9

            self.lineas[num][letra] = " X "

        if self.tablero[2] != [] :
            for celda in self.tablero[2] :
                inicio_letra = celda[:1]
                num = int(celda[1:]) - 1

                if inicio_letra == "a" :
                    letra = 0
                elif inicio_letra == "b" :
                    letra = 1
                elif inicio_letra == "c" :
                    letra = 2
                elif inicio_letra == "d" :
                    letra = 3
                elif inicio_letra == "e" :
                    letra = 4
                elif inicio_letra == "f" :
                    letra = 5
                elif inicio_letra == "g" :
                    letra = 6
                elif inicio_letra == "h" :
                    letra = 7
                elif inicio_letra == "i" :
                    letra = 8
                elif inicio_letra == "j" :
                    letra = 9

                self.lineas[num][letra] = " * "
        
    def quedan_movimientos(self,celda) :
        celda_letra = celda[:1]
        celda_numero = int(celda[1:])-1
        if celda_letra == "a" :
            letra = 0
        elif celda_letra == "b" :
            letra = 1
        elif celda_letra == "c" :
            letra = 2
        elif celda_letra == "d" :
            letra = 3
        elif celda_letra == "e" :
            letra = 4
        elif celda_letra == "f" :
            letra = 5
        elif celda_letra == "g" :
            letra = 6
        elif celda_letra == "h" :
            letra = 7
        elif celda_letra== "i" :
            letra = 8
        elif celda_letra == "j" :
            letra = 9
            
        horizontales = False
        verticales = False
        diagonales = False

        #Horizontal
        i = letra
        if ((i+1) <= 9 and self.lineas[celda_numero][i+1] == "   ") or ((i-1) >= 0 and self.lineas[celda_numero][i-1] == "   ") :
            horizontales = True

        #Verticales
        i = celda_numero
        if ((i+1) <= 9 and self.lineas[i+1][letra] == "   ") or ((i-1) >= 0 and self.lineas[i-1][letra] == "   ") :
            verticales = True

        #Diagonal_izq_sup
        i = letra
        j = celda_numero
        if ((j+1) <= 9 and (i-1) >= 0 and self.lineas[j+1][i-1] == "   ") or ((j+1) <= 9 and (i+1) <= 9 and self.lineas[j+1][i+1] == "   ") or ((j-1) >= 0 and (i-1) >= 0 and self.lineas[j-1][i-1] == "   ") or ((j-1) >= 0 and (i+1) <= 9 and self.lineas[j-1][i+1] == "   ") :
            diagonales = True
        
        #Verificar alguna posibilidad de movimiento para la celda
        posibilidad = False
        if (horizontales or verticales or diagonales) :
            posibilidad = True
            
        return posibilidad
        

    def perdedor(self,jugador) :
        cont = 0
        perdedor = False
        for j in jugador.posiciones :
            a = self.quedan_movimientos(j)
            if a :
                cont += 1
        if cont == 0 :
            perdedor = True
        return perdedor
    
    def movimiento_valido(self,inicio,fin,jugador) :
        inicio_letra = inicio[:1]
        inicio_num = int(inicio[1:]) - 1
        fin_letra = fin[:1]
        fin_num = int(fin[1:]) - 1

        if inicio_letra == "a" :
            letra = 0
        elif inicio_letra == "b" :
            letra = 1
        elif inicio_letra == "c" :
            letra = 2
        elif inicio_letra == "d" :
            letra = 3
        elif inicio_letra == "e" :
            letra = 4
        elif inicio_letra == "f" :
            letra = 5
        elif inicio_letra == "g" :
            letra = 6
        elif inicio_letra == "h" :
            letra = 7
        elif inicio_letra == "i" :
            letra = 8
        elif inicio_letra == "j" :
            letra = 9
        else :
            letra = int(inicio_letra)
            
        if fin_letra == "a" :
            letraf = 0
        elif fin_letra == "b" :
            letraf = 1
        elif fin_letra == "c" :
            letraf = 2
        elif fin_letra == "d" :
            letraf = 3
        elif fin_letra == "e" :
            letraf = 4
        elif fin_letra == "f" :
            letraf = 5
        elif fin_letra == "g" :
            letraf = 6
        elif fin_letra == "h" :
            letraf = 7
        elif fin_letra == "i" :
            letraf = 8
        elif fin_letra == "j" :
            letraf = 9
        else :
            letraf = int(fin_letra)

        posibilidades = []
        
        #Horizontales
        i = letra
        while (i+1) <= 9 and self.lineas[inicio_num][i+1] == "   " :
            i += 1
            posibilidades += [str(i) + str(inicio_num)]
        i = letra
        while (i-1) >= 0 and self.lineas[inicio_num][i-1] == "   " :
            i -= 1
            posibilidades += [str(i) + str(inicio_num)]

        #Verticales
        i = inicio_num
        while (i+1) <= 9 and self.lineas[i+1][letra] == "   " :
            i+=1
            posibilidades += [str(letra) + str(i)]
        i = inicio_num
        while (i-1) >= 0 and self.lineas[i-1][letra] == "   " :
            i-=1
            posibilidades += [str(letra) + str(i)]

        #Diagonales
        i = inicio_num
        j = letra
        while (i+1) <= 9 and (j+1) <= 9 and self.lineas[i+1][j+1] == "   " :
            i+=1
            j+=1
            posibilidades += [str(j) + str(i)]
        i = inicio_num
        j = letra
        while (i+1) <= 9 and (j-1) >= 0 and self.lineas[i+1][j-1] == "   " :
            i+=1
            j-=1
            posibilidades += [str(j) + str(i)]
        i = inicio_num
        j = letra
        while (i-1) >= 0 and (j+1) <= 9 and self.lineas[i-1][j+1] == "   " :
            i-=1
            j+=1
            posibilidades += [str(j) + str(i)]
        i = inicio_num
        j = letra
        while (i-1) >= 0 and (j-1) >= 0 and self.lineas[i-1][j-1] == "   " :
            i-=1
            j-=1
            posibilidades += [str(j) + str(i)]
                
        if not jugador.humano :
            return posibilidades
        else:
            valido = True
            if self.lineas[inicio_num][letra] != jug.ficha  :
                valido = False
                print("La celda de inicio no contine una de tus fichas")
            elif letra == letraf and inicio_num == fin_num :
                valido = False
                print("Tu ficha esta en esa posicion!")
            elif (str(letraf)+str(fin_num)) not in posibilidades :
                valido = False
                print("Esa ficha no se puede mover a esa celda")
            elif not (self.lineas[fin_num][letraf] == "   ") :
                valido = False
                if self.lineas[fin_num][letra] == " X " or self.lineas[fin_num][letra] == " 0 " :
                    objeto = "ficha"
                else :
                    objeto = "flecha"
                print("Esa posicion esta ocupada por una" , objeto)
            else :
                print("   ")
                print("Movimiento Valido!")
                print("   ")
                valido = True
            return valido

    def lanzamiento_valido(self,fin,lanza,jugador) :
        fin_letra = fin[:1]
        fin_num = int(fin[1:]) - 1
        lanza_letra = lanza[:1]
        lanza_num = int(lanza[1:]) - 1

        if fin_letra == "a" :
            letraf = 0
        elif fin_letra == "b" :
            letraf = 1
        elif fin_letra == "c" :
            letraf = 2
        elif fin_letra == "d" :
            letraf = 3
        elif fin_letra == "e" :
            letraf = 4
        elif fin_letra == "f" :
            letraf = 5
        elif fin_letra == "g" :
            letraf = 6
        elif fin_letra == "h" :
            letraf = 7
        elif fin_letra == "i" :
            letraf = 8
        elif fin_letra == "j" :
            letraf = 9

        if lanza_letra == "a" :
            letra = 0
        elif lanza_letra == "b" :
            letra = 1
        elif lanza_letra == "c" :
            letra = 2
        elif lanza_letra == "d" :
            letra = 3
        elif lanza_letra == "e" :
            letra = 4
        elif lanza_letra == "f" :
            letra = 5
        elif lanza_letra == "g" :
            letra = 6
        elif lanza_letra == "h" :
            letra = 7
        elif lanza_letra == "i" :
            letra = 8
        elif lanza_letra == "j" :
            letra = 9

        posibilidades = []
        #Horizontales
        i = letraf
        while (i+1) <= 9 and self.lineas[fin_num][i+1] == "   " :
            i += 1
            posibilidades += [str(i) + str(fin_num)]
        i = letraf
        while (i-1) >= 0 and self.lineas[fin_num][i-1] == "   " :
            i -= 1
            posibilidades += [str(i) + str(fin_num)]

        #Verticales
        i = fin_num
        while (i+1) <= 9 and self.lineas[i+1][letraf] == "   " :
            i+=1
            posibilidades += [str(letraf) + str(i)]
        i = fin_num
        while (i-1) >= 0 and self.lineas[i-1][letraf] == "   " :
            i-=1
            posibilidades += [str(letraf) + str(i)]

        #Diagonales
        i = fin_num
        j = letraf
        while (i+1) <= 9 and (j+1) <= 9 and self.lineas[i+1][j+1] == "   " :
            i+=1
            j+=1
            posibilidades += [str(j) + str(i)]
        i = fin_num
        j = letraf
        while (i+1) <= 9 and (j-1) >= 0 and self.lineas[i+1][j-1] == "   " :
            i+=1
            j-=1
            posibilidades += [str(j) + str(i)]
        i = fin_num
        j = letraf
        while (i-1) >= 0 and (j+1) <= 9 and self.lineas[i-1][j+1] == "   " :
            i-=1
            j+=1
            posibilidades += [str(j) + str(i)]
        i = fin_num
        j = letraf
        while (i-1) >= 0 and (j-1) >= 0 and self.lineas[i-1][j-1] == "   " :
            i-=1
            j-=1
            posibilidades += [str(j) + str(i)]
        
        
        valido = True
        if fin_letra == lanza_letra and fin_num == lanza_num :
            valido = False
            print("No puedes lanzar una flecha en la celda en la que estas!")
        elif (str(letra)+str(lanza_num)) not in posibilidades :
            print("Esta celda no esta dentro de la linea de ataque de la amazona")
            valido = False
        else :
            valido = True
            print("   ")
            print("Lanzamiento Valido!")
            print("   ")
        return valido
        

        

    def __str__(self) : #Este metodo seria igual a la funcion tablero_to_string()
        principal = "  | a | b | c | d | e | f | g | h | i | j |" + "\n"
        fijo = "  +---+---+---+---+---+---+---+---+---+---+" + "\n"
        linea10 = "10|"+self.lineas[9][0]+"|"+self.lineas[9][1]+"|"+self.lineas[9][2]+"|"+self.lineas[9][3]+"|"+self.lineas[9][4]+"|"+self.lineas[9][5]+"|"+self.lineas[9][6]+"|"+self.lineas[9][7]+"|"+self.lineas[9][8]+"|"+self.lineas[9][9]+"|"
        linea9 = " 9|"+self.lineas[8][0]+"|"+self.lineas[8][1]+"|"+self.lineas[8][2]+"|"+self.lineas[8][3]+"|"+self.lineas[8][4]+"|"+self.lineas[8][5]+"|"+self.lineas[8][6]+"|"+self.lineas[8][7]+"|"+self.lineas[8][8]+"|"+self.lineas[8][9]+"|"
        linea8 = " 8|"+self.lineas[7][0]+"|"+self.lineas[7][1]+"|"+self.lineas[7][2]+"|"+self.lineas[7][3]+"|"+self.lineas[7][4]+"|"+self.lineas[7][5]+"|"+self.lineas[7][6]+"|"+self.lineas[7][7]+"|"+self.lineas[7][8]+"|"+self.lineas[7][9]+"|"
        linea7 = " 7|"+self.lineas[6][0]+"|"+self.lineas[6][1]+"|"+self.lineas[6][2]+"|"+self.lineas[6][3]+"|"+self.lineas[6][4]+"|"+self.lineas[6][5]+"|"+self.lineas[6][6]+"|"+self.lineas[6][7]+"|"+self.lineas[6][8]+"|"+self.lineas[6][9]+"|"
        linea6 = " 6|"+self.lineas[5][0]+"|"+self.lineas[5][1]+"|"+self.lineas[5][2]+"|"+self.lineas[5][3]+"|"+self.lineas[5][4]+"|"+self.lineas[5][5]+"|"+self.lineas[5][6]+"|"+self.lineas[5][7]+"|"+self.lineas[5][8]+"|"+self.lineas[5][9]+"|"
        linea5 = " 5|"+self.lineas[4][0]+"|"+self.lineas[4][1]+"|"+self.lineas[4][2]+"|"+self.lineas[4][3]+"|"+self.lineas[4][4]+"|"+self.lineas[4][5]+"|"+self.lineas[4][6]+"|"+self.lineas[4][7]+"|"+self.lineas[4][8]+"|"+self.lineas[4][9]+"|"
        linea4 = " 4|"+self.lineas[3][0]+"|"+self.lineas[3][1]+"|"+self.lineas[3][2]+"|"+self.lineas[3][3]+"|"+self.lineas[3][4]+"|"+self.lineas[3][5]+"|"+self.lineas[3][6]+"|"+self.lineas[3][7]+"|"+self.lineas[3][8]+"|"+self.lineas[3][9]+"|"
        linea3 = " 3|"+self.lineas[2][0]+"|"+self.lineas[2][1]+"|"+self.lineas[2][2]+"|"+self.lineas[2][3]+"|"+self.lineas[2][4]+"|"+self.lineas[2][5]+"|"+self.lineas[2][6]+"|"+self.lineas[2][7]+"|"+self.lineas[2][8]+"|"+self.lineas[2][9]+"|"
        linea2 = " 2|"+self.lineas[1][0]+"|"+self.lineas[1][1]+"|"+self.lineas[1][2]+"|"+self.lineas[1][3]+"|"+self.lineas[1][4]+"|"+self.lineas[1][5]+"|"+self.lineas[1][6]+"|"+self.lineas[1][7]+"|"+self.lineas[1][8]+"|"+self.lineas[1][9]+"|"
        linea1 = " 1|"+self.lineas[0][0]+"|"+self.lineas[0][1]+"|"+self.lineas[0][2]+"|"+self.lineas[0][3]+"|"+self.lineas[0][4]+"|"+self.lineas[0][5]+"|"+self.lineas[0][6]+"|"+self.lineas[0][7]+"|"+self.lineas[0][8]+"|"+self.lineas[0][9]+"|"
        tts = principal + fijo + linea10 + "\n" + fijo + linea9 + "\n" + fijo + linea8 + "\n" + fijo + linea7 + "\n" + fijo + linea6 + "\n" + fijo + linea5 + "\n" + fijo + linea4 + "\n" + fijo + linea3 + "\n" + fijo + linea2 + "\n" + fijo + linea1 + "\n" + fijo + " 0 Jugador 1 - X Jugador2 - * Flecha" 
        return tts
        

class Jugador :
    def __init__(self,nombre,numero,ficha) :
        self.nombre = nombre
        self.numero = numero
        self.ficha = ficha
        self.posiciones = []
        self.humano = True

    def agregar_posiciones(self,posiciones) :
        for p in posiciones :
            self.posiciones += [p]

class Computador :
    def __init__(self,nombre,numero,ficha) :
        self.nombre = nombre
        self.numero = numero
        self.ficha = ficha
        self.posiciones = []
        self.humano = False

    def agregar_posiciones(self,posiciones) :
        for p in posiciones :
            self.posiciones += [p]

    def casillas_abiertas(self,celda,tab) :
        #Este metodo cuenta las casillas abiertas cercanas a una celda
        celda_letra = celda[:1]
        celda_num = int(celda[1:])-1

        if celda_letra == "a" :
            letra = 0
        elif celda_letra == "b" :
            letra = 1
        elif celda_letra == "c" :
            letra = 2
        elif celda_letra == "d" :
            letra = 3
        elif celda_letra == "e" :
            letra = 4
        elif celda_letra == "f" :
            letra = 5
        elif celda_letra == "g" :
            letra = 6
        elif celda_letra == "h" :
            letra = 7
        elif celda_letra == "i" :
            letra = 8
        elif celda_letra == "j" :
            letra = 9
        else :
            letra = int(celda_letra)
        
        cont = 0
        #Horizontal
        i = letra
        if ((i+1) <= 9 and tab.lineas[celda_num][i+1] == "   ") :
            cont += 1
        if ((i-1) >= 0 and tab.lineas[celda_num][i-1] == "   ") :
            cont += 1
        #Verticales
        i = celda_num
        if ((i+1) <= 9 and tab.lineas[i+1][letra] == "   ") :
            cont += 1
        if ((i-1) >= 0 and tab.lineas[i-1][letra] == "   ") :
            cont += 1
            
        #Diagonal_izq_sup
        i = letra
        j = celda_num
        if ((j+1) <= 9 and (i-1) >= 0 and tab.lineas[j+1][i-1] == "   ") :
            cont += 1
        if ((j+1) <= 9 and (i+1) <= 9 and tab.lineas[j+1][i+1] == "   ") :
            cont += 1
        if ((j-1) >= 0 and (i-1) >= 0 and tab.lineas[j-1][i-1] == "   ") :
            cont += 1
        if ((j-1) >= 0 and (i+1) <= 9 and tab.lineas[j-1][i+1] == "   ") :
            cont += 1
        return cont
           
    def celda_a_mover(self,tab) :
        #Este metodo analiza las fichas dej jugador no humano, y selecciona
        #aquella que tenga menos casillas abiertas cercanas, con el fin de moverla
        #a un mejor lugar
        abiertas = []
        menor = 100
        igual = 150000000
        res = []
        for celda in self.posiciones :
            if tab.quedan_movimientos(celda) :
                a = self.casillas_abiertas(celda,tab)
                if a <= menor :
                    if a == igual :
                        abiertas += [celda]
                    else :
                        abiertas = [celda]
                        igual = a
                    menor = a
                else :
                    res += [celda]
        if len(abiertas) != 0 :           
            t = random.randint(0,len(abiertas)-1)
            mover = abiertas[t]
        else :
            t = random.randint(0,len(res)-1)
            mover = res[t]
        return mover

    def posibilidades(self,inicio,tab) :
        #Este metodo, dada una celda, retorna una lista con las posibilidades de
        #movimiento o lanzamiento.
        inicio_letra = inicio[:1]
        inicio_num = int(inicio[1:]) - 1

        if inicio_letra == "a" :
            letra = 0
        elif inicio_letra == "b" :
            letra = 1
        elif inicio_letra == "c" :
            letra = 2
        elif inicio_letra == "d" :
            letra = 3
        elif inicio_letra == "e" :
            letra = 4
        elif inicio_letra == "f" :
            letra = 5
        elif inicio_letra == "g" :
            letra = 6
        elif inicio_letra == "h" :
            letra = 7
        elif inicio_letra == "i" :
            letra = 8
        elif inicio_letra == "j" :
            letra = 9

        posibilidades = []
        #Horizontales
        i = letra
        while (i+1) <= 9 and tab.lineas[inicio_num][i+1] == "   " :
            i += 1
            posibilidades += [str(i) + str(inicio_num)]
        i = letra
        while (i-1) >= 0 and tab.lineas[inicio_num][i-1] == "   " :
            i -= 1
            posibilidades += [str(i) + str(inicio_num)]

        #Verticales
        i = inicio_num
        while (i+1) <= 9 and tab.lineas[i+1][letra] == "   " :
            i+=1
            posibilidades += [str(letra) + str(i)]
        i = inicio_num
        while (i-1) >= 0 and tab.lineas[i-1][letra] == "   " :
            i-=1
            posibilidades += [str(letra) + str(i)]

        #Diagonales
        i = inicio_num
        j = letra
        while (i+1) <= 9 and (j+1) <= 9 and tab.lineas[i+1][j+1] == "   " :
            i+=1
            j+=1
            posibilidades += [str(j) + str(i)]
        i = inicio_num
        j = letra
        while (i+1) <= 9 and (j-1) >= 0 and tab.lineas[i+1][j-1] == "   " :
            i+=1
            j-=1
            posibilidades += [str(j) + str(i)]
        i = inicio_num
        j = letra
        while (i-1) >= 0 and (j+1) <= 9 and tab.lineas[i-1][j+1] == "   " :
            i-=1
            j+=1
            posibilidades += [str(j) + str(i)]
        i = inicio_num
        j = letra
        while (i-1) >= 0 and (j-1) >= 0 and tab.lineas[i-1][j-1] == "   " :
            i-=1
            j-=1
            posibilidades += [str(j) + str(i)]
        return posibilidades

    def analizar_movimiento(self,posibilidades,celda_inicial,tab) :
        #Este metodo, dada ua lista de posibilidades de movimiento, devuelve la
        #celda a la cual es mas conveniente mover la ficha, segun el numero
        #de casillas abiertas de cada una de las posibilidades
        abiertas = []
        mayor = -10000000
        igual = 150000000
        a = self.casillas_abiertas(celda_inicial,tab)
        residuo = []
        for celda in posibilidades :
            b = self.casillas_abiertas(celda,tab)
            if b >= a :
                if b == igual :
                    abiertas += [celda]
                else :
                    abiertas = [celda]
                    igual = b
                a = b
            else :
                residuo += [celda]

        if len(abiertas) != 0 :               
            t = random.randint(0,len(abiertas)-1)
            mover = abiertas[t]
        else :
            t = random.randint(0,len(residuo)-1)
            mover = residuo[t]
        return mover
        

    def analizar_lanzamiento(self,posibilidad,jug,tab) :
        #Este metodo, dada una lista de posibilidades de lanzamientos, retorna
        #una celda a la cual es mas favorable lanzar la flecha, segun
        #la proximidad a una ficha enemiga, y dandole preferencias a
        #aquellas fichas enemigas con menos casillas abiertas cercanas.
        menor = 1000000000000
        total = []
        for celda in jug.posiciones :
            posibilidades = []
            cont = 0
            celda_letra = celda[:1]
            celda_num = int(celda[1:])-1
            if celda_letra == "a" :
                letra = 0
            elif celda_letra == "b" :
                letra = 1
            elif celda_letra == "c" :
                letra = 2
            elif celda_letra == "d" :
                letra = 3
            elif celda_letra == "e" :
                letra = 4
            elif celda_letra == "f" :
                letra = 5
            elif celda_letra == "g" :
                letra = 6
            elif celda_letra == "h" :
                letra = 7
            elif celda_letra == "i" :
                letra = 8
            elif celda_letra == "j" :
                letra = 9

            #Horizontal
            i = letra
            if ((i+1) <= 9 and tab.lineas[celda_num][i+1] == "   ") :
                posibilidades += [str(i+1)+str(celda_num)]
                cont += 1
            if ((i-1) >= 0 and tab.lineas[celda_num][i-1] == "   ") :
                cont += 1
                posibilidades += [str(i-1)+str(celda_num)]
            #Verticales
            i = celda_num
            if ((i+1) <= 9 and tab.lineas[i+1][letra] == "   ") :
                cont+=1
                posibilidades += [str(letra)+str(i+1)]
            if ((i-1) >= 0 and tab.lineas[i-1][letra] == "   ") :
                cont+=1
                posibilidades += [str(letra)+str(i-1)]
                
            #Diagonal_izq_sup
            i = letra
            j = celda_num
            if ((j+1) <= 9 and (i-1) >= 0 and tab.lineas[j+1][i-1] == "   ") :
                cont+=1
                posibilidades += [str(i-1)+str(j+1)]
            if ((j+1) <= 9 and (i+1) <= 9 and tab.lineas[j+1][i+1] == "   ") :
                posibilidades += [str(i+1)+str(j+1)]
                cont+=1
            if ((j-1) >= 0 and (i-1) >= 0 and tab.lineas[j-1][i-1] == "   ") :
                posibilidades += [str(i-1)+str(j-1)]
                cont+=1
            if ((j-1) >= 0 and (i+1) <= 9 and tab.lineas[j-1][i+1] == "   ") :
                posibilidades += [str(i+1)+str(j-1)]
                cont+=1

            if cont < menor :
                especifico = []
                especifico += posibilidades

            total += posibilidades

        esp = []
        for casilla in posibilidad :
            if casilla in especifico :
                esp += [casilla]
        t = []
        for casilla in posibilidad :
            if (casilla in total) and (casilla not in esp):
                t += [casilla]
        if len(esp) != 0 :
            a = random.randint(0,len(esp)-1)
            lanzar = esp[a]
        elif len(t) != 0 :
            b = random.randint(0,len(t)-1)
            lanzar = t[b]
        else :
            c = random.randint(0,len(posibilidad)-1)
            lanzar = posibilidad[c]

        return lanzar
        

#Codigo Principal


print("""Bienvenido a AMAZONAS!! Las reglas del juego son simples:
Gana el jugador que continue con posibles movimientos, es decir,
pierde un jugador si en su turno ya no puede realizar un movimiento.

Un movimiento esta formado por dos partes:
    1.- Selecciona la celda de la ficha que deseas mover, y luego
    selecciona la celda a la cual la deseas mover.
    2.- Una vez que la ficha se mueva, debes seleccionar una celda a
    la cual lanzar una flecha.
    
*Las fichas se mueven en cualquier direccion , en linea recta y la cantidad
de casillas que se desee, siempre y cuando este dentro de el tablero.
(Similar a una reina de ajedrez)
*Solo podras mover una ficha o lanzar una flecha a una celda que este
vacia, y solo si la trayectoria hacia esa celda esta despejada.
*Si lo deseas, antes de empezar el movimiento, puedes guardar la partida y
continuar, o guardarla y salirte , para continuar despues.
*Si un jugador se rinde, automaticamente el otro sera el ganador.""")

print("   ")
print("""1. Jugar con un amigo
2. Jugar contra computadora
3. Batalla de Computadoras""")
print("   ")
res = int(input("Selecciona un modo de juego: "))
if res == 1 :
    print("   ")
    nombre1 = input("Ingresa el nombre del Jugador 1: ")
    nombre2 = input("Ingresa el nombre del Jugador 2: ")
    jug1 = Jugador(nombre1,1," 0 ")
    jug2 = Jugador(nombre2,2," X ")
elif res == 2 :
    print("   ")
    nombre1 = input("Ingresa el nombre del Jugador 1: ")
    nombre2 = "Robot"
    jug1 = Jugador(nombre1,1," 0 ")
    jug2 = Computador(nombre2,2," X ")
elif res == 3 :
    print("   ")
    print("Computadora Vs. Robot")
    nombre1 = "Computadora"
    nombre2 = "Robot"
    jug1 = Computador(nombre1,1," 0 ")
    jug2 = Computador(nombre2,2," X ")
print("   ")
continuar = input("Deseas continuar una partida anterior? 1-Si o 2-No ")
print("   ")


tab = Tablero()
if continuar == "1" :
    tab.tablero = tab.cargar_tablero()
    jug1.agregar_posiciones(tab.tablero[0])
    jug2.agregar_posiciones(tab.tablero[1])
elif continuar == "2" :
    tab.tablero = tab.nuevo_tablero()
    jug1.agregar_posiciones(tab.tablero[0])
    jug2.agregar_posiciones(tab.tablero[1])

turno = int(tab.tablero[3][0])
finalizar = False
while not finalizar :
    if turno % 2 != 0 :
        num = "1:"
        jug = jug1
        fichas = "'0'"
        ficha = " 0 "
        pos = []
        for item in tab.tablero[0] :
            pos += [item]           
    else :
        num = "2:"
        jug = jug2
        fichas = "'X'"
        ficha = " X "
        pos = []
        for item in tab.tablero[1] :
            pos += [item]
    jug.posiciones = []
    jug.agregar_posiciones(pos)
    perdedor = tab.perdedor(jug)
    if perdedor :
        print(tab)
        print("   ")
        finalizar = True
        if jug == jug1 :
            ganador = jug2
            perdedor = jug1
        else :
            ganador = jug1
            perdedor = jug2
        print("   ")    
        print("**********************************************************************")
        print("La partida ha terminado!")
        print("El jugador" , jug.numero , ":" , jug.nombre , "se ha quedado sin posibles movimientos")
        print("El jugador" , ganador.numero , ":" , ganador.nombre , "es el ganador!")
        print("**********************************************************************")

    else :
        movimiento_realizado = False
        eleccion = 0
        while not movimiento_realizado and eleccion == 0 :
            print("   ")
            tab.analizar_tablero()
            print(tab)
            print("   ")
            print("***** Turno del jugador" , jug.numero , jug.nombre, "*****")
            print("""Que deseas hacer?
1) Realizar un movimiento
2) Guardar la partida (salir/continuar)
3) Rendirse""")
            if jug.humano :
                eleccion = int(input("Elige una opcion: "))
                if eleccion != 1 and eleccion != 2 and eleccion != 3 :
                    eleccion = 0
                    print("   ")
                    print("Ingresa una opcion valida")
            else :
                eleccion = 1
            
            if eleccion == 1 :
                fase1 = False
                #En la fase 1 se verifica que la celda inicial, sea una ficha
                #del jugador correspondiente, y que tenga posibles movimientos
                while not fase1 :
                    print("   ")
                    print("Selecciona la celda de la ficha que deseas mover.Recuerda que tus fichas son las", fichas)
                    if jug.humano :
                        celda_inicial = input()
                    else :
                        celda_inicial = jug.celda_a_mover(tab)
                        print("   ")
                        print("Seleccionando ficha a mover")
                        time.sleep(1)
                        print(celda_inicial)
                        time.sleep(1)

                    if jug == jug1 :
                        casilla = tab.tablero[0]
                    elif jug == jug2 :
                        casilla = tab.tablero[1]

                    if celda_inicial not in casilla :
                        print("   ")
                        print("Esta celda no contiene una de tus amazonas.")
                        fase1 = False
                    else :
                        mov = tab.quedan_movimientos(celda_inicial)
                        if not mov :
                            fase1 = False
                            print("   ")
                            print("Esta amazona no tiene movimientos posibles")
                        else :
                            fase1 = True

                fase2 = False
                #En la fase 2 se verifica que la ficha de la celda inicial, se pueda
                #trasladar a la celda final ingresada
                while not fase2 :
                    print("   ")
                    print("Ahora selecciona la celda a la cual deseas mover la ficha.(Recuerda que debe estar vacia la nueva celda)")
                    if jug.humano :
                        celda_final = input()
                    else :
                        lm = jug.posibilidades(celda_inicial,tab)
                        movi = jug.analizar_movimiento(lm,celda_inicial,tab)
                        celda_final = tab.traducir(movi)
                        print("   ")
                        print("Calculando mejor movimiento")
                        time.sleep(1)
                        print(celda_final)
                        time.sleep(1)
                        
                    permitido = tab.movimiento_valido(celda_inicial , celda_final , jug)
                    if permitido :
                        pos.remove(celda_inicial)
                        pos.append(celda_final)
                        jug.posiciones = []
                        jug.agregar_posiciones(pos)
                        fase2 = True
                        if jug == jug1 :
                            tab.tablero[0] = pos
                        else :
                            tab.tablero[1] = pos
                        tab.quitar_fichas()
                        tab.analizar_tablero()
                        print(tab)
                    else :
                        fase2 = False

                fase3 = False
                #En la fase 3 se verifica que el lanzamiento este dentro de la linea
                #de fuego de la celda final, y que la casilla este vacia.
                while not fase3 :
                    print("   ")
                    print("Ahora, selecciona la celda a la cual lanzar una flecha")
                    lan_valido = False
                    if jug.humano :
                        celda_flecha = input()
                    else :
                        posi = jug.posibilidades(celda_final,tab)
                        if jug == jug2 :
                            en = tab.traducir(jug.analizar_lanzamiento(posi,jug1,tab))
                        elif jug == jug1 :
                            en = tab.traducir(jug.analizar_lanzamiento(posi,jug2,tab))
                        print("   ")
                        print("Analizando posibles lanzamientos")
                        time.sleep(1)
                        celda_flecha = en
                        print(celda_flecha)
                        time.sleep(1)

                        
                    lan_valido = tab.lanzamiento_valido(celda_final,celda_flecha,jug)
                    if lan_valido :
                        (tab.tablero[2]).append(celda_flecha)
                        tab.analizar_tablero()
                        fase3 = True

                movimiento_realizado = True
                turno += 1

            elif eleccion == 2 :
                tab.tablero[3] = str(jug.numero)
                tab.guardar_tablero()
                print("La partida ha sido guardada")
                print("Deseas continuar la partida o salir (1-Continuar. 2-Salir)")
                seguir = int(input())
                if seguir == 2:
                    finalizar = True
                elif seguir == 1:
                    print("La partida continuara")

            elif eleccion == 3 :
                finalizar = True
                if jug == jug1 :
                    ganador = jug2
                    perdedor = jug1
                else :
                    ganador = jug1
                    perdedor = jug2

                print("   ")    
                print("**********************************************************************")
                print("La partida ha terminado!")
                print("El jugador" , perdedor.numero , ":" , perdedor.nombre , ", se ha rendido.")
                print("El jugador", ganador.numero , ":" , ganador.nombre , ", es el ganador!")    
                print("**********************************************************************")
                    
            
                
                
                


                    

            
        
    




    


