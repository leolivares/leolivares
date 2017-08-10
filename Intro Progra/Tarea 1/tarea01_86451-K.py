print("""BIENVENIDOS AL TEXT TWIST 3
Las reglas del juego son las siguientes:
1. Cada jugador en su turno debe intentar escribir una palabra valida.
2. Una palabra valida es aquella que:
    - Existe
    - No se haya utilizado anteriormente en algun turno
    - Se pueda construir a partir de tres o mas letras del pozo de letras.
3. En su turno, cada jugador tiene 3 oportunidades para excribir una palabra valida.
4. Si ambos jugadores pasan 2 veces seguidas, se acaba el juego.
""")

#importamos las funciones que utilizaremos del modulo mezclador.py
import mezclador

#escribimos una funcion, que nos permita repetir las opciones cada turno

def opciones(numero_jugador,nombre_jugador) :
    print("   ")
    print("Turno del jugador" , numero_jugador , ":" , nombre_jugador)
    print("Pozo de Letras --> " , nuevo_pozo)
    print("""Acciones :
(1) Ingresar palabra
(2) Reordenar las letras
(3) Pasar
(4) Terminar el juego
""")
    print("Intentos restantes: " , oportunidad)
    print("Reordenamientos restantes: " , 3 - orden)
    opcion_seleccionada = int(input("Que quieres hacer? "))
    print("------------------------------------------------------------------")
    return opcion_seleccionada


#Ahora, escribimos una funcion que verifique si la palabra es valida

def verificador(palabra) :
    es_valida = mezclador.existe_palabra(palabra)
    return es_valida

#Ahora, una funcion que agregue palabras que han sido utilizadas

def añadir(palabra) :
    mezclador.agregar_palabra(palabra)

#Ahora, una funcion que verifique si alguna plabra ha sido utilizada

def utilizada(palabra) :
    fue_utilizada = mezclador.palabra_usada(palabra)
    return fue_utilizada

#Ahora, una funcion que reordene alguna palabra

def reordenar(palabra) :
    nueva = mezclador.reordenar_palabra(palabra)
    return nueva

#Ahora, una funcion que reescriba el pozo de letras de una manera ordenada (con mayusculas y espacios)

def acomodar(palabra) :
    palabra_mayus = palabra.upper()
    entonces = ""
    espacio = " "
    for letra in palabra_mayus :
        nuevo_pozo = letra + espacio
        entonces += nuevo_pozo
    return entonces

#Escribimos una funcion que permita verificar que las letras de la palabra ingresada, sean las del pozo
def letras_validas(palabra,pozo) :
    if len(palabra) <= len(pozo) :
        cont = 0
        abc = "ABCEDFGHIJKLMNOPQRSTUVWXYZ"
        for letra in abc :
            a = pozo.count(letra)
            b = palabra.count(letra)
            if b > a :
                cont += 1
        if cont != 0 :
            letrasvalidas = False
        else :
            letrasvalidas = True
    else :
        letrasvalidas = False
    return letrasvalidas


#Nombre de los jugadores

jug1 = input("Ingresa el nombre del jugador 1: ")
jug2 = input("Ingresa el nombre del jugador 2: ")

#Cantidad de letras con las que desean jugar y pozo de letras
cantidad = 0
while cantidad != 5 and cantidad != 6 and cantidad != 7 :
    cantidad = int(input("Cantidad de letras a utilizar (5, 6 o 7): "))
    if cantidad != 5 and cantidad != 6 and cantidad != 7 :
        print("   ")
        print("Ingresa una cantidad valida")
        print("   ")
palabra_entrante = mezclador.obtener_palabra(cantidad)
pozo = mezclador.reordenar_palabra(palabra_entrante)
tam_pozo = len(pozo)
nuevo_pozo = acomodar(pozo)



#Parametros para que continue el juego
pasar = 0
orden = 0
eleccion = 0
parametros = (pasar < 4) and (eleccion != 4)

#Establezco el loop con el cual el juego continuara.y otros datos
#Se establecera la variable turno, la cual indicara el turno del jugador.

turno = 1
puntos1 = 0
puntos2 = 0



