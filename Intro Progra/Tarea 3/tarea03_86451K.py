import time
#Estoy optando por el bonus de la tarea.
#La manera en que logre optimizar el tiempo que tarda en obtener el resultado
#fue asegurandome de realizar la funcion recursiva, entregando como
#posibilidades las casillas del tablero en las que era seguro que se necesitara
#una luz.
#Para esto las organice segun las paredes que contienen un numero. De mayor a menor
#Las paredes con mayores numero entregan sus casillas de posibilidades con mayor
#pertinencia, al momento de realizar la funcion recursiva.

#Se explicara un poco mas en las funciones

#Las estadisticas se guardaran dentro del archivo, en la ultima linea, justo despues
#del tablero. En caso de no tener, empiezan desde 0

class Tablero :
    def __init__(self,nombre) :
        self.nombre = nombre
        archivo = open(self.nombre)
        lineas = archivo.readlines()
        archivo.close()
        limpias = []
        for linea in lineas :
            limpias += [linea.strip().split(",")]

        if limpias[-1][0] == "Estadisticas" :
            self.correctas = int(limpias[-1][1])
            self.incorrectas = int(limpias[-1][2])
            self.tablero = limpias[:len(limpias)-1]
        else :
            self.correctas = 0
            self.incorrectas = 0
            self.tablero = limpias

        self.vacias = []
        self.paredes = []
        self.luces = []
        

    def guardar_partida(self,nombre) :
        if "guardado" in nombre :
            save = nombre
        else :
            save = nombre[:len(nombre)-4] + "_guardado.txt"
        archivo = open(save , "w")
        for ele in self.tablero :
            print(",".join(ele),file=archivo)
        stats = "Estadisticas," + str(self.correctas) + "," + str(self.incorrectas)
        print(stats , file=archivo)
        archivo.close()
        print("Partida Guardada con exito! Nombre del archivo:" , save)
        print("   ")


    
    def analizar_tablero(self) :
        self.vacias = []
        self.luces = []
        self.paredes = []
        f = 0
        for linea in self.tablero :
            c = 0
            while c < len(linea) :
                if self.tablero[f][c] == "-" or self.tablero[f][c] == "L" :
                    self.vacias += [[f , c]]
                    
                elif self.tablero[f][c] == "X" :
                    self.paredes += [[f , c , "X"]]
                    
                elif self.tablero[f][c].isnumeric() :
                    self.paredes += [[f , c , int(self.tablero[f][c])]]

                elif self.tablero[f][c] == "B" :
                    self.luces += [[f,c]]

                c += 1
            f += 1
    
    def esta_iluminada(self,i,j) :
        iluminado = False

        if [i,j] in self.luces :
            iluminado = True
        else :
            
            fila = i
            while (fila + 1) < len(self.tablero) and (self.tablero[fila+1][j] == "-" or self.tablero[fila+1][j] == "B"):
                fila += 1
                if [fila,j] in self.luces :
                    iluminado = True

            col = j
            while (col+1) < len(self.tablero[0]) and (self.tablero[i][col+1] == "-" or self.tablero[i][col+1] == "B") :
                col += 1
                if [i,col] in self.luces :
                    iluminado = True

            fila = i
            while (fila-1) >= 0 and (self.tablero[fila-1][j] == "-" or self.tablero[fila-1][j] == "B") :
                fila-=1
                if [fila,j] in self.luces :
                    iluminado = True

            col = j
            while (col-1) >= 0 and (self.tablero[i][col-1] == "-" or self.tablero[i][col-1] == "B"):
                col -= 1
                if [i,col] in self.luces :
                    iluminado = True

        return iluminado
        

    def posibilidades(self) :
        posibilidades = []
        cont = 0
        copia = []

        for vac in self.vacias :
            if not self.esta_iluminada(vac[0],vac[1]) :
                posibilidades += [vac]

        for pared in self.paredes :
            if str(pared[2]).isnumeric() :
                anex = self.luces_anexas(pared)
                if pared[2] <= len(anex) or pared[2] == 0 :
                    anex1 = self.calcular_anexas(pared)
                    for par in anex1 :
                        if par in posibilidades :
                            posibilidades.remove(par)
                            
        return posibilidades
                        


        return posibilidades
            
    def calcular_anexas(self,lista) :
        fil = lista[0]
        col = lista[1]
        anexas =[]
        
        f = fil
        if f + 1 < len(self.tablero) and [f+1,col] in self.vacias :
            anexas += [[f+1,col]]
            
        f = fil
        if f - 1 >= 0  and [f-1,col] in self.vacias :
            anexas += [[f-1,col]]
            
        c = col
        if c + 1 < len(self.tablero[0]) and [fil,c+1] in self.vacias :
            anexas += [[fil,c+1]]
            
        c = col    
        if c - 1 >= 0  and [fil,c-1] in self.vacias :
            anexas += [[fil,c-1]]

        return anexas

    def luces_anexas(self,pared) :
        fil = pared[0]
        col = pared[1]
        anexas = []

        f = fil
        if f + 1 < len(self.tablero) and self.tablero[f+1][col] == "B" :
            anexas += [[f+1,col]]
            
        f = fil
        if f - 1 >= 0  and self.tablero[f-1][col] == "B" :
            anexas += [[f-1,col]]
            
        c = col
        if c + 1 < len(self.tablero[0]) and self.tablero[fil][c+1] == "B" :
            anexas += [[fil,c+1]]
            
        c = col    
        if c - 1 >= 0  and self.tablero[fil][c-1] == "B" :
            anexas += [[fil,c-1]]

        return anexas
            
                   
    def posibles(self) :
        #Esta funcion no solo busca las posibilidades para el metodo recursivo,
        #sino que tambien las ordena segun su petinencia, para lograr optimizar el
        #tiempo en que entrega el resultado.
        posible = []
        copia = []
        def orden(item) :
            return -item[2]-len(self.luces_anexas(item)) , len(self.calcular_anexas(item))
        
        for pared in self.paredes :
            if (pared[2]) != "X" and pared[2] > 0 :
                copia += [pared]
            
        copia.sort(key=orden)


        if len(copia) > 0 :
            for par in copia :
                anexas = self.calcular_anexas(par)
                posible += anexas

            for p in self.paredes:
                if p[2] == 0 :
                    lista = self.calcular_anexas(p)
                    for cel in lista :
                        if cel in posible :
                            posible.remove(cel)
               
        else :
            for vac in self.vacias :
                posible += [vac]

            for par in self.paredes :
                a = self.calcular_anexas(par)
                for luz in a :
                    if luz in posible and par[2] == 0 :
                        posible.remove(luz)

        if len(posible) > 0 :
            ult = []
            for celda in posible :
                if not self.esta_iluminada(celda[0],celda[1]):
                    ult += [celda]
        return ult
                      
    def asignacion_valida(self,i,j) :
        valida = True

        if [i,j] in self.vacias :
            for pared in self.paredes :
                anexas = self.calcular_anexas(pared)
                if [i,j] in anexas and str(pared[2]).isnumeric() and pared[2] > 0 and pared[2] > len(self.luces_anexas(pared)):
                    valida = True
                elif [i,j] in anexas and str(pared[2]).isnumeric() and (not pared[2] > 0 or pared[2] <= len(self.luces_anexas(pared))) :
                    valida = False
                    print("·No se pueden colocar mas luces cerca de esta pared!")
                    print("   ")

            if self.esta_iluminada(i,j) :
                print("·Esta celda ya esta iluminada")
                print("   ")
                valida = False

        elif self.tablero[i][j] == "X" or self.tablero[i][j].isnumeric() :
            for pare in self.paredes :
                if pare[:2] == [i,j] :
                    valida = False
                    print("·No puedes colocar luces en las paredes!")
                    print("   ")

        elif [i,j] in self.luces :
            print("·Esta celda ya tiene una luz")
            print("   ")
            valida = False

        if valida :
            self.correctas += 1
        else :
            self.incorrectas += 1
                       
        return valida
        

    def tablero_completo(self) :
        completo = False
        cont = 0
        for celda in self.vacias :
            if self.esta_iluminada(celda[0],celda[1]) :
                cont += 1
        if cont == len(self.vacias) :
            completo = True
        return completo

    def tablero_res(self) :
        res = []
        resuelto = False
        if self.tablero_completo() :
            for pared in self.paredes :
                if str(pared[2]).isnumeric() :
                    anexas = self.luces_anexas(pared)
                    cont = len(anexas)
                    if pared[2] == 0 :
                        res += [True]
                    else :
                        res += [False]
            if False in res :
                resuelto = False
            else :
                resuelto = True
                
        return resuelto                   

    def colocar_luz(self, i , j) :
        self.tablero[i][j] = "B"
        self.analizar_tablero()
            
    def quitar_luz(self,i,j) :
        if [i,j] in self.luces :
            valido = True
            self.tablero[i][j] = "-"
            self.analizar_tablero()
        else :
            valido = False
            print("·Esta celda no contiene una luz")
            print("   ")
        return valido

    def remover_ampolletas(self) :
        for luz in self.luces :
            self.tablero[luz[0]][luz[1]] = "-"
        self.analizar_tablero()

    def tablero_resuelto(self) :
        valido = False
        if self.tablero_completo() :
            for pared in self.paredes :
                if (str(pared[2]).isnumeric()) and (pared[2] != len(self.luces_anexas(pared))) :
                    valido = False
                    return valido
                else :
                    valido = True
        return valido
                    

    def prender_luces(self) :
        cont = 0
        for luz in self.luces :
            f = luz[0]
            c = luz[1]

            while f + 1 < len(self.tablero) and [f+1,c] in self.vacias :
                cont += 1
                f += 1
                self.tablero[f][c] = "L"

            f = luz[0]
            c = luz[1]

            while f - 1 >= 0 and [f-1,c] in self.vacias :
                cont += 1
                f -= 1
                self.tablero[f][c] = "L"

            f = luz[0]
            c = luz[1]
            while c - 1 >= 0 and [f,c-1] in self.vacias :
                cont += 1
                c -= 1
                self.tablero[f][c] = "L"

            f = luz[0]
            c = luz[1]
            while c + 1 < len(self.tablero[0]) and [f,c+1] in self.vacias :
                cont += 1
                c += 1
                self.tablero[f][c] = "L"

        print(self)
        print("   ")
        input("·Presiona ENTER para continuar")
        
        self.apagar_luces()              
                
    def apagar_luces(self) :
        k = 0
        for ele in self.tablero :
           l = 0
           for i in ele :
               if i == "L" :
                   self.tablero[k][l] = "-"
               l += 1
           k += 1
        self.analizar_tablero()
            
    def reducir_paredes(self,i,j) :
        for pared in self.paredes :
            if str(pared[2]).isnumeric() :
                a = pared[:2]
                anex = self.luces_anexas(a)
                for anexas in anex :
                    if [i,j] == anexas :
                        pared[2] -= 1
                        self.tablero[pared[0]][pared[1]] = str(pared[2])


    def aumentar_paredes(self,i,j) :
        for pared in self.paredes :
            if str(pared[2]).isnumeric() :
                a = pared[:2]
                anex = self.calcular_anexas(a)
                if [i,j] in anex :
                    pared[2] += 1
                    self.tablero[pared[0]][pared[1]] = str(pared[2])
            
    
    def __str__(self) :
        n = len(self.tablero[0])
        msg = ""
        fijo = "   " + "+---" * n + "+" + "\n"
        col = ""
        for i in range(0,n) :
            co = "| " + str(i) + " "
            col += co
        columnas = "   " + col
        msg += columnas + "|" + "\n"
        msg += fijo

        n = len(self.tablero)
        fil = ""
        for j in range(0,n) :
            if len(str(j)) == 1 :
                fi = " " + str(j) + "| "
                for elem in self.tablero[j] :
                    if elem == "-" :
                        m = "   "
                    elif elem == "X" :
                        m = " X "
                    elif elem.isnumeric() :
                        m = " "+str(elem)+" "
                    elif elem == "B" :
                        m = " B "
                    elif elem == "L" :
                        m = " L "
                    fi += m + "|"
            msg += fi + "\n"
            msg += fijo
        msg += "Ampolletas -> B , Paredes -> (X/Num) , Iluminadas -> (L/B)" + "\n"
    
        return msg

    def iniciar_solucion(self) :
        soluciones = []
        parcial = []
        self.resolver_tablero(parcial , soluciones)
        return soluciones
    
    def resolver_tablero(self , parcial , soluciones) :
        if self.tablero_res() :
            copia = parcial[:]
            soluciones += copia
            return True

        else :

            posibles = self.posibles()

            falle = False
            i = 0
            while (not falle) and (i < len(posibles)) :
                pos = posibles[i]
                parcial += [pos]
                self.tablero[pos[0]][pos[1]] = "B"
                self.reducir_paredes(pos[0],pos[1])
                self.analizar_tablero()
                falle = self.resolver_tablero(parcial,soluciones)
                luz = parcial[len(parcial)-1]
                self.tablero[luz[0]][luz[1]] = "-"
                self.analizar_tablero()
                self.aumentar_paredes(luz[0],luz[1])


                self.analizar_tablero()
                parcial.pop()
                i += 1
            return falle
            

