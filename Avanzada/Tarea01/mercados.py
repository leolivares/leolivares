import datetime as dt
import random
import usuarios as usu
from decimal import Decimal
from time import gmtime , strftime

class Mercado :

    order_id = 1

    def __init__(self,ticket,valor=None):
        self.ticket = ticket
        self.orders = []
        self.orders_activas = []
        self.asks = []
        self.bids = []
        self.usuarios = []
        self.tasa = Decimal(str(random.randint(1, 40) / 100))
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self,value):
        if value > 0 :
            self._valor = value


    #Crea una order
    def crear_order(self,precio,cantidad,tipo,ticket,id,fecha,fecha_match=None):
        order = [Orders(id,tipo,Decimal(cantidad),Decimal(precio),ticket,fecha,fecha_match)]
        if tipo == "ask" :
            self.asks += order
        elif tipo == "bid" :
            self.bids += order
        self.orders += order
        if not fecha_match :
            self.orders_activas += order

    #Entrega a un usuario las monedas por ingresar a un mercado
    def aniadir_monedas(self,app,cliente):
        curr = app.obtener_currencies()
        moneda_compra = self.ticket[:3]
        moneda_venta = self.ticket[3:]
        i = 0
        for moneda in curr :
            if moneda.lower() == moneda_compra.lower() :
                cliente.balance[i] += Decimal("50000")
            if moneda.lower() == moneda_venta.lower() :
                cliente.balance[i] += Decimal("50000")
            i += 1
        print("   ")
        print("Recibiste 50.000 monedas de {} y {} por registrarte al mercado".format(moneda_compra,moneda_venta))

    #Entrega una lista con las orders del dia
    def orders_del_dia(self):
        orders = []
        hoy = dt.date.today().strftime("%d-%m-%y")

        for order in self.orders :
            order_fecha = dt.datetime.strptime(order.fecha,"%Y-%m-%d")
            order_fecha = dt.datetime.strftime(order_fecha,"%d-%m-%y")
            if order_fecha == hoy :
                if order.fecha_match == "" :
                    orders += [[order,False]]
                else :
                    orders += [[order,True]]
        return orders

    # Entrega una lista con las orders de una fecha especifica
    def orders_fecha_especifica(self,fecha):
        orders = []
        fecha = fecha.split("-")
        anio = fecha[0]
        mes = fecha[1]
        dia = fecha[2]
        if len(mes) == 1 :
            mes = "0" + mes
        if len(dia) == 1 :
            dia = "0" + dia

        fecha = [anio,mes,dia]
        fecha = "-".join(fecha)

        for order in self.orders :
            order_fecha = dt.datetime.strptime(order.fecha,"%Y-%m-%d")
            fecha2 = dt.datetime.strftime(order_fecha,"%Y-%m-%d")

            if fecha2 == fecha :
                if order.fecha_match == "" :
                    orders += [[order,False]]
                else :
                    orders += [[order,True]]
        return orders

    # Entrega una lista con las orders entre fechas
    def orders_entre_fechas(self,fecha):
        orders = self.orders_fecha_especifica(fecha)
        return orders

    # Entrega una lista con las orders de un mercado
    def orders_mercado(self,fecha):
        lista = fecha.split("-")
        anio = lista[0]
        mes = lista[1]
        dia = lista[2]
        if len(mes) == 1 :
            mes = "0" + mes
        if len(dia) == 1 :
            dia = "0" + dia
        orders = self.orders_fecha_especifica(dia,mes,anio)
        return orders

    #Retorna el numero de orders totales y activas de un mercado
    def numero_ordenes(self):
        return (len(self.orders),len(self.orders_activas))

    #Calcula el spread del mercado
    def spread(self):
        posible = True
        min = 1000000000000000
        for order in self.orders_activas:
            if order.tipo == "ask" :
                if Decimal(order.precio) < min :
                    min = Decimal(order.precio)
        if min == 1000000000000000 :
            posible = False

        maxi = 0
        for order in self.orders_activas :
            if order.tipo == "bid" :
                if Decimal(order.precio) > maxi :
                    maxi = Decimal(order.precio)
        if maxi == 0 :
            posible = False

        return [(min - maxi),posible]

    #Calculan los volumenes del mercado
    def volumen_acumulado_asks(self):
        simbolo = self.ticket[:3]
        volumen = 0
        for order in self.orders_activas :
            if order.tipo == "ask" :
                volumen += Decimal(order.cantidad)
        return [simbolo,volumen]


    def volumen_acumulado_bids(self):
        simbolo = self.ticket[3:]
        volumen = 0
        for order in self.orders_activas :
            if order.tipo == "bid" :
                volumen += Decimal(order.precio) * Decimal(order.cantidad)
        return [simbolo,volumen]

    #Calculan los best del mercado
    def ask_best(self):
        min = 100000000000000000
        simbol = self.ticket[:3]
        for order in self.orders_activas :
            if order.tipo == "ask" :
                if float(order.precio) < min :
                    min = float(order.precio)
        if min == 100000000000000000 :
            min = False
        return [simbol,min]


    def bid_best(self):
        maxi = 0
        simbol = self.ticket[3:]
        for order in self.orders_activas :
            if order.tipo == "bid" :
                if float(order.precio) > maxi :
                    maxi = float(order.precio)
        if maxi == 0 :
            maxi = False
        return [simbol,maxi]

    #Calcula el ult id utilizado para una order
    def calcular_id(self,num):
        seguir = True
        while seguir :
            seguir = False
            for order in self.orders :
                if num == order.id :
                    num += 1
                    Mercado.order_id += 1
                    seguir =True
        return num

    #Registra un nuevo ask en el sistema
    def nuevo_ask(self,id,cantidad,precio,cliente):
        hoy = dt.datetime.today()
        fecha = dt.datetime.strftime(hoy,"%Y-%m-%d")
        order = Orders(id,"ask",cantidad,precio,self.ticket,fecha)
        self.asks += [order]
        self.orders += [order]
        self.orders_activas += [order]
        cliente.orders_id += [id]
        return order


    # Registra un nuevo bid en el sistema
    def nuevo_bid(self,id,cantidad,precio,cliente):
        hoy = dt.datetime.today()
        fecha = dt.datetime.strftime(hoy,"%Y-%m-%d")
        order = Orders(id,"bid",cantidad,precio,self.ticket,fecha)
        self.bids += [order]
        self.orders += [order]
        self.orders_activas += [order]
        cliente.orders_id += [id]
        return order

    #Calcula la comision del mercado segun el tipo de cliente
    def calcular_comision(self,monto,cliente):
        if isinstance(cliente,usu.Trader) :
            return self.tasa * Decimal(str(monto))
        elif isinstance(cliente,usu.Investor) :
            return (self.tasa / 2) * Decimal(str(monto))


    #Otorga el pago al vendedor en un match
    def cobrar(self,currencies,ask,monto,vendedor) :
        producto = self.ticket[:3]
        divisa = self.ticket[3:]
        comision = self.calcular_comision(monto,vendedor)

        i = 0
        for curr in currencies :
            if curr == divisa :
                num = i
            i += 1
        pago = monto - comision

        for usu in self.usuarios :
            for ord in usu.orders_id :
                if ord == ask.id :
                    usu.balance[num] += pago

    #Entrega el producto al comprador en un match
    def recibir_producto(self,currencies,bid,monto,comprador):
        producto = self.ticket[:3]
        divisa = self.ticket[3:]
        comision = self.calcular_comision(monto,comprador)

        i = 0
        for curr in currencies :
            if curr == producto :
                num = i
            i += 1

        pago = monto - comision

        for usu in self.usuarios :
            for ord in usu.orders_id :
                if ord == bid.id :
                    usu.balance[num] += pago

    #Disminuye la cantidad ofertada en un ask
    #En caso de ser 0, significa que hubo match
    def reducir_ask(self,ask,cantidad):
        ask.cantidad -= cantidad
        if ask.cantidad == 0 :
            hoy = dt.datetime.today()
            fecha = dt.datetime.strftime(hoy,"%Y-%m-%d")
            ask.fecha_match = fecha
            i = 0
            for order in self.orders_activas :
                if order.tipo == "ask" and order.id == ask.id :
                    num = i
                i += 1
            self.orders_activas.pop(num)

     # Disminuye la cantidad pedida en un bid
     # En caso de ser 0, significa que hubo match
    def reducir_bid(self,bid,cantidad):
        bid.cantidad -= cantidad
        if bid.cantidad == 0 :
            hoy = dt.datetime.today()
            fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
            bid.fecha_match = fecha
            i = 0
            for order in self.orders_activas:
                if order.tipo == "bid" and order.id == bid.id:
                    num = i
                i += 1
            self.orders_activas.pop(num)

    #En caso de haber match o match parcial, por un precio menor al esperado por el comprador
    #se le devuelve al comprador la diferencia que ahorro
    def devolver_diferencia(self,currencies,bid,diferencia):
        producto = self.ticket[:3]
        divisa = self.ticket[3:]

        i = 0
        for curr in currencies :
            if curr == divisa :
                num = i
            i += 1

        for usu in self.usuarios :
            for ord in usu.orders_id :
                if ord == bid.id :
                    usu.balance[num] += diferencia

    #Retorna una lista ordenada segun las prioridades para un match
    def prioridad(self,lista):
        priority = []
        for order in lista :
            for usuario in self.usuarios :
                for id in usuario.orders_id :
                    if id == order.id :
                        if isinstance(usuario,usu.Investor) :
                            priority.append([order,usuario])
        for order in lista :
            for usuario in self.usuarios :
                for id in usuario.orders_id :
                    if id == order.id and [order,usuario] not in priority :
                        priority.append([order,usuario])

        return priority

    #Retorna al cliente segun una order id
    def buscar_cliente(self,order_id):
        for usu in self.usuarios :
            for id in usu.orders_id :
                if id == order_id :
                    return usu

    #Se encarga de analizar todos los casos posibles para un match
    def match(self,order,currencies,permiso) :

        if order.tipo == "ask" :
            cantidad = order.cantidad
            precio = order.precio

            seguir = True
            while seguir :
                match = False
                bids_activas = []
                for ord in self.orders_activas :
                    if ord.tipo == "bid" :
                        bids_activas.append(ord)

                if len(bids_activas) == 0 :
                    seguir = False
                    if permiso :
                        print("//////////////////////////////////////////////////")
                        print("No hay match para el siguiente ask:")
                        print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id,order.cantidad,self.ticket[:3],order.precio,self.ticket[3:]))
                        print("Esta order permanecera en el mercado esperando algun match")
                        print("//////////////////////////////////////////////////")
                        print("   ")
                else :

                    bid_precios_iguales = []
                    bid_precios_mayores = []
                    for bid in bids_activas :
                        if bid.precio == order.precio :
                            bid_precios_iguales.append(bid)
                        elif bid.precio > order.precio :
                            bid_precios_mayores.append(bid)

                    if len(bid_precios_iguales) != 0 :
                        bid_cantidad_iguales = []
                        bid_cantidad_mayor =[]
                        bid_cantidad_menor = []
                        for bid in bid_precios_iguales:
                            if bid.cantidad == cantidad :
                                bid_cantidad_iguales += [bid]
                            elif bid.cantidad < cantidad :
                                bid_cantidad_menor += [bid]
                            elif bid.cantidad > cantidad :
                                bid_cantidad_mayor += [bid]

                        if len(bid_cantidad_iguales) != 0 :
                            lista = self.prioridad(bid_cantidad_iguales)
                            monto = order.precio * order.cantidad
                            cantidad = order.cantidad
                            id_ask = order.id
                            id_bid = lista[0][0].id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies,order,monto,vendedor)
                            self.recibir_producto(currencies,lista[0][0],cantidad,comprador)
                            self.reducir_ask(order,cantidad)
                            self.reducir_bid(lista[0][0],cantidad)
                            self.valor = order.precio
                            match = True
                            seguir = False

                            if permiso :
                                print("----------------------------------------------")
                                print("Tu order de venta (ask) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Vendiste {} {}".format(cantidad,self.ticket[:3]))
                                print("Recibiste como pago una cantidad de {} {}".format(monto,self.ticket[3:]))
                                print("----------------------------------------------")


                        elif len(bid_cantidad_mayor) != 0 :
                            lista = self.prioridad(bid_cantidad_mayor)
                            monto = lista[0][0].precio * order.cantidad
                            cantidad = order.cantidad
                            id_ask = order.id
                            id_bid = lista[0][0].id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies,order,monto,vendedor)
                            self.recibir_producto(currencies,lista[0][0],cantidad,comprador)
                            self.reducir_ask(order,cantidad)
                            self.reducir_bid(lista[0][0],cantidad)
                            self.valor = order.precio
                            match = True
                            seguir = False

                            if permiso :
                                print("----------------------------------------------")
                                print("Tu order de venta (ask) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Vendiste {} {}".format(order.cantidad,self.ticket[:3]))
                                print("Recibiste como pago una cantidad de {} {}".format(monto,self.ticket[3:]))
                                print("----------------------------------------------")


                        elif len(bid_cantidad_menor) != 0 :
                            lista = self.prioridad(bid_cantidad_menor)
                            monto = lista[0][0].cantidad * order.precio
                            cantidad = lista[0][0].cantidad
                            id_ask = order.id
                            id_bid = lista[0][0].id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies,order,monto,vendedor)
                            self.recibir_producto(currencies,lista[0][0],cantidad,comprador)
                            self.reducir_ask(order,cantidad)
                            self.reducir_bid(lista[0][0],cantidad)
                            self.valor = order.precio
                            if order.cantidad == 0 :
                                match = True
                                seguir = False

                            if permiso :
                                print("----------------------------------------------")
                                print("Tu order de venta (ask) realizo un match parcial!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Vendiste {} {}".format(cantidad,self.ticket[:3]))
                                print("Recibiste como pago una cantidad de {} {}".format(monto,self.ticket[3:]))
                                print("----------------------------------------------")


                        else :
                            seguir = False
                            if permiso:
                                print("//////////////////////////////////////////////////")
                                print("No hay match para el siguiente ask:")
                                print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id, order.cantidad,self.ticket[:3],order.precio,self.ticket[3:]))
                                print("Esta order permanecera en el mercado esperando algun match")
                                print("//////////////////////////////////////////////////")
                                print("   ")


                    elif len(bid_precios_mayores) != 0 :
                        bid_cantidad_iguales = []
                        bid_cantidad_mayor = []
                        bid_cantidad_menor = []
                        for bid in bid_precios_mayores :
                            if bid.cantidad == cantidad :
                                bid_cantidad_iguales += [bid]
                            elif bid.cantidad > cantidad :
                                bid_cantidad_mayor += [bid]
                            elif bid.cantidad < cantidad :
                                bid_cantidad_menor += [bid]

                        if len(bid_cantidad_iguales) != 0 :
                            lista = self.prioridad(bid_cantidad_iguales)
                            monto = order.cantidad * order.precio
                            cantidad = order.cantidad
                            diferencia = (lista[0][0].precio * lista[0][0].cantidad) - monto
                            id_ask = order.id
                            id_bid = lista[0][0].id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies,order,monto,vendedor)
                            self.recibir_producto(currencies,lista[0][0],cantidad,comprador)
                            self.reducir_ask(order,cantidad)
                            self.reducir_bid(lista[0][0],cantidad)
                            self.devolver_diferencia(currencies,lista[0][0],diferencia)
                            self.valor = order.precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de venta (ask) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Vendiste {} {}".format(cantidad, self.ticket[:3]))
                                print("Recibiste como pago una cantidad de {} {}".format(monto, self.ticket[3:]))
                                print("----------------------------------------------")


                        elif len(bid_cantidad_mayor) != 0 :
                            lista = self.prioridad(bid_cantidad_mayor)
                            monto = order.precio * order.cantidad
                            cantidad = order.cantidad
                            diferencia = (order.cantidad * lista[0][0].precio) - monto
                            id_ask = order.id
                            id_bid = lista[0][0].id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies,order,monto,vendedor)
                            self.recibir_producto(currencies,lista[0][0],cantidad,comprador)
                            self.reducir_ask(order,cantidad)
                            self.reducir_bid(lista[0][0],cantidad)
                            self.devolver_diferencia(currencies,lista[0][0],diferencia)
                            self.valor = order.precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de venta (ask) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Vendiste {} {}".format(cantidad, self.ticket[:3]))
                                print("Recibiste como pago una cantidad de {} {}".format(monto, self.ticket[3:]))
                                print("----------------------------------------------")


                        elif len(bid_cantidad_menor) != 0 :
                            lista = self.prioridad(bid_cantidad_menor)
                            monto = lista[0][0].cantidad * order.precio
                            cantidad = lista[0][0].cantidad
                            diferencia = (lista[0][0].cantidad * lista[0][0].precio) - monto
                            id_ask = order.id
                            id_bid = lista[0][0].id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies, order, monto,vendedor)
                            self.recibir_producto(currencies, lista[0][0], cantidad,comprador)
                            self.reducir_ask(order, cantidad)
                            self.reducir_bid(lista[0][0], cantidad)
                            self.devolver_diferencia(currencies, lista[0][0], diferencia)
                            self.valor = order.precio
                            if order.cantidad == 0 :
                                match = True
                                seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de venta (ask) realizo un match parcial!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Vendiste {} {}".format(cantidad, self.ticket[:3]))
                                print("Recibiste como pago una cantidad de {} {}".format(monto, self.ticket[3:]))
                                print("----------------------------------------------")


                        else :
                            seguir = False
                            if permiso:
                                print("//////////////////////////////////////////////////")
                                print("No hay match para el siguiente ask:")
                                print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id, order.cantidad,self.ticket[:3],order.precio,self.ticket[3:]))
                                print("Esta order permanecera en el mercado esperando algun match")
                                print("//////////////////////////////////////////////////")
                                print("   ")

                    else :
                        seguir = False
                        if permiso:
                            print("//////////////////////////////////////////////////")
                            print("No hay match para el siguiente ask:")
                            print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id, order.cantidad,self.ticket[:3],order.precio,self.ticket[3:]))
                            print("Esta order permanecera en el mercado esperando algun match")
                            print("//////////////////////////////////////////////////")
                            print("   ")

                if match :
                    hoy = dt.datetime.today()
                    fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
                    tiempo = strftime("%H:%M:%S", gmtime())
                    self.registro_acciones(str(order.id) + "/" + str(lista[0][0].id),fecha,tiempo,"Match")


        elif order.tipo == "bid" :
            cantidad = order.cantidad
            precio = order.precio

            seguir = True
            while seguir :
                match = False
                ask_activas = []
                for ord in self.orders_activas:
                    if ord.tipo == "ask":
                        ask_activas.append(ord)

                if len(ask_activas) == 0:
                    seguir = False
                    if permiso :
                        print("//////////////////////////////////////////////////")
                        print("No hay match para este bid")
                        print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id, order.cantidad,self.ticket[:3], order.precio,self.ticket[3:]))
                        print("Esta order permanecera en el mercado esperando algun match")
                        print("//////////////////////////////////////////////////")
                        print("   ")

                else :

                    ask_precios_iguales = []
                    ask_precios_menores = []
                    for ask in ask_activas:
                        if ask.precio == order.precio:
                            ask_precios_iguales.append(ask)
                        elif ask.precio < order.precio:
                            ask_precios_menores.append(ask)

                    if len(ask_precios_menores) != 0 :
                        ask_cantidad_iguales = []
                        ask_cantidad_mayor = []
                        ask_cantidad_menor = []
                        for ask in ask_precios_menores:
                            if ask.cantidad == cantidad :
                                ask_cantidad_iguales += [ask]
                            elif ask.cantidad < cantidad :
                                ask_cantidad_menor += [ask]
                            elif ask.cantidad > cantidad :
                                ask_cantidad_mayor += [ask]


                        if len(ask_cantidad_iguales) != 0 :
                            lista = self.prioridad(ask_cantidad_iguales)
                            monto = lista[0][0].precio * lista[0][0].cantidad
                            cantidad = ask.cantidad
                            diferencia = (order.precio*order.cantidad) - monto
                            id_ask = lista[0][0].id
                            id_bid = order.id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies,lista[0][0],monto,vendedor)
                            self.recibir_producto(currencies,order,cantidad,comprador)
                            self.reducir_ask(lista[0][0],cantidad)
                            self.reducir_bid(order,cantidad)
                            self.devolver_diferencia(currencies,order,diferencia)
                            self.valor = lista[0][0].precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de compra (bid) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Compraste {} {}".format(cantidad, self.ticket[:3]))
                                print("Entregaste como pago {} {}".format(monto, self.ticket[3:]))
                                print("Conseguiste comprar a un precio mas economico, por lo tanto recuperaste {} {}".format(diferencia,self.ticket[3:]))
                                print("----------------------------------------------")


                        elif len(ask_cantidad_mayor) != 0 :
                            lista = self.prioridad(ask_cantidad_mayor)
                            monto = lista[0][0].precio * order.cantidad
                            cantidad = order.cantidad
                            diferencia = (order.precio * order.cantidad) - monto
                            id_ask = lista[0][0].id
                            id_bid = order.id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies, lista[0][0], monto,vendedor)
                            self.recibir_producto(currencies, order, cantidad,comprador)
                            self.reducir_ask(lista[0][0], cantidad)
                            self.reducir_bid(order, cantidad)
                            self.devolver_diferencia(currencies, order, diferencia)
                            self.valor = lista[0][0].precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de compra (bid) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Compraste {} {}".format(cantidad, self.ticket[:3]))
                                print("Entregaste como pago {} {}".format(monto, self.ticket[3:]))
                                print("Conseguiste comprar a un precio mas economico, por lo tanto recuperaste {} {}".format(diferencia, self.ticket[3:]))
                                print("----------------------------------------------")


                        elif len(ask_cantidad_menor) != 0 :
                            lista = self.prioridad(ask_cantidad_menor)
                            monto = lista[0][0].precio * lista[0][0].cantidad
                            cantidad = lista[0][0].cantidad
                            diferencia = (order.precio * lista[0][0].cantidad) - monto
                            id_ask = lista[0][0].id
                            id_bid = order.id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies, lista[0][0], monto,vendedor)
                            self.recibir_producto(currencies, order, cantidad,comprador)
                            self.reducir_ask(lista[0][0], cantidad)
                            self.reducir_bid(order, cantidad)
                            self.devolver_diferencia(currencies, order, diferencia)
                            self.valor = lista[0][0].precio
                            if order.cantidad == 0 :
                                match = True
                                seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de compra (bid) realizo un match parcial!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Compraste {} {}".format(cantidad, self.ticket[:3]))
                                print("Entregaste como pago {} {}".format(monto, self.ticket[3:]))
                                print("Conseguiste comprar a un precio mas economico, por lo tanto recuperaste {} {}".format(diferencia, self.ticket[3:]))
                                print("----------------------------------------------")


                    elif len(ask_precios_iguales) != 0 :
                        ask_cantidad_iguales = []
                        ask_cantidad_mayor = []
                        ask_cantidad_menor = []
                        for ask in ask_precios_iguales:
                            if ask.cantidad == cantidad:
                                ask_cantidad_iguales += [ask]
                            elif ask.cantidad < cantidad:
                                ask_cantidad_menor += [ask]
                            elif ask.cantidad > cantidad:
                                ask_cantidad_mayor += [ask]


                        if len(ask_cantidad_iguales) != 0 :
                            lista = self.prioridad(ask_cantidad_iguales)
                            monto = lista[0][0].precio * lista[0][0].cantidad
                            cantidad = lista[0][0].cantidad
                            id_ask = lista[0][0].id
                            id_bid = order.id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies, lista[0][0], monto,vendedor)
                            self.recibir_producto(currencies, order, cantidad,comprador)
                            self.reducir_ask(lista[0][0], cantidad)
                            self.reducir_bid(order, cantidad)
                            self.valor = lista[0][0].precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de compra (bid) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Compraste {} {}".format(cantidad, self.ticket[:3]))
                                print("Entregaste como pago {} {}".format(monto, self.ticket[3:]))
                                print("----------------------------------------------")

                        elif len(ask_cantidad_mayor) != 0 :
                            lista = self.prioridad(ask_cantidad_mayor)
                            monto = lista[0][0].precio * order.cantidad
                            cantidad = order.cantidad
                            id_ask = lista[0][0].id
                            id_bid = order.id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies, lista[0][0], monto,vendedor)
                            self.recibir_producto(currencies, order, cantidad,comprador)
                            self.reducir_ask(lista[0][0], cantidad)
                            self.reducir_bid(order, cantidad)
                            self.valor = lista[0][0].precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de compra (bid) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Compraste {} {}".format(cantidad, self.ticket[:3]))
                                print("Entregaste como pago {} {}".format(monto, self.ticket[3:]))
                                print("----------------------------------------------")

                        elif len(ask_cantidad_menor) != 0 :
                            lista = self.prioridad(ask_cantidad_menor)
                            monto = lista[0][0].precio * lista[0][0].cantidad
                            cantidad = lista[0][0].cantidad
                            id_ask = lista[0][0].id
                            id_bid = order.id
                            vendedor = self.buscar_cliente(id_ask)
                            comprador = self.buscar_cliente(id_bid)
                            self.cobrar(currencies, lista[0][0], monto,vendedor)
                            self.recibir_producto(currencies, order, cantidad,comprador)
                            self.reducir_ask(lista[0][0], cantidad)
                            self.reducir_bid(order, cantidad)
                            self.valor = lista[0][0].precio
                            match = True
                            seguir = False

                            if permiso:
                                print("----------------------------------------------")
                                print("Tu order de compra (bid) realizo un match!")
                                print("La tasa de comision en este mercado es de {}".format(self.tasa))
                                print("Compraste {} {}".format(cantidad, self.ticket[:3]))
                                print("Entregaste como pago {} {}".format(monto, self.ticket[3:]))
                                print("----------------------------------------------")

                        else :
                            seguir = False
                            if permiso:
                                print("//////////////////////////////////////////////////")
                                print("No hay match para el siguiente ask:")
                                print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id, order.cantidad,self.ticket[:3],order.precio,self.ticket[3:]))
                                print("Esta order permanecera en el mercado esperando algun match")
                                print("//////////////////////////////////////////////////")
                                print("   ")

                    else :
                        seguir = False
                        if permiso:
                            print("//////////////////////////////////////////////////")
                            print("No hay match para el siguiente ask:")
                            print("[Order Id: {} , Cantidad: {} {} , Precio: {} {}] ".format(order.id, order.cantidad,self.ticket[:3],order.precio,self.ticket[3:]))
                            print("Esta order permanecera en el mercado esperando algun match")
                            print("//////////////////////////////////////////////////")
                            print("   ")

                if match :
                    hoy = dt.datetime.today()
                    fecha = dt.datetime.strftime(hoy, "%Y-%m-%d")
                    tiempo = strftime("%H:%M:%S", gmtime())
                    self.registro_acciones(str(order.id) + "/" + str(lista[0][0].id),fecha,tiempo,"Match")

    # Se encarga de registrar acciones y eventos en el sistema
    # Toda esta informacion termina en el archivo registros.csv
    def registro_acciones(self, *args):
        archivo = open("registros.csv", "a")
        msg = ""
        for arg in args:
            msg += str(arg) + ";"
        msg.strip(";")
        print(msg, file=archivo)
        archivo.close()



class Orders:

    def __init__(self,id,tipo,cantidad,precio,ticket,fecha,fecha_match=None):
        self.id = id
        self.tipo = tipo
        self.cantidad = cantidad
        self.precio = precio
        self.ticket = ticket
        self.fecha = fecha
        self.fecha_match = fecha_match