#Codigo Central
#Comienzo el proceso de iteracion entre los jugadores.
#Comenzando por el primero
oportunidad = 3
while (pasar < 4) and (eleccion != 4) :
    if turno % 2 != 0 :
        eleccion = opciones(1 , jug1)
        
        if eleccion != 1 and eleccion != 2 and eleccion!= 3 and eleccion != 4 :
            print("Opcion no valida: Utiliza una opcion correcta.")
            
        elif eleccion == 1 :
            palab = input("Ingresa tu palabra: ")
            palabra = palab.upper()
            valida = verificador(palabra)
            usada = utilizada(palabra)
            letrasvalidas = letras_validas(palabra,pozo)

            
            if oportunidad > 0 :
                if valida != True :
                    print("Palabra no valida: la palabra no existe")
                    oportunidad -= 1
                    pasar = 0
                    print("Pierdes una oportunidad, queda(n)" , oportunidad , "oportunidad(es)")

                elif usada == True :
                    print("Palabra no valida: la palabra ya ha sido utilizada en turnos anteriores")
                    oportunidad -= 1
                    pasar = 0
                    print("Pierdes una oportunidad, queda(n)" , oportunidad , "oportunidad(es)")

                elif letrasvalidas == False :
                    print("La palabra no esta correctamente formada segun el pozo")
                    oportunidad -= 1
                    pasar = 0
                    print("Pierdes una oportunidad, queda(n)" , oportunidad , "oportunidad(es)")

                elif (valida == True) and (usada == False) and (letrasvalidas == True) :
                    tam_palabra = len(palabra)
                    if tam_palabra == tam_pozo :
                        puntos_obtenidos = (tam_palabra * 5)
                        puntos1 += (tam_palabra) * 5
                    else :
                        puntos_obtenidos = (tam_palabra * 2)                       
                        puntos1 += (tam_palabra) * 2
                    añadir(palabra)
                    print("Palabra valida, gana" , puntos_obtenidos , "puntos! Se acaba el turno del jugador 1")
                    turno += 1
                    pasar = 0
                    oportunidad = 3
                    orden = 0


            if oportunidad == 0 :
                print("   ")
                print("Perdiste tus 3 oportunidades")
                print("Se pasa al turno del jugador 2, con un descuento de 2 puntos")
                puntos1 -= 2
                turno += 1
                oportunidad = 3
                orden = 0
                    


        elif eleccion == 2 :
            orden += 1
            if orden >= 4 :
                turno += 1
                oportunidad = 3
                orden = 0
                pasar = 0
                print("   ")
                print("Se pasa al turno del jugador 2, por exceso de reordenamiento.")
            else :
                nuevo_pozo = acomodar(reordenar(pozo))
                pasar = 0
                print("    ")
                print("Letras reordenadas!")

        elif eleccion == 3 :
            pasar += 1
            turno += 1
            oportunidad = 3
            orden = 0

        elif eleccion == 4 :
            ganador = jug2
            perdedor = jug1
            pasar = 4
            eleccion = 4
            


    elif turno % 2 == 0 :
        eleccion = opciones(2, jug2)
        
        if eleccion != 1 and eleccion != 2 and eleccion!= 3 and eleccion != 4 :
            print("Opcion no valida: Utiliza una opcion correcta.")
            
        if eleccion == 1 :
            palab = input("Ingresa tu palabra: ")
            palabra = palab.upper()
            valida = verificador(palabra)
            usada = utilizada(palabra)
            letrasvalidas = letras_validas(palabra,pozo)

            
            if oportunidad > 0 :
                if valida != True :
                    print("Palabra no valida: la palabra no existe")
                    oportunidad -= 1
                    pasar = 0
                    print("Pierdes una oportunidad, queda(n)" , oportunidad , "oportunidad(es)")

                elif usada == True :
                    print("Palabra no valida: la palabra ya ha sido utilizada en turnos anteriores")
                    oportunidad -= 1
                    pasar = 0
                    print("Pierdes una oportunidad, queda(n)" , oportunidad , "oportunidad(es)")

                elif letrasvalidas == False :
                    print("La palabra no esta correctamente formada segun el pozo")
                    oportunidad -= 1
                    pasar = 0
                    print("Pierdes una oportunidad, queda(n)" , oportunidad , "oportunidad(es)")

                elif (valida == True) and (usada == False) :
                    tam_palabra = len(palabra)
                    if tam_palabra == tam_pozo :
                        puntos_obtenidos = (tam_palabra * 5)
                        puntos2 += (tam_palabra * 5)
                    else :
                        puntos_obtenidos = (tam_palabra * 2)
                        puntos2 += (tam_palabra * 2)
                    añadir(palabra)
                    print("Palabra valida, gana" , puntos_obtenidos , "puntos! Se acaba el turno del jugador 2")
                    turno += 1
                    pasar = 0
                    oportunidad = 3
                    orden = 0

            if oportunidad == 0 :
                print("   ")
                print("Se pasa al turno del jugador 1, con un descuento de 2 puntos.")
                puntos2 -= 2
                turno += 1
                oportunidad = 3
                orden = 0

        elif eleccion == 2 :
            orden += 1
            if orden >= 4 :
                turno += 1
                oportunidad = 3
                orden = 0
                pasar = 0
                print("     ")
                print("Se pasa al turno del jugador 1, por exceso de reordenamiento.")

            else :
                nuevo_pozo = acomodar(reordenar(pozo))
                pasar = 0
                print("    ")
                print("Letras reordenadas!")

        elif eleccion == 3 :
            pasar += 1
            turno += 1
            oportunidad = 3
            orden = 0

        elif eleccion == 4 :
            ganador = jug1
            perdedor = jug2
            pasar = 4
            eleccion = 4
            


#Termina el while y aparecen los resultados finales del juego

if eleccion == 4 :
    print("///////////////////////////////////////")
    print("El jugador", perdedor, "se ha rendido.")
    print("El ganador es" , ganador , "!!!")
else :
    if puntos1 > puntos2 :
        print("   ")
        print("El ganador es:" , jug1 , "!!!")
    elif puntos2 > puntos1 :
        print("   ")
        print("El ganador es:" , jug2 , "!!!")
    else :
        print("   ")
        print("No hay ganador. EMPATE!")

print(" ")
print("*************************************************")
print("Se acaba el juego!")
print(jug1 , "(jugador 1) tiene" , puntos1 , "puntos")
print(jug2 , "(jugador 2) tiene" , puntos2 , "puntos")
print("*************************************************")
###Termina



    
          