#Codigo Principal

print("""Bienvenido a Akari! Las reglas del juego son simples:
El objetivo del juego es colocar luces estrategicamente para iluminar todas las casillas.
En cada turno tendras distintas opciones.
Las luces iluminan toda la fila y columna en la que estan, hasta toparse con un borde
o una pared.
Podras colocar y quitar luces segun desees, pero ten en cuenta que el tablero tendra
paredes que indicaran cual es el maximo obligatorio de luces adyacentes que deben tener.
Entre cada turno puedes guardar la partida. Si te rindes, puedes pedir la solucion del tablero.""")

print("   ")
jugador = input("Ingresa tu nombre: ")
print("   ")
print("""Elige un opcion
1.Nueva partida
2.Cargar partida""")
opcion = 0
while opcion != 1 and opcion != 2 :
    opcion = int(input("Opcion: "))
    print("   ")
    if opcion != 1 and opcion != 2 :
        print("Ingresa una opcion valida")

if opcion == 1 :
    print("""Selecciona el nivel de dificultad :
1. Facil
2. Medio
3. Dificil""")
    nivel = 0
    while nivel != 1 and nivel != 2 and nivel != 3 :
        nivel = int(input("Nivel: "))
        print("   ")
        if nivel != 1 and nivel != 2 and nivel != 3 :
            print("Selecciona un nivel correctamente")
            
    if nivel == 1 :
        nombre = "facil.txt"
    elif nivel == 2 :
        nombre = "medio.txt"
    elif nivel == 3 :
        nombre = "dificil.txt"

