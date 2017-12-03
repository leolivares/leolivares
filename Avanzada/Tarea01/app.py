import usuarios as us
import mercados as merc
import datetime as dt
from decimal import Decimal
from time import gmtime , strftime


class Aplicacion :

    id = 1
    def __init__(self):
        self.mercados = []
        self.caja = 0
        self.usuarios = []
        self.underaged = []
        self.traders = []
        self.investors = []
        self.monedas = []

    #Realiza la lectura inicial de los .csv
    #Crea las clases necesarias (Usuarios, Mercados, Orders)
    #Guarda los objetos en donde pertenecen
    def leer_base_datos(self):

        #Currencies
        archivo = open("Currencies.csv","r")
        lineas = archivo.readlines()
        limpio = []
        for linea in lineas :
            limpio += [linea.strip().split(";")]
        archivo.close()

        header = limpio.pop(0)

        base = []
        simbolos = []
        for linea in limpio :
            i = 0
            for head in header :
                if "symbol" in head :
                    base += [0]
                    simbolos += [linea[i]]
                i += 1


        i = 0
        simbolos += ["DCC"]
        base += [0]
        mercados = []
        while i < len(simbolos) :
            j = 0
            while j < len(simbolos) :
                if simbolos[i] != simbolos[j] :
                    mercados += [simbolos[i]+simbolos[j]]
                j += 1
            i += 1

        i = 0
        for head in header :
            if "name" in head :
                num = i
            i += 1
        for linea in limpio :
            self.monedas.append(linea[num])
        self.monedas.append("DCC CryptoCoin")

        #Creamos todos los posibles mercados a partir de la Currencies
        for mer in mercados :
            self.mercados += [merc.Mercado(mer)]


        #Registramos a los Usuarios
        archivo = open("users.csv","r")
        lineas = archivo.readlines()
        limpio = []
        for linea in lineas:
            limpio += [linea.strip().split(";")]
        archivo.close()
        header = limpio.pop(0)
        for linea in limpio :

            i = 0
            for head in header :
                if "orders" in head :
                    orden = linea[i]
                    i += 1
                elif "birthday" in head :
                    fecha = linea[i]
                    i += 1
                elif "username" in head :
                    username = linea[i]
                    i += 1
                elif "lastname" in head :
                    lastname = linea[i]
                    i += 1
                elif "name" in head :
                    name = linea[i]
                    i += 1
                elif "mercados_registrados" in head :
                    merc_regis = linea[i]
                    i += 1
                elif "tipo" in head :
                    tipo = linea[i]
                    i += 1


            if len(header) == 5 :
                self.registro(username,False,name,lastname,fecha,orden,list(),None)
            else :
                self.registro(username, False, name, lastname, fecha, orden,merc_regis,tipo)


        #Creamos las ordenes
        archivo = open("orders.csv","r")
        lineas = archivo.readlines()
        limpio = []
        for linea in lineas :
            limpio += [linea.strip().split(";")]
        archivo.close()

        header = limpio.pop(0)

        for linea in limpio:

            i = 0
            for head in header:
                if "order_id" in head:
                    order_id = linea[i]
                    i += 1
                elif "amount" in head:
                    amount = linea[i]
                    i += 1
                elif "date_created" in head:
                    date_created = linea[i]
                    i += 1
                elif "type" in head:
                    type = linea[i]
                    i += 1
                elif "price" in head:
                    price = linea[i]
                    i += 1
                elif "ticker" in head :
                    ticket = linea[i]
                    i += 1
                elif "date_match" in head :
                    date_match = linea[i]
                    i += 1

            for mer in self.mercados :
                if ticket == mer.ticket :
                    mer.crear_order(price,amount,type,ticket,order_id,date_created,date_match)


        #Asigna a los usuarios sus respectivos balances

        archivo = open("users.csv","r")
        lineas = archivo.readlines()
        header = lineas.pop(0).strip().split(";")
        archivo.close()

        if len(header) == 5 :

            # Agrega a los mercados, a los respectivos usuarios
            for mer in self.mercados:
                for ord in mer.orders:
                    for usua in self.usuarios:
                        for id in usua.orders_id:
                            if ord.id == id:
                                mer.usuarios += [usua]


            #Revisa los match del archivo inicial, antes de entrar al programa
            for merca in self.mercados:
                if len(merca.orders) != 0:
                    for ord in merca.orders:
                        if not ord.fecha_match  :
                            self.buscar_matches(ord,False)

            for usu in self.usuarios:
                for mer in self.mercados:
                    if usu in mer.usuarios:
                        usu.mercados_registrados += [mer.ticket]


            self.calcular_last_id()


        elif len(header) == 8 :

            for linea in lineas :
                limpio += [linea.strip().split(";")]

            i = 0
            for head in header :
                if "username" in head :
                    num_us = i
                i += 1


            for usua in self.usuarios :
                usua.balance = []
                for linea in limpio :
                    if linea[num_us] == usua.usuario :
                        balan = linea[-1].split(":")
                        for x in balan :
                            usua.balance += [Decimal(x)]

            for usua in self.usuarios :
                for mer in usua.mercados_registrados :
                    for merca in self.mercados :
                        if mer == merca.ticket :
                            merca.usuarios.append(usua)

            self.calcular_last_id()

    #Retorna una lista, que representa el balance de un nuevo usuario
    def base_currencies(self):
        archivo = open("Currencies.csv","r")
        lineas = archivo.readlines()
        lineas.pop(0)

        base = []
        for linea in lineas:
            base += [Decimal("0")]
        base += [Decimal("0")]
        return base


    #Retorna una lista con las currencies ordenadas
    #Esta lista ayudara a sumar y restar cantidades en los balances
    def obtener_currencies(self):
        archivo = open("Currencies.csv","r")
        lineas = archivo.readlines()
        archivo.close()
        header = lineas.pop(0).strip().split(";")
        limpio = []
        for linea in lineas :
            limpio += [linea.strip().split(";")]
        i = 0
        for head in header :
            if "symbol" in head :
                num = i
            i += 1
        currencies = []
        for curr in limpio :
            currencies += [curr[num]]
        currencies += ["DCC"]
        return currencies

    #Se encarga de registrar a los usuarios en el sistema
    #Si son usuarios previamente registrados, utiliza la informacion de los .csv
    #Si son usuarios nuevos, obtiene la informacion a traves de la consola
    #Los usuarios nuevos reciben 100.000 DCC
    def registro(self,username=None,nuevo=True,*args):

        aceptado = True
        for usuario in self.usuarios :
            if usuario.usuario == username :
                aceptado = False
                print("El usuario {} es invalido. Ya esta registrado".format(username))

        if aceptado :
            if nuevo :
                username = input("Ingresa tu nombre de usuario: ")
                registrado = False
                for usua in self.usuarios :
                    if usua.usuario == username :
                        print("  ")
                        print("Este usuario ya esta registrado")
                        print("  ")
                        registrado = True

                if not registrado :
                    nombre = input("Ingresa tu nombre: ")
                    apellido = input("Ingresa tu apellido: ")
                    fecha_correcta = False
                    while not fecha_correcta :
                        fecha = input("Ingresa tu fecha de nacimiento (yyyy-mm-dd): ")
                        lista = fecha.split("-")
                        if len(fecha) != 10 :
                            fecha_correcta = False
                            print("Escribe tu fecha de nacimiento con el formato correcto yyyy-mm-dd")
                        elif int(lista[0]) < 1900 or int(lista[0]) > 2017 :
                            fecha_correcta = False
                            print("Tu fecha de nacimiento no puede ser esta.")
                        else :
                            fecha_correcta = True
                    orders = []
                    balance = self.base_currencies()
                    tipo = None
                    mercs_regis = []
                    print("  ")
                    print("El usuario {} ha sido registrado exitosamente".format(username))
                    print("  ")
                    balance[-1] += Decimal("100000")
                    print("Recibiste 100000 monedas DCC por registrarte al sistema")

            else :
                registrado = False
                nombre = args[0]
                apellido = args[1]
                fecha = args[2]
                orders = args[3].split(":")
                if orders[0] == "":
                    orders = []


                if len(args[4]) != 0 :
                    mercs_regis = args[4].split(":")
                else :
                    mercs_regis = []

                if args[5] :
                    tipo = args[5]
                else :
                    tipo = None

                balance = self.base_currencies()

            if not registrado :
                actual = dt.datetime.now()


                if tipo :
                    if tipo == "Underaged" :
                        cliente = us.Underaged(username, nombre, apellido, fecha, orders, balance, mercs_regis)
                        self.underaged += [cliente]
                        self.usuarios += [cliente]

                    elif tipo == "Trader" :
                        cliente = us.Trader(username, nombre, apellido, fecha, orders, balance, mercs_regis)
                        self.traders += [cliente]
                        self.usuarios += [cliente]

                    elif tipo == "Investor" :
                        cliente = us.Investor(username, nombre, apellido, fecha, orders, balance, mercs_regis)
                        self.traders += [cliente]
                        self.usuarios += [cliente]

                else :
                    if actual - dt.timedelta(days=(365*18)) < dt.datetime.strptime(fecha,'%Y-%m-%d') :
                        cliente = us.Underaged(username, nombre, apellido, fecha, orders,balance,mercs_regis)
                        self.underaged += [cliente]
                        self.usuarios += [cliente]

                    else :
                        cliente = us.Trader(username, nombre, apellido, fecha, orders,balance,mercs_regis)
                        self.traders += [cliente]
                        self.usuarios += [cliente]


    #Permite entrar al sistema a usuarios registrados
    def iniciar_sesion(self) :

        username = input("Ingresa tu nombre de usuario: ")

        ingresar = False
        for user in self.usuarios :
            if user.usuario == username :
                ingresar = True
                cliente = user

        if ingresar :
            print("Bienvenido {} al sistema".format(username))
        else :
            cliente = None
            print("  ")
            print("Este usuario no esta registrado.")
            print("  ")

        return ingresar , cliente

    #Calcula el ultimo id utilizado en una order
    def calcular_last_id(self):
        ids = []
        for mercado in self.mercados :
            for order in mercado.orders:
                ids += [order.id]

        seguir = True
        while seguir :
            if str(Aplicacion.id) in ids :
                Aplicacion.id += 1
            else :
                seguir = False

    #Muestra una lista de todos los mercados disponibles
    def mercados_disponibles(self):
        print("Esta es la lista de los mercados disponibles:")
        i = 1
        for mercado in self.mercados :
            print("   ", str(i)+". "+mercado.ticket,"\n")
            i += 1
        print("   ")

    #Muestra un lista de los mercados en los que esta registrado el cliente
    def mercados_registrados(self,cliente):

        registrados = []
        for mercado in self.mercados :
            for usuario in mercado.usuarios :
                if usuario.usuario == cliente.usuario :
                    registrados += [mercado]

        if len(registrados) == 0 :
            print("  ")
            print("No te encuentras regitrado en ningun mercado")
            print("  ")

        else :
            print("  ")
            print("Te encuentras registrado en los siguientes mercados:")
            print("  ")
            i = 1
            for merc in registrados :
                print("   ",str(i)+". "+merc.ticket)
                i += 1
            print("   ")


    #Registra a un cliente en un mercado, si no estaba registrado
    #Se encarga de que el cliente reciba 50.000 de cada moneda
    def registrar_mercado(self,cliente,mercado):

        for mer in self.mercados :
            if mer.ticket.lower() == mercado.lower() :
                registrado = False
                for usuario in mer.usuarios :
                    if usuario.usuario == cliente.usuario :
                        registrado = True
                if not registrado :
                    mer.usuarios += [cliente]
                    mer.aniadir_monedas(self,cliente)
                    cliente.mercados_registrados.append(mer.ticket)
                else :
                    print("   ")
                    print("Ya te encuentras registrado en este mercado")
                    print("   ")
        return registrado

    #Se encarga de mostrar por mercado, las orders realizadas ese dia
    def lista_orders_dia(self,cliente):
        existen = False
        for mer in self.mercados :
            lista = mer.orders_del_dia()
            if len(lista) != 0 :
                existen = True
                for order in lista :
                    print("   ")
                    print("El mercado {} registro el dia de hoy las siguientes orders".format(mer.ticket))
                    print("   Tipo:", order[0].tipo, "Cantidad:", order[0].cantidad, "Precio:", order[0].precio, "Fecha:",order[0].fecha, "Match:", order[1])
                    print("   ")

        if not existen :
            print("  ")
            print("No hay orders realizadas el dia de hoy")
            print("  ")

        hoy = dt.datetime.today()
        fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
        tiempo = strftime("%H:%M:%S", gmtime())
        self.registro_acciones(cliente.usuario, fecha, tiempo, "Consulta de Orders del Dia")


    #Se encarga de mostrar por mercado, las orders realizadas en una fecha especifica
    #Si el usuario es Underaged o Trader, solo tiene acceso a los ultimos 7 dias
    def lista_orders_fecha(self,cliente):
        dia = input("Ingresa el dia: ")
        mes = input("Ingresa el mes: ")
        permitido = False
        while not permitido :
            anio = input("Ingresa el anio: ")
            if len(anio) == 4 :
                permitido = True
            else :
                print("Ingresa el anio correctamente (%yyyy)")
        if len(dia) == 1 :
            dia = "0" + dia
        if len(mes) == 1 :
            mes = "0" + mes
        buscar = True

        if isinstance(cliente,us.Trader) or isinstance(cliente,us.Underaged) :
            hoy = dt.datetime.today()
            menos_siete = hoy - dt.timedelta(days=(7))
            fecha = "{}-{}-{}".format(anio,mes,dia)
            fecha1 = dt.datetime.strptime(fecha,"%Y-%m-%d")
            if fecha1 < menos_siete :
                print("  ")
                print("Por ser un usuario {}, no puedes acceder a orders realizadas hace mas de 7 dias.".format(cliente.tipo))
                print("  ")
                buscar = False

        if buscar :
            existen = False
            for mer in self.mercados :
                lista = mer.orders_fecha_especifica(fecha)
                if len(lista) != 0 :
                    existen = True
                    for order in lista :
                        print("   ")
                        print("El mercado {} registro en la fecha {}-{}-{} las siguientes orders:".format(mer.ticket,dia,mes,anio))
                        print("    Tipo:",order[0].tipo,"Cantidad:",order[0].cantidad,"Precio:",order[0].precio,"Fecha:",order[0].fecha,"Match:",order[1])

            if not existen :
                print("   ")
                print("En la fecha {}-{}-{} no se realizaron orders".format(dia,mes,anio))
                print("   ")

            hoy = dt.datetime.today()
            fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
            tiempo = strftime("%H:%M:%S", gmtime())
            self.registro_acciones(cliente.usuario, fecha, tiempo, "Consulta de Orders entre Fechas")


    #Se encarga de mostrar por mercado, las orders realizadas entre dos fechas
    #Si el usuario es Underaged o Trader, solo tiene acceso a los ultimos 7 dias
    def lista_orders_entre(self,cliente):

        permitido = False
        while not permitido :
            fecha1 = input("Ingresa la fecha min (yyyy-mm-dd): ")
            if len(fecha1) == 10 :
                permitido = True
            else :
                print("Ingresa la fecha en el formato correcto yyyy-mm-dd")

        permitido = False
        while not permitido :
            fecha2 = input("Ingresa la fecha max (yyyy-mm-dd): ")
            if len(fecha2) == 10 :
                permitido = True
            else :
                print("Ingresa la fecha en el formato correcto yyyy-mm-dd")

        buscar = True

        if isinstance(cliente, us.Trader) or isinstance(cliente, us.Underaged):
            hoy = dt.datetime.today()
            menos_siete = hoy - dt.timedelta(days=(7))
            fecha3 = dt.datetime.strptime(fecha1, "%Y-%m-%d")
            fecha4 = dt.datetime.strptime(fecha2, "%Y-%m-%d")
            if fecha3 < menos_siete :
                print("  ")
                print("Por ser un usuario {}, no puedes acceder a orders realizadas hace mas de 7 dias.".format(cliente.tipo))
                print("  ")
                buscar = False

            if fecha4 > hoy :
                print("  ")
                print("No puedes realizar una busqueda en este rango de fechas")
                print("  ")
                buscar = False

        elif isinstance(cliente,us.Investor) :
            fecha3 = dt.datetime.strptime(fecha1, "%Y-%m-%d")
            fecha4 = dt.datetime.strptime(fecha2, "%Y-%m-%d")

        if buscar :
            while fecha3 <= fecha4 :
                for mer in self.mercados :
                    lista = mer.orders_entre_fechas(fecha1)
                    if len(lista) != 0 :
                        for order in lista :
                            print("   ")
                            print("El mercado {} registro en la fecha {} las siguientes orders:".format(mer.ticket, fecha1))
                            print("    Id:" , order[0].id, "Tipo:", order[0].tipo, "Cantidad:", order[0].cantidad, "Precio:",order[0].precio, "Fecha:", order[0].fecha, "Match:", order[1])
                            print("   ")

                fecha3 = fecha3 + dt.timedelta(days=1)
                fecha1 = "{}-{}-{}".format(fecha3.year,fecha3.month,fecha3.day)

            hoy = dt.datetime.today()
            fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
            tiempo = strftime("%H:%M:%S", gmtime())
            self.registro_acciones(cliente.usuario, fecha, tiempo, "Consulta de Orders Historicas")


    #Se encarga de mostrar las orders de un mercado en especifico
    #Si el usuario es Underaged o Trader, solo tiene acceso a los ultimos 7 dias
    def lista_orders_mercado(self,mercado,cliente):
        existe = False
        hoy = dt.datetime.today()

        for mer in self.mercados :
            if mer.ticket.lower() == mercado.lower() :
                existe = True
                if isinstance(cliente,us.Underaged) or isinstance(cliente,us.Trader) :
                    vacio = True
                    menos_siete = hoy - dt.timedelta(days=7)
                    print("   ")
                    print("Se mostraran las orders realizadas en el mercado {}, durante los ultimos 7 dias".format(mercado))
                    while hoy >= menos_siete :
                        fecha = hoy.strftime("%Y-%m-%d")
                        f = fecha.split("-")
                        lista = mer.orders_entre_fechas(fecha)
                        if len(lista) != 0 :
                            vacio = False
                            for order in lista :
                                print("   ")
                                print("El mercado {} registro en la fecha {}-{}-{} las siguientes orders:".format(mer.ticket, f[0], f[1], f[2]))
                                print("    Id:", order[0].id , "Tipo:", order[0].tipo, "Cantidad:", order[0].cantidad, "Precio:",order[0].precio, "Fecha:", order[0].fecha, "Match:", order[1])
                                print("   ")

                        hoy = hoy - dt.timedelta(days=1)

                    if vacio :
                        print("   ")
                        print("El mercado {} no ha registrado orders en los ultimos 7 dias".format(mercado))
                        print("   ")

                elif isinstance(cliente,us.Investor) :
                    print("   ")
                    print("Se mostraran las orders realizadas en el mercado {}".format(mercado))
                    if len(mer.orders) != 0 :
                        print("   ")
                        print("El mercado {} registro las siguientes orders:".format(mercado))
                        for order in mer.orders :
                            match = False
                            if order.fecha_match != "" :
                                match = True
                            print("    Id:" , order[0].id, "Tipo:", order.tipo, "Cantidad:", order.cantidad, "Precio:",order.precio, "Fecha:", order.fecha, "Match:",match)
                        print("   ")

                    else :
                        print("   ")
                        print("El mercado {} no tiene orders registradas".format(mercado))
                        print("   ")

                hoy = dt.datetime.today()
                fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
                tiempo = strftime("%H:%M:%S", gmtime())
                self.registro_acciones(cliente.usuario, fecha, tiempo, "Consulta de Orders (Mercado)",mercado)

        if not existe :
            print("El mercado {} no existe".format(mercado))


    #Se encarga de mostrar todas la orders activas
    #Si el usuario es Underaged o Trader, solo tiene acceso a los ultimos 7 dias
    def lista_orders_activas(self,cliente):

        activas = False
        if isinstance(cliente, us.Underaged) or isinstance(cliente, us.Trader):
            for merca in self.mercados :
                printear = True
                hoy = dt.datetime.today()
                menos_siete = hoy - dt.timedelta(days=7)
                while hoy >= menos_siete :
                    fecha = hoy.strftime("%Y-%m-%d")
                    if len(merca.orders_activas) != 0 :
                        for order in merca.orders_activas :
                            fecha1 = dt.datetime.strptime(order.fecha,"%Y-%m-%d")
                            fecha1 = fecha1.strftime("%Y-%m-%d")
                            if fecha1 == fecha :
                                activas = True
                                if printear :
                                    print("   ")
                                    print("Las orders activas para el mercado {}, en los ultimos 7 dias, son las siguientes:".format(merca.ticket))
                                    printear = False
                                print("    Tipo:", order.tipo, "Cantidad:", order.cantidad, "Precio:",order.precio, "Fecha:", order.fecha, "Match: False")
                    hoy = hoy - dt.timedelta(days=1)
            print("   ")
            if not activas :
                print("No hay orders activas en los mercados en los ultimos 7 dias.")
                print("   ")

        elif isinstance(cliente,us.Investor) :
            for merca in self.mercados :
                if len(merca.orders_activas) != 0 :
                    activas = True
                    print("   ")
                    print("Las orders activas para el mercado {} son las siguientes:".format(merca.ticket))
                    for order in merca.orders_activas :
                        print("    Tipo:", order.tipo, "Cantidad:", order.cantidad, "Precio:", order.precio, "Fecha:",order.fecha, "Match: False")
            print("   ")
            if not activas :
                print("No hay orders activas en los mercados.")
                print("   ")

        hoy = dt.datetime.today()
        fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
        tiempo = strftime("%H:%M:%S", gmtime())
        self.registro_acciones(cliente.usuario, fecha, tiempo, "Consulta de Orders Activas")


    #Se encarga de mostrar la informacion de uno o todos los mercados en el sistema
    #Es decir, el spread, volumenes, y best
    def desplegar_informacion(self,mercado=None):

        if mercado :
            for mer in self.mercados :
                if mercado.lower() == mer.ticket.lower() :
                    todas , activas = mer.numero_ordenes()
                    if activas != 0 :
                        spread = mer.spread()
                        v_asks = mer.volumen_acumulado_asks()
                        v_bids = mer.volumen_acumulado_bids()
                        ask_best = mer.ask_best()
                        bid_best = mer.bid_best()
                        print("   ")
                        print("Informacion General del Mercado: {}".format(mercado))
                        print("    Cantidad de orders: {}".format(todas))
                        print("    Cantidad de orders activas: {}".format(activas))
                        if spread[1] :
                            print("    Spread: {}".format(spread[0]))
                        else :
                            print("    Spread: No existe informacion suficiente para calcular este dato")
                        print("    Volumen acumulado de Asks: {} {}".format(v_asks[1],v_asks[0]))
                        print("    Volumen acumulado de Bids: {} {}".format(v_bids[1], v_bids[0]))
                        if ask_best[1] != False :
                            print("    Ask Best: {} {}".format(ask_best[1],ask_best[0]))
                        else :
                            print("    Actualmente no se puede calcular un ask_best (No hay asks)")
                        if bid_best[1] != False :
                            print("    Bid Best: {} {}".format(bid_best[1],bid_best[0]))
                        else :
                            print("    Actualmente no se puede calcular un bid_best (No hay bids)")
                        print("   ")
                    else :
                        print("   ")
                        print("Informacion General del Mercado: {}".format(mercado))
                        print("    Cantidad de orders: {}".format(todas))
                        print("    Cantidad de orders activas: {}".format(activas))
                        print("    Spread: No hay orders activas para calcular este dato.")
                        print("    El volumen de asks y bids actualmente son 0 ambos.")
                        print("    El ask_best y bid_best actualmente no se pueden calcular")
                        print("   ")

        else :
            for mer in self.mercados :
                todas, activas = mer.numero_ordenes()
                if activas != 0:
                    spread = mer.spread()
                    v_asks = mer.volumen_acumulado_asks()
                    v_bids = mer.volumen_acumulado_bids()
                    ask_best = mer.ask_best()
                    bid_best = mer.bid_best()
                    print("   ")
                    print("Informacion General del Mercado: {}".format(mer.ticket))
                    print("    Cantidad de orders: {}".format(todas))
                    print("    Cantidad de orders activas: {}".format(activas))
                    if spread[1] :
                        print("    Spread: {}".format(spread[0]))
                    else :
                        print("    Spread: No existe informacion suficiente para calcular este dato")
                    print("    Volumen acumulado de Asks: {} {}".format(v_asks[1], v_asks[0]))
                    print("    Volumen acumulado de Bids: {} {}".format(v_bids[1], v_bids[0]))
                    if ask_best[1] != False:
                        print("    Ask Best: {} {}".format(ask_best[1], ask_best[0]))
                    else:
                        print("    Actualmente no se puede calcular un ask_best (No hay asks)")
                    if bid_best[1] != False:
                        print("    Bid Best: {} {}".format(bid_best[1], bid_best[0]))
                    else:
                        print("    Actualmente no se puede calcular un bid_best (No hay bids)")
                    print("   ")
                else:
                    print("   ")
                    print("Informacion General del Mercado: {}".format(mer.ticket))
                    print("    Cantidad de orders: {}".format(todas))
                    print("    Cantidad de orders activas: {}".format(activas))
                    print("    Spread: No hay orders activas para calcular este dato.")
                    print("    El volumen de asks y bids actualmente son 0 ambos.")
                    print("    El ask_best y bid_best actualmente no se pueden calcular")
                    print("   ")


    #Se encarga de permitir al usuario ingresar un ask a un mercado
    def ingresar_ask(self,cliente):
        mer = input("Ingresa el mercado en el que deseas colocar un ask: ")
        for merca in self.mercados :
            if mer.lower() == merca.ticket.lower() :
                if cliente not in merca.usuarios :
                    print("No te encuentras registrado en este mercado.")
                    print("Debes registrate antes de realizar un order.")
                else :
                    cantidad = Decimal(input(("Ingresa la cantidad de {} que deseas vender: ".format(mer[:3]))))
                    precio = Decimal(input("Ingresa el precio en {} al que deseas vender cada unidad: ".format(mer[3:])))
                    vender = True
                    if cantidad == 0 :
                        vender = False
                        print("No puedes ingresar una orden de venta por 0 {}".format(mer[:3]))
                    elif precio == 0 :
                        vender = False
                        print("No puedes ingresar una orden de venta sin precio. Necesitamos la comision!")
                    elif not cliente.revisar_balance(self.obtener_currencies(),cantidad,mer[:3]) :
                        print("La cantidad de {} que deseas ofrecer es mayor a la que posees.".format(mer[:3]))
                        vender = False
                    if vender :
                        id = Aplicacion.id
                        currencies = self.obtener_currencies()
                        i = 0
                        for curr in currencies :
                            if curr.lower() == mer[:3].lower() :
                                num = i
                            i += 1
                        cliente.balance[num] -= cantidad
                        order = merca.nuevo_ask(id,cantidad,precio,cliente)
                        Aplicacion.id += 1
                        cliente.informacion_entrada(self)
                        hoy = dt.datetime.today()
                        fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
                        tiempo = strftime("%H:%M:%S", gmtime())
                        self.registro_acciones(cliente.usuario, fecha, tiempo, "Ingresar Ask")
                        return order

    # Se encarga de permitir al usuario ingresar un bid a un mercado
    def ingresar_bid(self,cliente):
        mer = input("Ingresa el mercado en el que deseas colocar un bid: ")
        for merca in self.mercados :
            if mer.lower() == merca.ticket.lower() :
                if cliente not in merca.usuarios :
                    print("No te encuentras registrado en este mercado.")
                    print("Debes registrate antes de realizar un order.")
                else :
                    cantidad = Decimal(input(("Ingresa la cantidad de {} que deseas comprar: ".format(mer[:3]))))
                    precio = Decimal(input("Ingresa el precio en {} al que deseas comprar cada unidad: ".format(mer[3:])))
                    comprar = True
                    if cantidad == 0 :
                        comprar = False
                        print("No puedes ingresar una orden de venta por 0 {}".format(mer[:3]))
                    elif precio == 0 :
                        comprar = False
                        print("No puedes ingresar una orden de venta sin precio. Necesitamos la comision!")
                    elif not cliente.revisar_balance(self.obtener_currencies(),precio*cantidad,mer[3:]) :
                        print("La cantidad de {} que deseas obtener es mayor a la que puedes pagar ({}).".format(mer[:3],precio*cantidad))
                        comprar = False
                    if comprar :
                        id = Aplicacion.id
                        currencies = self.obtener_currencies()
                        i = 0
                        for curr in currencies :
                            if curr.lower() == mer[3:].lower() :
                                num = i
                            i += 1
                        cliente.balance[num] -= precio*cantidad
                        order = merca.nuevo_bid(id,cantidad,precio,cliente)
                        Aplicacion.id += 1
                        cliente.informacion_entrada(self)
                        hoy = dt.datetime.today()
                        fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
                        tiempo = strftime("%H:%M:%S", gmtime())
                        self.registro_acciones(cliente.usuario,fecha,tiempo,"Ingresar Bid")
                        return order

    #Permite a un usuario Trader, que cumple las condiciones, convertirse en un Investor
    def upgrade(self,cliente):
        if float(cliente.balance[-1]) >= 300000:
            nuevo_cliente = cliente.upgrade_investor()

            for mer in self.mercados :
                i = 0
                for usu in mer.usuarios :
                    if usu.usuario == cliente.usuario :
                        mer.usuarios[i] = nuevo_cliente
                    i += 1

            i = 0
            for usua in self.usuarios :
                if usua.usuario == cliente.usuario :
                    num = i
                i += 1
            self.usuarios.pop(num)
            self.usuarios += [nuevo_cliente]
            print("   ")
            print("Felicitaciones! Ahora eres un usuario Investor" "\n"
                  "Tendras muchas mas ventajas que antes.")
            print("   ")
            return nuevo_cliente

        else:
            print("   ")
            print("No tienes suficientes monedas DCC para realizar el upgrade a Investor")
            print("   ")

    #Se encarga de buscar un match para una order
    def buscar_matches(self,order,permiso):
        for mercado in self.mercados :
            if mercado.ticket.lower() == order.ticket.lower() :
                mercado.match(order,self.obtener_currencies(),permiso)

    #Se encarga de permitir una transaccion entre usuarios
    def banco(self,cliente):
        permitido = False
        currencies = self.obtener_currencies()
        for bal in cliente.balance :
            if bal > 0 :
                permitido = True

        if not permitido :
            print("  ")
            print("Lo sentimos, pero no tienes monedas para transferir.")
            print("   ")

        else :
            username = input("Ingresa el username del usuario al que deseas transferir monedas: ")
            existe = False
            for user in self.usuarios :
                if user.usuario == username :
                    transferir_a = user
                    existe = True

            if not existe :
                print("  ")
                print("Lo sentimos, pero el usuario ingresado no existe.")
                print("   ")

            else :
                cliente.transferencia(transferir_a,currencies)

    #Se encarga de guardar los datos del sistema en los archivos .csv
    def actualizar_datos(self):

        archivo = open("users.csv","w")

        print("name:string;lastname:string;username:string;birthday:string;orders:list;tipo:string;mercados_registrados;balance:list",file=archivo)

        columna = []
        for usuario in self.usuarios :
            if isinstance(usuario,us.Underaged) :
                tipo = "Underaged"
            elif isinstance(usuario,us.Trader) :
                tipo = "Trader"
            elif isinstance(usuario,us.Investor) :
                tipo = "Investor"

            balan = []
            for balance in usuario.balance :
                balan.append(str(balance))
            balan = ":".join(balan)

            ids = []
            for id in usuario.orders_id :
                ids.append(str(id))
            ids = ":".join(ids)

            merc_regis = []
            for mer in usuario.mercados_registrados :
                merc_regis.append(mer)
            merc_regis = ":".join(merc_regis)


            fila = usuario.nombre + ";" + usuario.apellido + ";" + usuario.usuario + ";" + usuario.fecha + ";" + ids + ";" +  tipo + ";" + merc_regis + ";" + balan
            columna.append(fila)

        for fila in columna :
            print(fila,file=archivo)

        archivo.close()

        archivo = open("orders.csv","w")

        print("order_id:int;type:string;ticker:string;price:float;amount:float;date_created:string;date_match:string",file=archivo)

        columna = []
        for mer in self.mercados :
            for ord in mer.orders :
                if not ord.fecha_match :
                    ord.fecha_match = " "
                fila = str(ord.id) + ";" + ord.tipo + ";" + mer.ticket + ";" + str(ord.precio) + ";" + str(ord.cantidad) + ";" + ord.fecha + ";" + ord.fecha_match
                columna.append(fila)

        for fila in columna :
            print(fila,file=archivo)

        archivo.close()

    #Se encarga de mostrarle al usuario su balance
    #Ademas, muestra su saldo total en monedas DCC
    #Si no hay un valor actual aun (no se ha realizado un match)
    #entonces la relacion entre la moneda y DCC sera 1-1
    def consultar_saldo(self,cliente):
        currencies = self.obtener_currencies()
        cliente.consultar_saldo(currencies)

        salde_en_dcc = 0
        valor = []
        for merca in self.mercados :
            if merca.ticket[3:] == "DCC" :
                if merca.valor :
                    valor.append(merca.valor)
                else:
                    valor.append(1)
        valor.append(1)

        i = 0
        for bal in cliente.balance :
            salde_en_dcc += bal * valor[i]
            i += 1

        print("Tu saldo total en monedas DCC es igual a {}".format(salde_en_dcc))
        print("   ")

        hoy = dt.datetime.today()
        fecha = dt.datetime.strftime(hoy,"%Y-%m-%d")
        tiempo = strftime("%H:%M:%S",gmtime())
        self.registro_acciones(cliente.usuario,fecha,tiempo,"Consulta de Saldo")

    #Se encarga de registrar acciones y eventos en el sistema
    #Toda esta informacion termina en el archivo registros.csv
    def registro_acciones(self,*args):
        archivo = open("registros.csv","a")
        msg = ""
        for arg in args :
            msg += str(arg) + ";"
        msg.strip(";")
        print(msg,file=archivo)
        archivo.close()

    #Retorna la cantidad de orders activas que tiene un cliente
    def revisar_activas(self,cliente):
        cant = 0
        for mer in self.mercados :
            for order in mer.orders_activas :
                if order.id in cliente.orders_id :
                    cant += 1
        return cant

    #Muestra una lista de todos los usuarios en el sistema
    def consulta_usuarios(self):
        underaged = []
        traders = []
        investors = []
        for usu in self.usuarios :
            if isinstance(usu,us.Underaged) :
                underaged.append(usu)
            elif isinstance(usu,us.Trader) :
                traders.append(usu)
            elif isinstance(usu,us.Investor) :
                investors.append(usu)

        if len(underaged) != 0 :
            print("   ")
            print("Los usuarios Underaged registrados son los siguientes:")
            for under in underaged :
                print("   " , under.usuario, " " , under.nombre , " ", under.apellido)
            print("   ")
        else :
            print("   ")
            print("No hay usuarios Underaged registrados en el sistema")
            print("   ")


        if len(traders) != 0:
            print("   ")
            print("Los usuarios Traders registrados son los siguientes:")
            for trade in traders:
                print("   ", trade.usuario, " ", trade.nombre, " ", trade.apellido)
            print("   ")
        else:
            print("   ")
            print("No hay usuarios Traders registrados en el sistema")
            print("   ")


        if len(investors) != 0:
            print("   ")
            print("Los usuarios Investors registrados son los siguientes:")
            for inves in investors:
                print("   " ,inves.usuario, " ", inves.nombre, " ", inves.apellido)
            print("   ")
        else:
            print("   ")
            print("No hay usuarios Investors registrados en el sistema")
            print("   ")


    #Muestra un lista con todos los matches que se ha realizado
    def historial_matches(self):
        match = []
        for mer in self.mercados :
            for order in mer.orders :
                if order.fecha_match :
                    if len(order.fecha_match) > 3 :
                        match.append(order)
        print("   ")
        ticket = ""
        for order in match :
            if order.ticket != ticket :
                print("------------------------------------------------------------------------------------------------")
            ticket = order.ticket
            print("Order Id:", order.id , "Fecha:", order.fecha, "Fecha de Match:", order.fecha_match, "Tipo:", order.tipo, "Mercado:", order.ticket)
        print("   ")


    #Muestra informacion importante sobre un moneda en especifico
    def info_moneda(self,moneda):
        currencies = self.obtener_currencies()
        if moneda.upper() in currencies :
            i = 0
            for curr in currencies :
                if curr.lower() == moneda.lower() :
                    num = i
                i += 1
            print("   ")
            print("Simbolo:", moneda.upper(), ";", "Nombre:", self.monedas[num])

            mer_order_activa = []
            for mer in self.mercados :
                if mer.ticket[:3].lower() == moneda.lower() :
                    if len(mer.orders_activas) != 0 :
                        mer_order_activa.append(mer)
                    if mer.valor != None :
                        print("Mercado:", mer.ticket, "; Valor actual de la moneda {}".format(moneda.upper()), mer.valor)
                        if len(mer.orders) != 0 :
                            print("Ultima order realizada en este mercado fue el {}".format(mer.orders[-1].fecha))
                        else:
                            print("No se han realizado orders en este mercado")
                        print("---------------------------------------------------------")
            print("Cantidad de Mercados con Orders activas. Transando la moneda {}:".format(moneda), len(mer_order_activa))
            print("   ")

        else :

            print("   ")
            print("Esta moneda no existe.")
            print("   ")


    #Permite a un usuario cancelar una order que no ha realizado match
    def cancelar_order(self,cliente,order_id):
        if int(order_id) not in cliente.orders_id :
            print("   ")
            print("Lo sentimos, pero esta order id no esta entre las tuyas.")
            print("   ")

        else :
            activa = False
            mercado = None
            for mer in self.mercados :
                for ord in mer.orders_activas :
                    if int(ord.id) == int(order_id) :
                        activa = True
                        mercado = mer
                        cancelar = ord

            if activa :
                eliminar_order = []
                for order in mercado.orders :
                    if int(order.id) != int(order_id) :
                        eliminar_order.append(order)
                mercado.orders = eliminar_order

                desactivar_order = []
                for ord in mercado.orders_activas :
                    if int(ord.id) != int(order_id) :
                        desactivar_order.append(ord)
                mercado.orders_activas = desactivar_order

                ids = []
                for id in cliente.orders_id :
                    if int(id) != int(order_id) :
                        ids.append(int(id))
                cliente.orders_id = ids

                currencies =self.obtener_currencies()
                self.devolver_monedas(cliente,cancelar,currencies)

                print("   ")
                print("Tu order numero {} ha sido cancelada".format(order_id))
                print("Recibiste tus monedas nuevamente")
                print("   ")


            else :
                print("   ")
                print("Lo sentimos, pero esta order ya no esta activa.")
                print("   ")

    #Devuelve las monedas a un usuario que cancelo una order
    def devolver_monedas(self,cliente,cancelar,currencies):
        if cancelar.tipo == "ask" :
            devolver = cancelar.cantidad
            moneda = cancelar.ticket[:3]

        elif cancelar.tipo == "bid" :
            devolver = cancelar.cantidad * cancelar.precio
            moneda = cancelar.ticket[3:]

        i = 0
        for curr in currencies :
            if curr == moneda :
                num = i
            i += 1

        cliente.balance[num] += devolver