elif opcion == 2 :
    print("Ingresa el nombre del archivo que deseas cargar (sin el .txt):")
    nombre = input() + ".txt"
    print("   ")
    
tab = Tablero(nombre)
tab.analizar_tablero()

acabado = False
while not acabado :
    print(tab)
    
    print("""Escoge una accion :
1. Colocar un ampolleta
2. Eliminar una ampolleta
3. Prender Luces
4. Guardar partida
5. Remover todas las ampolletas
6. Resolver Tablero
7. Salir del Juego""")
    print("   ")
    print("Jugadas Correctas:" , tab.correctas)
    print("Jugadas Incorrectas :" , tab.incorrectas)
    print("   ")
    eleccion = 0
    while eleccion not in [1,2,3,4,5,6,7] :
        eleccion = int(input("Eleccion: "))
        if eleccion not in [1,2,3,4,5,6,7]:
            print("Selecciona una accion correcta")

    if eleccion == 1 :
        
        if len(tab.posibilidades()) == 0 :
            print("No hay mas celdas disponibles para colocar ampolletas")
            print("Debes eliminar alguna(s) ampolleta(s)")
            print("   ")
        else :
            valida = False
            while not valida :
                celda = []
                fila = (-1)
                while (fila < 0) or (fila >= len(tab.tablero)) :
                    print("Ingresa la fila de la celda en la que deseas colocar una ampolleta")
                    fila = int(input("Fila: "))
                    print("   ")
                    if fila < 0 or fila >= len(tab.tablero) :
                        print("Esta fila no esta dentro del tablero. Intenta de nuevo.")
                        print("   ")
                celda += [fila]
                
                col = (-1)
                while col < 0 or col >= len(tab.tablero[0]) :
                    print("Ingresa la columna de la celda en la que deseas colocar una ampolleta")
                    col = int(input("Columna: "))
                    if col < 0 or col >= len(tab.tablero[0]) :
                        print("Esta columna no esta dentro del tablero. Intenta de nuevo.")
                        print("   ")
                celda += [col]
            
                if tab.asignacion_valida(celda[0],celda[1]) :
                    tab.colocar_luz(celda[0],celda[1])
                    print("   ")

                valida = True
                    
    elif eleccion == 2 :

        if len(tab.luces) == 0 :
            print("Actualmente no hay ampolletas en el tablero")
            print("   ")
            
        else :
            valida = False
            while not valida :
                celda = []
                fila = (-1)
                while (fila < 0) or (fila >= len(tab.tablero)) :
                    print("Ingresa la fila de la celda en la que deseas eliminar una ampolleta")
                    fila = int(input("Fila: "))
                    print("   ")
                    if fila < 0 or fila >= len(tab.tablero) :
                        print("Esta fila no esta dentro del tablero. Intenta de nuevo.")
                        print("   ")
                celda += [fila]
                
                col = (-1)
                while col < 0 or col >= len(tab.tablero[0]) :
                    print("Ingresa la columna de la celda en la que deseas eliminar una ampolleta")
                    col = int(input("Columna: "))
                    if col < 0 or col >= len(tab.tablero[0]) :
                        print("Esta columna no esta dentro del tablero. Intenta de nuevo.")
                        print("   ")
                celda += [col]

                if tab.quitar_luz(celda[0],celda[1]) :
                    valida = True
                    print("La ampolleta fue eliminada")
                    print("   ")

    elif eleccion == 3 :
        
        if len(tab.luces) == 0 :
            print("No se pueden encender luces en un tablero sin ampolletas")
            print("   ")
            
        else :
            tab.prender_luces()

    elif eleccion == 4 :
        tab.guardar_partida(nombre)

    elif eleccion == 5 :
        tab.remover_ampolletas()
        print("Todas las ampolletas han sido eliminadas")
        
    elif eleccion == 6 :
        tab.remover_ampolletas()
        a = time.time()
        solucion = tab.iniciar_solucion()
        b = time.time()
        print(b-a)
        print("   ")
        print("----------------------")
        print("SOLUCION DEL TABLERO")
        print("----------------------")
        for celda in solucion :
            tab.colocar_luz(celda[0],celda[1])
        print(tab)
        print("   ")
        print("///////////////////////")
        print("Te has rendido")
        print("El juego ha terminado")
        print("///////////////////////")
        acabado = True

    elif eleccion == 7 :
        print("   ")
        print("Hasta luego!")
        acabado = True

        
    if tab.tablero_resuelto() and not acabado :
        print(tab)
        print("   ")
        print("//////////////////////////////////////////////////////")
        print("Felicitaciones! Has resuelto el tablero correctamente!")
        print("# De jugadas correctas :" , tab.correctas)
        print("# De jugadas incorrectas :" , tab.incorrectas)
        print("//////////////////////////////////////////////////////")
        acabado = True


        

   
    
    

    
      



 
