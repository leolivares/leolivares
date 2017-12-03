import persons as per
import products as pro
from datetime import datetime, timedelta
from random import randint, expovariate, triangular, choice, random, sample, uniform
import time
from bisect import insort
from collections import deque, defaultdict
import variables as var

class Semestre:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.otros = 0
        self.alumnos = list()
        self.funcionarios = list()
        self.vendedores = list()
        self.carabineros = list()
        self.datos = dict()
        self.productos = {"Puesto de snacks": [],
                          "Puesto de comida china": [],
                          "Puesto de comida mexicana": []}

        self.dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes",
                     "Sabado", "Domingo"]
        self.dia_actual = ""
        self.gen_dia = self.dia_de_semana()
        self.dias_susto = 0

        self.fecha_inicio = datetime(2017, 1, 1)
        self.fecha_final = self.fecha_inicio + timedelta(days=120)
        self.fecha_actual = self.fecha_inicio

        self.tiempos_instalacion = list()
        self.llegada_miembros = list()
        self.tiempos_decision = list()
        self.tiempos_traslados = list()
        self.tiempos_snack = list()
        self.tiempos_revision = list()
        self.prox_temperatura = 0

        self.temperatura = None
        self.horarios_definidos = False

        self.n = 0
        self.prox_lluvia = None
        self.lluvia = False
        self.mas_enfermedad = False

        self.viernes_sin_concha = 0
        self.proba_concha = 0

        self.quickd = per.QuickDevil()
        self.prox_llamada = 0


        # Estadisticas
        self.vendedores_fiscalizados = 0
        self.dinero_confiscado = 0
        self.productos_vendidos = dict()
        self.ventas_diarias = [0]
        self.cantidad_confiscaciones = {"Mr. Hyde": 0, "Dr. Jekyll": 0}
        self.llamadas = 0
        self.concha_stereo = 0
        self.temp_extremas = 0
        self.lluvia_hamb = 0
        self.cantidad_hora = {"12:00-12:59": [0],
                              "13:00-13:59": [0],
                              "14:00-15:00": [0]}
        self.sin_almorzar = [0]
        self.suma_calidades = 0
        self.intox = 0
        self.descompuestos = 0
        self.abandono_cola = [0]
        self.sin_stock = list()
        self.engano = {"Mr. Hyde": 0, "Dr. Jekyll": 0}


    @property
    def actual(self):
        return self.fecha_actual

    @property
    def calcular_temperatura(self):
        """
        Calcula la proxima fecha que tendra temperaturas extremas
        """
        anio = self.actual.year
        mes = self.actual.month
        dia = self.actual.day
        self.prox_temperatura = (datetime(year=anio, month=mes, day=dia) +
                                 timedelta(days=randint(2, 20)))

    @property
    def calcular_lluvia(self):
        probabilidad = expovariate(21 - self.n)
        return probabilidad

    def numeros(self):
        i = 0
        while True:
            yield i
            i += 1

    def dia_de_semana(self):
        while True:
            for dia in self.dias:
                yield dia

    def obtener_parametros(self):
        """
        Realiza la lectura del archivo de parametros iniciales y guarda
        la informacion en un diccionario.
        """

        with open("parametros_iniciales.csv", "r") as archivo:
            lineas = [linea.strip().split(",") for linea in archivo]
            for conjunto in zip(lineas[0], lineas[1]):
                self.datos.update({conjunto[0].strip(): conjunto[1]})

        porcentajes = self.datos["distribución_almuerzo"].split(";")
        self.x = float(porcentajes[0])
        self.y = float(porcentajes[1])
        self.otros = 100 - (self.x + self.y)
        self.quickd.tasa_llamada = float(self.datos["llamado_policial"])
        self.dias_susto = float(self.datos["días_susto"])
        self.proba_concha = float(self.datos["concha_estéreo"])

    def obtener_personas(self):
        """
        Realiza la lectura del archivo de personas. Crea las instacias de cada
        persona y las almacena segun corresponda
        """
        with open("personas.csv", "r") as archivo:
            personas = [linea.strip().split(";") for linea in archivo]
        labels = personas.pop(0)
        number = self.numeros()
        dicc = {label.strip(): next(number) for label in labels}


        for persona in personas:
            if persona[dicc["Entidad"]].strip() == "Alumno":
                alumno = per.Alumno(self.datos["base_mesada"],
                                    self.datos["limite_paciencia"],
                                    persona[dicc["Vendedores de Preferencia"]]
                                    .strip(),
                                    self.datos["traslado_campus"],
                                    self.datos["moda_llegada_campus"],
                                    persona[dicc["Nombre"]].strip(),
                                    persona[dicc["Apellido"]].strip(),
                                    persona[dicc["Edad"]].strip())
                self.alumnos.append(alumno)

            elif persona[dicc["Entidad"]].strip() == "Funcionario":
                func = per.Funcionario(self.datos["dinero_funcionarios"],
                                       self.datos["moda_llegada_campus"],
                                       persona[dicc[
                                           "Vendedores de Preferencia"]]
                                       .strip(),
                                       self.datos["traslado_campus"],
                                       persona[dicc["Nombre"]].strip(),
                                       persona[dicc["Apellido"]].strip(),
                                       persona[dicc["Edad"]].strip())
                self.funcionarios.append(func)

            elif persona[dicc["Entidad"]].strip() == "Vendedor":
                ve = per.Vendedor(persona[dicc["Tipo Comida"]],
                                  self.datos["rapidez_vendedores"].split(";"),
                                  self.datos["stock_vendedores"],
                                  self.datos["probabilidad_permiso"],
                                  persona[dicc["Nombre"]].strip(),
                                  persona[dicc["Apellido"]].strip(),
                                  persona[dicc["Edad"]].strip())
                self.vendedores.append(ve)

            elif persona[dicc["Entidad"]].strip() == "Carabinero":
                personalidad = persona[dicc["Personalidad"]].strip()
                if personalidad == "Mr. Hyde":
                    data = self.datos["personalidad_hide"].split(";")
                elif personalidad == "Dr. Jekyll":
                    data = self.datos["personalidad_jekyll"].split(";")
                car = per.Carabinero(personalidad, float(data[0]),
                                     float(data[1]),
                                     persona[dicc["Nombre"]].strip(),
                                     persona[dicc["Apellido"]].strip(),
                                     persona[dicc["Edad"]].strip())
                self.carabineros.append(car)

    def obtener_productos(self):
        """
        Realiza la lectura del  archivo de productos, a partir del cual crea un
        diccionario con las instancias de cada producto, segun su lugar de
        venta. Estas instancias tendran los precios originales durante toda la
        simulacion.
        """
        with open("productos.csv", "r") as archivo:
            products = [linea.strip().split(";") for linea in archivo]
            labels = products.pop(0)
            numero = self.numeros()
            dicc = {label.strip(): next(numero) for label in labels}
            for product in products:
                self.productos[product[dicc["Vendido en"]].strip()]\
                    .append(pro.Producto(product[dicc["Producto"]].strip(),
                     product[dicc["Tipo"]].strip(),
                     product[dicc["Precio"]].strip(),
                     product[dicc["Calorias"]].strip(),
                     product[dicc["Tasa Putrefacción"]].strip()))

                self.productos_vendidos\
                    .update({product[dicc["Producto"]].strip(): list()})

    def definir_horarios(self):
        """
        Se encarga de asignar los horarios de almuerzo a los estudiantes,
        segun las probabilidades indicada en los parametros iniciales"
        """
        if not self.horarios_definidos :
            cantidad = len(self.funcionarios) + len(self.alumnos)
            percent_x = round((self.x / 100) * cantidad)
            percent_y = round((self.y / 100) * cantidad)
            percent_otros = round((self.otros / 100) * cantidad)
            horarios = list()

            for _ in range(percent_x):
                horarios.append(13)
            for _ in range(percent_y):
                horarios.append(14)
            for _ in range(percent_otros):
                horarios.append(12)

            while len(horarios) > 0:
                modulo = choice(horarios)
                horarios.remove(modulo)
                miembro = list(filter(lambda x: x.horario_almuerzo is None,
                               (self.alumnos + self.funcionarios)))[0]
                miembro.horario_almuerzo = modulo

        self.horarios_definidos = True

    @property
    def prox_instalacion(self):
        """
        Calcula el tiempo en minutos y el vendedor que realizaran la proxima
        instalacion.
        """
        cerrados = list(filter(lambda x: x[0].instalado is False and x[0].asustados == 0,
                               self.tiempos_instalacion))

        if len(cerrados) != 0:
            menor = cerrados[0]
            return (menor[0], menor[1])

        return (None, float("Inf"))


    @property
    def prox_arreglos(self):
        """
        Calcula el tiempo en minutos, para el inicio del proximo dia, es decir,
        00:00.
        """
        day , month, year = (self.actual.day + 1, self.actual.month,
                             self.actual.year)
        intentar = True
        while intentar:
            try :
                prox_fecha = datetime(year=year, month=month, day=day, hour=0,
                                      minute=0, second=0)
                intentar = False
            except ValueError:
                day = 1
                month += 1

        minutes_diff = (prox_fecha - self.actual).total_seconds() / 60.0
        return minutes_diff

    @property
    def prox_arreglo_mensual(self):
        """
        Calcula el tiempo en minutos para el inicio del proximo mes
        """

        if self.actual.day != 1:
            prox_fecha = datetime(year=self.actual.year,
                                  month=self.actual.month + 1,
                                  day=1,
                                  hour=0,
                                  minute=0,
                                  second=0)

            prox_fecha -= timedelta(seconds=1)

            minutes_diff = (prox_fecha - self.actual).total_seconds() / 60
            if minutes_diff == 0:
                return float("Inf")
            return minutes_diff
        return float("Inf")


    @property
    def prox_miembro_llega(self):
        """
        Calcula el tiempo en minutos del miembro que esta mas proximo a
        llegar a la universidad.
        :return:
        """
        cerrados = list(filter(lambda x: x[0].en_campus is False,
                               self.llegada_miembros))

        if len(cerrados) != 0:
            menor = cerrados[0]
            return (menor[0], menor[1])

        return (None, float("Inf"))

    @property
    def prox_cliente_atendido(self):
        """
        Calcula el tiempo en minutos, para que algun cliente comience a ser
        atendido por un vendedor o deje de ser atendido por un  vendedor.
        """
        tiempos = list()

        for vendedor in list(filter(lambda x: x.instalado is True,
                                    self.vendedores)):

            if len(vendedor.cola) != 0 and not vendedor.atendiendo:
                tiempos.append((vendedor, 0))

            elif len(vendedor.cola) != 0 and vendedor.atendiendo:
                tiempos.append((vendedor, vendedor.t_atencion))

            elif len(vendedor.cola) == 0 and vendedor.atendiendo:
                tiempos.append((vendedor, vendedor.t_atencion))

        if len(tiempos) != 0:
            return min(tiempos, key=lambda x: x[1])

        return (None, float("Inf"))

    @property
    def prox_decision(self):
        """
        Calcula el tiempo en minutos del proximo miembro que decidira almorzar.
        """

        posible = list(filter(lambda x: x[0].en_campus and not x[0].decidio
                                        and x[1] >= 0, self.tiempos_decision))
        if len(posible) != 0:
            return posible[0]
        return (None, float("Inf"))

    @property
    def prox_traslado(self):
        """
        Calcula el tiempo en minutos para que el proximo miembro termine de
        trasladarse a los puestos de comida
        """

        posible = list(filter(lambda x: x[0].decidio and x[1] >= 0 and
                                        not x[0].traslado, self.tiempos_traslados))
        if len(posible) != 0:
            return posible[0]

        return (None, float("Inf"))

    @property
    def prox_snack(self):
        """
        Calcula el tiempo en minutos para que el proximo estudiante compre un
        Snack
        """
        if len(self.tiempos_snack) != 0:
            return self.tiempos_snack[0]
        return (None, float("Inf"))

    @property
    def prox_revision(self):
        """
        Calcula el tiempo en minutos del proximo vendedor que sera revisado por
        un Carabinero
        """
        posibles = list(filter(lambda x: x[0].instalado and not x[0].revisado,
                               self.tiempos_revision))
        if len(posibles) != 0:
            return min(posibles, key=lambda x: x[1])
        return (None, float("Inf"))


    def preparar_producto(self, tipo, cant_stock):
        """
        Se encarga de entregar un diccionario con las cantidades de cada
        producto que tendra el vendedor. Segun el tipo de comida, se deciden
        al azar los productos y segun la cantidad de stock diario del vendedor.
        """
        dict_stock = defaultdict(int)

        if tipo == "Snack":
            vendido_en = "Puesto de snacks"
        elif tipo == "Mexicana":
            vendido_en = "Puesto de comida mexicana"
        else:
            vendido_en = "Puesto de comida china"

        for _ in range(cant_stock):
            producto = choice(self.productos[vendido_en])
            dict_stock[producto.nombre] += 1
        return dict_stock

    def definir_precios(self):
        """
        Se encarga de establecer un diccionario personal a cada vendedor,
        en donde estara reflejado los precios de sus productos.
        """
        tipos = {"Snack": "Puesto de snacks",
                 "China": "Puesto de comida china",
                 "Mexicana": "Puesto de comida mexicana"}

        for vendedor in self.vendedores:

            posibles = self.productos[tipos[vendedor.tipo_comida]]

            for product in posibles:
                vendedor.precios[product.nombre] += product.precio


    def definir_productos(self):
        """
        Entrega un diccionario a cada vendedor, para guardar informacion de sus
        productos, precios y aumentos por concha estereo
        """
        tipos = {"Snack": "Puesto de snacks",
                 "China": "Puesto de comida china",
                 "Mexicana": "Puesto de comida mexicana"}

        for vendedor in self.vendedores:
            vendedor.productos = {k.nombre: 0
                                  for k in self.productos[tipos[vendedor.tipo_comida]]}

            vendedor.precios = {k.nombre: 0
                                  for k in self.productos[tipos[vendedor.tipo_comida]]}

            vendedor.aumento_concha = {k.nombre: 0
                                  for k in self.productos[tipos[vendedor.tipo_comida]]}

    def arreglos_diarios(self):
        """
        Esta funcion se llama al inicio de cada dia. Su objetivo es devolver
        algunos parametros a su estado original, para llevar a cabo la
        simulacion del nuevo dia. Tambien se encarga de llamar a las respectivas
        funciones, para calcular algunos de los tiempos de los eventos del
        nuevo dia. Por ultimo, realiza algunas verificaciones para las
        distintas estadisticas.
        """

        if self.actual != datetime(year=2017,month=1,day=1):
            self.update_estadisticas()
            tiempo = self.prox_arreglos
            self.fecha_actual += timedelta(minutes=tiempo)
            self.reducir_tiempos(tiempo)

            if self.dia_actual in ["Lunes", "Martes", "Miercoles", "Jueves",
                                   "Viernes"]:
                for al in self.alumnos:
                    if al.almorzo is False:
                        self.sin_almorzar[-1] += 1

                for vend in self.vendedores:

                    restante = sum(map(lambda x: vend.productos[x],
                                       vend.productos))
                    if restante == 0:
                        self.sin_stock[-1] += restante
                        vend.cantidad_sin_stock += 1

                    if restante == vend.stock_inicial and vend.asustados == 0:
                        vend.dias_sin_vender += 1
                        vend.cant_todo_stock += 1
                        if vend.dias_sin_vender == 20:
                            vend.bancarrota = True
                            #print(vend.nombre, vend.apellido, "Estoy en bancarota")
                    else:
                        vend.dias_sin_vender = 0

        self.dia_actual = next(self.gen_dia)

        #print("Hoy es {} {}".format(self.dia_actual, self.actual))

        self.mas_enfermedad = False

        self.tiempos_revision = []
        self.tiempos_snack = []
        self.tiempos_traslados = []
        self.tiempos_instalacion = []
        self.tiempos_decision = []
        self.llegada_miembros = []

        if self.temperatura is not None:
            self.temperatura = None
        if self.lluvia is True:
            self.lluvia = False
            self.mas_enfermedad = True

        for alumno in self.alumnos:
            alumno.dinero = alumno.mesada / 20
            alumno.calcular_paciencia
            alumno.en_campus = False
            alumno.decidio = False
            alumno.almorzo = False
            alumno.traslado = False
            alumno.siendo_atendido = False

        for funcionario in self.funcionarios:
            funcionario.dinero = funcionario.base_dinero
            funcionario.en_campus = False
            funcionario.almorzo = False
            funcionario.decidio = False
            funcionario.traslado = False
            funcionario.siendo_atendido = False

        for vendedor in self.vendedores:

            if vendedor.asustados == 0 and not vendedor.bancarrota :
                vendedor.stock_inicial = vendedor.calcular_stock
                vendedor.productos = self.preparar_producto(vendedor.tipo_comida,
                                                            vendedor.stock_inicial)
            vendedor.instalado = False
            vendedor.atendiendo = None
            vendedor.revisado = False
            if vendedor.asustados > 0:
                vendedor.asustados -= 1

            for product in vendedor.productos:
                if vendedor.aumento_concha[product] > 0:
                    vendedor.precios[product] -= vendedor.aumento_concha[product]
                    vendedor.aumento_concha[product] = 0

        if self.actual == self.prox_temperatura:
            self.temperatura_extrema()
            self.n = 0
        else:
            self.n += 1

        if random() <= self.calcular_lluvia and not self.temperatura:
            self.lluvia = True
            self.lluvia_hamb += 1
            for al in self.alumnos:
                al.almorzo = True

        if self.dia_actual not in ["Sabado", "Domingo"]:

            for vendedor in self.vendedores:
                if not vendedor.bancarrota and vendedor.asustados == 0:
                    insort(self.tiempos_instalacion,
                           (vendedor, self.calcular_instalacion(vendedor)))


            for miembro in self.alumnos + self.funcionarios:
                insort(self.llegada_miembros,
                       (miembro, self.calcular_llegada(miembro)))

                if not self.lluvia:
                    insort(self.tiempos_decision,
                           (miembro, self.calcular_decision(miembro)))

            if self.dia_actual == "Viernes":
                if random() <= self.proba_concha or\
                                self.viernes_sin_concha == 4:
                    self.concha_stereo += 1
                    self.aumento_de_precios()
                    self.viernes_sin_concha = 0
                else:
                    self.viernes_sin_concha += 1

    def arreglos_mensuales(self):

        """
        Esta funcion es parecida a la anterior, solo que ocurre al inicio de
        cada mes. Se encarga de hacer los calculos estadisticos necesarios,
        verificar aumentos de precios, calcular las nuevas mesadas.
        """
        if self.prox_temperatura == 0:
            self.calcular_temperatura

        for alumno in self.alumnos:
            alumno.calcular_mesada
            alumno.dinero = alumno.mesada / 20

        for vendedor in self.vendedores:

            for product in vendedor.productos:
                inicial = vendedor.precios[product]
                aumento = vendedor.precios[product] * ((vendedor.cantidad_sin_stock * 6) / 100)
                disminucion = vendedor.precios[product] * ((vendedor.cant_todo_stock * 5) / 100)
                vendedor.precios[product] += aumento
                vendedor.precios[product] -= disminucion

                porcentaje = (inicial - vendedor.precios[product] / inicial) * 100

            self.verificar_precios(vendedor)

            vendedor.cant_todo_stock = 0
            vendedor.cantidad_sin_stock = 0

        if not self.horarios_definidos:
            self.definir_horarios()
            self.prox_llamada = (round(expovariate(self.quickd.tasa_llamada)) * 1440) + 1
            self.definir_productos()
            self.definir_precios()

        else:
            tiempo = self.prox_arreglo_mensual
            self.fecha_actual += timedelta(minutes=tiempo)
            self.reducir_tiempos(tiempo)

            if len(self.sin_almorzar) <= 3:
                self.sin_almorzar.append(0)

    def aumento_de_precios(self):
        """
        Se encarga de aumentar el precio de los productos de los vendedore,
        en un 25%, por la concha estereo. Este aumento se guarda en un
        diccionario, para que al dia siguiente sea reestablecido
        """
        for vendedor in self.vendedores:
            for product in vendedor.productos:
                aumento = vendedor.precios[product] * 0.25
                vendedor.aumento_concha[product] = aumento
                vendedor.precios[product] += aumento

    def verificar_precios(self, vendedor):
        """
        Se encarga de verificar que los precios de los productos no bajen a un
        valor menor del 1% del original.
        """
        tipos = {"Snack": "Puesto de snacks",
                 "China": "Puesto de comida china",
                 "Mexicana": "Puesto de comida mexicana"}

        for product in vendedor.precios:
            precio_original = list(filter(lambda x: x.nombre == product,
                                          self.productos[tipos[vendedor.tipo_comida]]))[0].precio

            if vendedor.precios[product] < (precio_original * 0.1):
                vendedor.precios[product] = precio_original * 0.1


    def calcular_instalacion(self, vendedor):
        """
        Retorna el tiempo en minutos en la que el vendedor se instalara
        """
        base = vendedor.hora_instalacion
        minutes_diff = 0
        if self.actual.time() < (datetime(1,1,1) + timedelta(hours=11)).time():

            prox_fecha = datetime(year=self.actual.year,
                                  month=self.actual.month,
                                  day=self.actual.day,
                                  hour=var.INSTALACION,
                                  minute=0,
                                  second=0)

            minutes_diff = (prox_fecha - self.actual).total_seconds() / 60.0

        return base + minutes_diff

    def calcular_decision(self, miembro):
        """
        Retorna el tiempo en minutos en la que el miebro decidira almorzar.
        """
        base = miembro.tiempo_decision
        minutes_diff = 0

        if self.actual.time() < (datetime(1, 1, 1) + timedelta(hours=miembro.horario_almuerzo)).time():

            prox_fecha = datetime(year=self.actual.year,
                                  month=self.actual.month,
                                  day=self.actual.day,
                                  hour=miembro.horario_almuerzo,
                                  minute=10,
                                  second=0)

            minutes_diff = (prox_fecha - self.actual).total_seconds() / 60.0

        return base + minutes_diff

    def calcular_llegada(self, miembro):
        """
        Retorna el tiempo en minutos en la que el miebro llegara a la
        universidad.
        """
        base = miembro.tiempo_llegada
        minutes_diff = 0
        if self.actual.time() < (datetime(1,1,1) + timedelta(hours=11)).time():

            prox_fecha = datetime(year=self.actual.year,
                                  month=self.actual.month,
                                  day=self.actual.day,
                                  hour=var.LLEGADA_MIEMBROS,
                                  minute=0,
                                  second=0)

            minutes_diff = (prox_fecha - self.actual).total_seconds() / 60.0

        return base + minutes_diff

    def calcular_tiempo_snack(self, miembro):
        """
        Retorna el tiempo en minutos en la que el miebro comprara un Snack.
        """
        prox_fecha = datetime(year=self.actual.year,
                              month=self.actual.month,
                              day=self.actual.day,
                              hour=15,
                              minute=0,
                              second=0)

        minutes_diff = (prox_fecha - self.actual).total_seconds() / 60.0

        insort(self.tiempos_snack, (miembro, uniform(0, minutes_diff)))

    def realizar_instalacion(self):
        """
        Instala al vendedor que corresponda y actualiza el tiempo.
        """
        vendedor , tiempo = self.prox_instalacion
        self.fecha_actual += timedelta(minutes=tiempo)

        self.reducir_tiempos(tiempo)

        vendedor.instalado = True
        #print("{}: Abri el puesto a las {}".format(vendedor.nombre,
                                                  #self.actual.time()))

    def llega_miembro(self):
        """
        Llega el miembro y actualiza el tiempo. Verifica si el miembro
        comprara un Snack ese dia.
        """
        miembro, tiempo = self.prox_miembro_llega
        self.fecha_actual += timedelta(minutes=tiempo)

        self.reducir_tiempos(tiempo)

        miembro.en_campus = True
        #print("{}: Soy {} y llegue a las {}".format(miembro.nombre, miembro.__class__.__name__, self.actual.time()))

        if random() <= 0.5 and not self.lluvia:
            self.calcular_tiempo_snack(miembro)

    def atender_cliente(self):
        """
        Se atiende al siguiente cliente y actualiza el tiempo. Segun el caso,
        el proximo cliente en la fila comienza a ser atendido. Se le entrega
        el producto al cliente que deja de ser atendido.
        """
        vendedor, tiempo = self.prox_cliente_atendido
        self.fecha_actual += timedelta(minutes=tiempo)

        if vendedor.atendiendo and len(vendedor.cola) == 0:
            cliente = vendedor.atendiendo

            if not isinstance(cliente, per.Carabinero):

                product = self.obtener_producto(vendedor, cliente)

                vendedor.productos[product.nombre] -= 1

                #print("El cliente {} ha sido atendido".format(cliente.nombre))
                self.comer(cliente, product, vendedor)

            vendedor.atendiendo = None
            vendedor.t_atencion = 0


        elif vendedor.atendiendo and len(vendedor.cola) != 0:
            cliente = vendedor.atendiendo

            if not isinstance(cliente, per.Carabinero):

                product = self.obtener_producto(vendedor, cliente)

                vendedor.productos[product.nombre] -= 1
                #print("El cliente {} ha sido atendido".format(vendedor.atendiendo.nombre))
                self.comer(cliente, product, vendedor)

            vendedor.atendiendo = vendedor.cola.popleft()
            vendedor.t_atencion = vendedor.velocidad
            #print("El cliente {} comenzo a ser atendido".format(vendedor.atendiendo.nombre))

        elif not vendedor.atendiendo and len(vendedor.cola) != 0:
            cliente = vendedor.cola.popleft()
            vendedor.atendiendo = cliente
            vendedor.t_atencion = vendedor.velocidad
            #print("El cliente {} comenzo a ser atendido".format(cliente.nombre))

        self.reducir_tiempos(tiempo)

    def obtener_producto(self, vendedor, cliente):
        """
        Segun el cliente, se selecciona un producto posible. Para los funciona
        rios, se busca el de mayor calidad
        """
        tipos = {"Snack": "Puesto de snacks",
                 "China": "Puesto de comida china",
                 "Mexicana": "Puesto de comida mexicana"}

        if isinstance(cliente, per.Alumno):

            products = list(filter(lambda x: vendedor.productos[x] > 0
                                        and vendedor.precios[x] <= cliente.dinero,
                              vendedor.productos))

            product_name = choice(products)

            product = list(filter(lambda x: x.nombre == product_name,
                                  self.productos[tipos[vendedor.tipo_comida]]))[0]


        elif isinstance(cliente, per.Funcionario):

            products = list(filter(lambda x: vendedor.precios[x] <= cliente.dinero and vendedor.productos[x] > 0,
                                   vendedor.productos))

            posibles = list(map(lambda x: (x, x.calcular_calidad(x.calcular_putrefaccion(self.tiempo_putre(), self.temperatura), self.temperatura, vendedor.precios[x.nombre])),
                          filter(lambda x: x.nombre in products, self.productos[tipos[vendedor.tipo_comida]])))

            product = max(posibles, key=lambda x: x[1])[0]

        return product

    def comer(self, cliente, producto, vendedor):
        """
        El cliente obtiene el producto. Se verfifica si se enfermo, y de ser
        asi, se modifica su lista de preferencias. Se actualizan estadisticas
        """
        self.ventas_diarias[-1] += 1

        if isinstance(vendedor, per.Vendedor):
            cliente.dinero -= vendedor.precios[producto.nombre]
        else:
            for puesto in self.productos:
                for product in self.productos[puesto]:
                    if product.nombre == producto.nombre:
                        cliente.dinero -= product.precio

        if producto.tipo != "Snack":
            cliente.almorzo = True

            if self.actual.hour >= 12 and self.actual.hour < 13:
                self.cantidad_hora["12:00-12:59"][-1] += 1
            elif self.actual.hour >= 13 and self.actual.hour < 14:
                self.cantidad_hora["13:00-13:59"][-1] += 1
            elif self.actual.hour >= 14 and self.actual.hour <= 15:
                self.cantidad_hora["14:00-15:00"][-1] += 1

        tiempo_putre = self.tiempo_putre()
        #print("{} se ha comido un {} a las {}".format(cliente.nombre, producto.nombre, self.actual.time()))
        putrefaccion = producto.calcular_putrefaccion(tiempo_putre,
                                                      self.temperatura)

        if not isinstance(vendedor, per.QuickDevil):
            calidad = producto.calcular_calidad(putrefaccion, self.temperatura, vendedor.precios[producto.nombre])
        else:
            calidad = producto.calcular_calidad(putrefaccion, self.temperatura)

        self.suma_calidades += calidad

        probabilidad = 0.35
        if self.mas_enfermedad:
            probabilidad = 0.7

        if putrefaccion >= 0.75:
            self.descompuestos += 1

        if calidad <= 0.2 and random() <= probabilidad:
            #print("El {} {} se ha enfermado".format(cliente.__class__.__name__, cliente.nombre))

            self.intox += 1
            if not isinstance(vendedor, per.QuickDevil):
                cliente.preferencias.remove(
                    vendedor.nombre + " " + vendedor.apellido)

                #print("{}: Ya no comere mas en el puesto de {}".format(cliente.nombre, vendedor.nombre + " " + vendedor.apellido))

    def tiempo_putre(self):
        """
        Retorna el tiempo en minutos, desde la 8:00 am de ese dia
        """
        anio = self.actual.year
        mes = self.actual.month
        dia = self.actual.day
        desde = datetime(year=anio, month=mes, day=dia) + \
                timedelta(hours=var.INICIO_PUTRE)

        min_diff = (self.actual - desde).total_seconds() / 60.0

        return min_diff


    def reducir_tiempos(self, minutos):
        """
        Se encarga de reducir los tiempos correspondientes, cuando ocurre
        algun evento.
        """
        self.tiempos_instalacion = list(map(lambda x: (x[0], x[1] - minutos),
                                            self.tiempos_instalacion))

        self.llegada_miembros = list(map(lambda x: (x[0], x[1] - minutos),
                                            self.llegada_miembros))

        self.tiempos_decision = list(map(lambda x: (x[0], x[1] - minutos),
                                            self.tiempos_decision))

        self.tiempos_traslados = list(map(lambda x: (x[0], x[1] - minutos),
                                            self.tiempos_traslados))

        self.tiempos_snack = list(map(lambda x: (x[0], x[1] - minutos),
                                            self.tiempos_snack))

        self.tiempos_revision = list(map(lambda x: (x[0], x[1] - minutos),
                                            self.tiempos_revision))

        self.prox_llamada -= minutos

        for vendedor in self.vendedores:
            if vendedor.atendiendo:
                vendedor.t_atencion -= minutos

    def comprar(self, miembro, tipo):
        """
        Busca un puesto en donde el miembro pueda comprar. En caso de ser
        necesario, se compra en el QuickDevil
        """
        if tipo == "Snack":
            posibles = list(filter(lambda x: x.instalado == True,
                                   filter(lambda x: x.tipo_comida == "Snack",
                                          filter(lambda x:
                                                 (x.nombre + " " + x.apellido)
                                                 in miembro.preferencias,
                                                 self.vendedores))))

        elif tipo == "Fondo":
            posibles = list(filter(lambda x: x.instalado == True,
                                   filter(lambda x: x.tipo_comida == "China" or
                                                    x.tipo_comida == "Mexicana",
                                          filter(lambda x:
                                                 (x.nombre + " " + x.apellido)
                                                 in miembro.preferencias,
                                                 self.vendedores))))

        if len(posibles) != 0:
            en_fila = False
            while not en_fila and len(posibles) != 0:
                vend = posibles[0]
                posibles.pop(0)
                if self.cumple_condiciones(vend, miembro):
                    self.insertar_a_cola(vend, miembro)

                    #print("{} ha entrado a la fila de {} para comprar {}"
                          #.format(miembro.nombre, vend.nombre, tipo))
                    en_fila = True

        else:
            #print("{}: Tendre que comprar en QuickDevil".format(miembro.nombre))
            self.compra_quickdevil(miembro, tipo)

    def compra_quickdevil(self, miembro, tipo):
        """
        El cliente es atendido en el QuickDevil.
        """
        product = None
        if tipo == "Snack":

            posibles_products = list(filter(lambda x: x.precio <= miembro.dinero,
                                       self.productos["Puesto de snacks"]))

            if len(posibles_products) != 0:
                product = choice(posibles_products)

        elif tipo == "Fondo":
            posibles_products = list(filter(lambda x: x.precio <= miembro.dinero,
                                            self.productos["Puesto de comida mexicana"] + self.productos["Puesto de comida china"]))

            if len(posibles_products) != 0:
                product = choice(posibles_products)

        if product:
            self.comer(miembro, product, self.quickd)


    def insertar_a_cola(self, vendedor, cliente):
        """
        Se agrega al cliente a la cola. Si el cliente es un Fucionario, se
        verifica que los demas deseen seguir en la cola.
        """
        if isinstance(cliente, per.Funcionario) and len(vendedor.cola) != 0:
            i = 0
            adentro = False
            while i < len(vendedor.cola):
                if not isinstance(vendedor.cola[i], per.Funcionario) and not adentro:
                    vendedor.cola.insert(i, cliente)
                    adentro = True
                    self.seguir_en_cola(vendedor)
                i += 1
        else:
            vendedor.cola.append(cliente)

    def cumple_condiciones(self, vend, miembro):
        """
        Verifica que el puesto del vendedor cumpla las condiciones para que el
        miembro compre.
        """
        cant_disp = sum(map(lambda x: vend.productos[x], vend.productos))

        if cant_disp > len(vend.cola):


            menor_precio = min(list(map(lambda x: vend.precios[x],
                                        filter(lambda x: vend.productos[x] > 0,
                                               vend.productos))))

            if miembro.dinero >= menor_precio:
                tiempo_a_esperar = (vend.velocidad * len(vend.cola)) + vend.t_atencion
                if tiempo_a_esperar < miembro.limite_paciencia:
                    return True
        return False

    def temperatura_extrema(self):
        """
        Determina que clase de temperatura extrema habra ese dia.
        """
        self.temp_extremas += 1

        self.calcular_temperatura
        if choice(["Frio", "Calor"]) == "Frio":
            self.temperatura = "Frio"
        else:
            self.temperatura = "Calor"

    def decidir_comer(self):
        """
        El miembro correspondiente decide ir a comer, con lo cual se calcula el
        tiempo de traslado a los puestos de comida
        """
        miembro, tiempo = self.prox_decision
        miembro.decidio = True

        #print("El {} {} ha decidido ir a comer a las {}".
              #format(miembro.__class__.__name__, miembro.nombre,
                     #self.fecha_actual.time()))

        self.fecha_actual += timedelta(minutes=tiempo)
        self.reducir_tiempos(tiempo)
        miembro.decidio = True

        tiempo_traslado = expovariate(miembro.tasa_traslado)

        insort(self.tiempos_traslados, (miembro, tiempo_traslado))

    def trasladarse(self):
        """
        El tiempo de traslado del miembro se ha cumplido, por lo que procede
        a comprar en uno de los puestos, en caso de que pueda.
        """
        miembro, tiempo = self.prox_traslado
        #print("{} se ha trasladado a los puestos de comida a las {}"
              #.format(miembro.nombre, self.actual.time()))

        self.fecha_actual += timedelta(minutes=tiempo)
        self.reducir_tiempos(tiempo)
        miembro.traslado = True

        self.comprar(miembro, "Fondo")

    def comprar_snack(self):
        """
        Se encarga de que el miembro correspondiente, que decidio comprar ese
        dia Snack, lo compre.
        :return:
        """
        miembro, tiempo = self.prox_snack
        #print("{} comprara un Snack".format(miembro.nombre, self.actual.time()))

        self.fecha_actual += timedelta(minutes=tiempo)
        self.tiempos_snack.remove((miembro, tiempo))
        self.reducir_tiempos(tiempo)

        self.comprar(miembro, "Snack")

    def seguir_en_cola(self, vendedor):
        """
        Revisa a cada miembro que este en la cola del vendedor, y verifica que
        desee seguir en la cola. Esta funcion se activa si entra un funcionario
        o si un carabinero comienza a revisar el puesto. En caso de que el
        miembro decida salir, vuelve a intentar comprar en otro puesto.
        """
        i = 0
        for cliente in vendedor.cola:

            tiempo_espera = vendedor.t_atencion + (i * vendedor.velocidad)

            menor_precio = min(list(map(lambda x: vendedor.precios[x],
                                        filter(lambda x: vendedor.productos[
                                                             x] > 0,
                                               vendedor.productos))))

            cantidad_disp = sum(map(lambda x: vendedor.productos[x],
                                    vendedor.productos))

            if tiempo_espera > cliente.limite_paciencia or\
                            menor_precio > cliente.dinero or\
                            cantidad_disp < (i + 1):

                self.abandono_cola[-1] += 1
                #print("El cliente {} ha decidido dejar la cola".format(cliente.nombre))

                cliente.limite_paciencia -= 5
                cola_lista = list(vendedor.cola)
                cola_lista.insert(i, False)
                cola_lista.pop(i + 1)
                vendedor.cola = deque(cola_lista)

                if vendedor.tipo_comida == "Mexicana" or\
                                vendedor.tipo_comida == "China":
                    tipo = "Fondo"
                else:
                    tipo = "Snack"

                self.comprar(cliente, tipo)
                i -= 1

            cola_final = deque(filter(lambda x: x is not False, vendedor.cola))
            vendedor.cola = cola_final

            i += 1

    def llamar(self):
        """
        Se realiza la llamada a los Carabineros. Se calculan los tiempos en
        que revisaran cada puesto, a partir de las 13:00. Se calcula el tiempo
        para la proxima llamada.
        """
        #print("Nebil ha decidido el dia de hoy llamar a los carabineros! {}".format(self.actual.time()))
        self.llamadas += 1

        tiempo = self.prox_llamada
        self.fecha_actual += timedelta(minutes=tiempo)
        self.reducir_tiempos(tiempo)

        prox_fecha = datetime(year=self.actual.year,
                              month=self.actual.month,
                              day=self.actual.day,
                              hour=13,
                              minute=0,
                              second=0)

        minutes_diff = (prox_fecha - self.actual).total_seconds() / 60.0
        vendedores = list(filter(lambda x: x.bancarrota is False and
                                           x.asustados == 0, self.vendedores))

        cant_vendedores = len(vendedores)

        if cant_vendedores != 0:
            tiempo_por_puesto = 40 / cant_vendedores

            tiempos_revision = [minutes_diff + (tiempo_por_puesto * i)
                                     for i in range(1, cant_vendedores + 1)]

            random_vend = sample(vendedores, len(vendedores))

            self.tiempos_revision = [(k, v) for k, v in zip(random_vend,
                                                            tiempos_revision)]

        self.prox_llamada = self.quickd.calcular_llamada

    def revisar(self):
        """
        El carabinero pasa a ser "atendido" por el vendedor. Se verifica que
        tenga permiso y una cantidad de sus productos. En caso de que decida
        fiscalizar, se el vendedor se ausentara una cierta cantidad de dias y
        las personas en su cola pasaran a comprar en otro puesto.
        """
        vendedor, tiempo = self.prox_revision

        vendedor.revisado = True
        self.fecha_actual += timedelta(minutes=tiempo)
        self.reducir_tiempos(tiempo)

        tiempo_por_puesto = len(list(filter(lambda x: x.instalado, self.vendedores))) / 40
        carabinero = choice(self.carabineros)

        #print("El vendedor {} comenzo a ser revisado por {} (Personalidad: {}) a las {}".format(
            #vendedor.nombre, carabinero.nombre, carabinero.personalidad, self.actual.time()))

        if vendedor.atendiendo:
            vendedor.cola.insert(0, vendedor.atendiendo)
            vendedor.atendiendo = carabinero
            vendedor.t_atencion = tiempo_por_puesto

            self.seguir_en_cola(vendedor)

        fiscalizar = False
        if not vendedor.permiso:
            if random() <= carabinero.prob_engano:
                #print("{} no tiene permiso, pero ha engañado al carabinero".format(vendedor.nombre, carabinero.nombre))
                self.engano[carabinero.personalidad] += 1
            else:
                #print("{} no tiene permiso, y sus productos seran fiscalizados".format(vendedor.nombre))
                fiscalizar = True

        if not fiscalizar:

            tipos = {"Snack": "Puesto de snacks",
                     "China": "Puesto de comida china",
                     "Mexicana": "Puesto de comida mexicana"}

            cant_revisar = round(carabinero.tasa_productos *
                                 len(vendedor.productos))
            productos_disponibles = list(filter(lambda x: vendedor.productos[x]
                                                          > 0,
                                                vendedor.productos))
            productos_a_revisar = sample(productos_disponibles, cant_revisar)

            productos_a_revisar = list(filter(lambda x: x.nombre in
                                                        productos_a_revisar,
                                      self.productos[tipos[
                                          vendedor.tipo_comida]]))

            for product in productos_a_revisar:
                putre = product.calcular_putrefaccion(self.tiempo_putre(),
                                                      self.temperatura)
                if product.calcular_calidad(putre, self.temperatura,
                                            vendedor.precios[product.nombre])\
                        <= var.DESCOMPUESTO:
                    fiscalizar = True

            if fiscalizar:
                pass
                #print("{} tiene productos en mal estado y por lo tanto sera fiscalizado".format(vendedor.nombre))

        if fiscalizar:
            dinero_confiscado = sum(map(lambda x: vendedor.productos[x]
                                                  * vendedor.precios[x],
                                        vendedor.productos))

            self.dinero_confiscado += dinero_confiscado
            self.cantidad_confiscaciones[carabinero.personalidad] += 1

            #print("Se le ha confiscado {} al vendedor {}"
                  #.format(dinero_confiscado, vendedor.nombre))

            vendedor.instalado = False
            vendedor.asustados = self.dias_susto
            vendedor.productos = []

            if vendedor.tipo_comida == "Snack":
                tipo = "Snack"
            else:
                tipo = "Fondo"

            for cliente in vendedor.cola:
                self.comprar(cliente, tipo)

            vendedor.cola = deque()

    def update_estadisticas(self):
        """
        Esta funcion se encarga de modificar las estructuras que almacenan
        las estadisticas, en caso de ser necesario.
        """
        self.ventas_diarias.append(0)

        for product in self.productos_vendidos:
            self.productos_vendidos[product].append(0)

        if self.dia_actual in ["Lunes", "Martes", "Miercoles", "Jueves",
                               "Viernes"]:

            for hora in self.cantidad_hora:
                self.cantidad_hora[hora].append(0)

            self.abandono_cola.append(0)

        self.sin_stock.append(0)


    def imprimir_estadisticas(self, printear):
        """
        Se encarga de obtener las estadisticas que se deben mostrar. Si es
        necesario, las imprime en consola. En caso de ser utilizada la simula
        cion para los escenarios, retorna las estadisticas en un diccionario.
        """
        num_confis = sum(map(lambda x: self.cantidad_confiscaciones[x],
                             self.cantidad_confiscaciones))
        promedio_confis = 0
        if num_confis != 0:
            promedio_confis = self.dinero_confiscado / num_confis
        minimo = min(list(filter(lambda x: x > 0, self.ventas_diarias)))
        maximo = max(self.ventas_diarias)
        prom_ventas = sum(self.ventas_diarias) / len(self.ventas_diarias)
        confis_jekyll = self.cantidad_confiscaciones["Dr. Jekyll"]
        confis_hyde = self.cantidad_confiscaciones["Mr. Hyde"]
        prom_12 = sum(self.cantidad_hora["12:00-12:59"]) / len(
            self.cantidad_hora["12:00-12:59"])
        prom_13 = sum(self.cantidad_hora["13:00-13:59"]) / len(
            self.cantidad_hora["13:00-13:59"])
        prom_14 = sum(self.cantidad_hora["14:00-15:00"]) / len(
            self.cantidad_hora["14:00-15:00"])
        calidad_prom = self.suma_calidades / sum(self.ventas_diarias)
        abandono_prom = sum(self.abandono_cola) / len(self.abandono_cola)
        sin_stock_prom = sum(self.sin_stock) / len(self.sin_stock)


        if printear:

            print("Estadisticas:")
            print("1. Cantidad promedio de dinero confiscado a los vendedores.")
            print("     {}$".format(promedio_confis))
            print("2. Cantidad minima, maxima y promedio por productos vendidos durante un d́ıa.")
            print("     Minimo: {}".format(minimo))
            print("     Maximo: {}".format(maximo))
            print("     Promedio: {}".format(prom_ventas))
            print("3. Cantidad de confiscaciones por tipo de Carabinero.")
            print("     Dr. Jekyll: {} confiscaciones".format(confis_jekyll))
            print("     Mr. Hyde: {} confiscaciones".format(confis_hyde))
            print("4. Numero de llamadas realizadas por QuickDevil.")
            print("     Cantidad: {}".format(self.llamadas))
            print("5. Numero de veces que se realizo la Concha Estereo.")
            print("     Cantidad: {}".format(self.concha_stereo))
            print("6. Numero de veces donde hubo Temperaturas Extremas.")
            print("     Cantidad: {}".format(self.temp_extremas))
            print("7. Numero de veces donde hubo Lluvia de Hamburguesas.")
            print("     Cantidad: {}".format(self.lluvia_hamb))
            print("8. Cantidad promedio de personas que almorzaron, por hora.")
            print("     12:00-12:59: {}".format(prom_12))
            print("     13:00-13:59: {}".format(prom_13))
            print("     14:00-15:00: {}".format(prom_14))
            print("9. Cantidad de Alumnos que no almorzo por mes.")
            print("     Mes 1: {}".format(self.sin_almorzar[0]))
            print("     Mes 2: {}".format(self.sin_almorzar[1]))
            print("     Mes 3: {}".format(self.sin_almorzar[2]))
            print("     Mes 4: {}".format(self.sin_almorzar[3]))
            print("10. Calidad Promedio de los productos por escenario")
            print("     Promedio: {}".format(calidad_prom))
            print("11. Cantidad de miembros UC intoxicados")
            print("     Cantidad: {}".format(self.intox))
            print("12. Cantidad de Productos descompuestos")
            print("     Cantidad: {}".format(self.descompuestos))
            print("13. Promedio diario de miembros UC que abandonan colas.")
            print("     Promedio: {}".format(abandono_prom))
            print("14. Promedio diario de vendedores sin stock.")
            print("     Promedio: {}".format(sin_stock_prom))
            print("15. Cantidad de engaños a Carabineros.")
            print("     Dr. Jekyll: {}".format(self.engano["Dr. Jekyll"]))
            print("     Mr. Hyde: {}".format(self.engano["Mr. Hyde"]))

        else:

            results = {1: promedio_confis, 2: minimo, 3: maximo, 4: prom_ventas,
                    5: confis_jekyll, 6: confis_hyde, 7: self.llamadas,
                    8: self.concha_stereo, 9: self.temp_extremas,
                    10: self.lluvia_hamb, 11: prom_12, 12: prom_13, 13: prom_14,
                    14: self.sin_almorzar[0] + self.sin_almorzar[1] +
                        self.sin_almorzar[2] + self.sin_almorzar[2],
                    15: calidad_prom, 16: self.intox, 17: self.descompuestos,
                    18: abandono_prom, 19: sin_stock_prom,
                    20: self.engano["Dr. Jekyll"], 21: self.engano["Mr. Hyde"]}
            return results

    @property
    def prox_evento(self):
        """
        Determina cual sera el proximo evento que ocurrira
        """
        eventos = ["arreglos diarios",
                   "arreglos mensuales",
                   "instalacion",
                   "llega miembro",
                   "atender cliente",
                   "decidir comer",
                   "trasladarse",
                   "snack",
                   "llamada",
                   "revision"]

        tiempos = [self.prox_arreglos,
                   self.prox_arreglo_mensual,
                   self.prox_instalacion[1],
                   self.prox_miembro_llega[1],
                   self.prox_cliente_atendido[1],
                   self.prox_decision[1],
                   self.prox_traslado[1],
                   self.prox_snack[1],
                   self.prox_llamada,
                   self.prox_revision[1]]

        tiempo_prox_evento = min(tiempos)

        return eventos[tiempos.index(tiempo_prox_evento)]

    def run(self, printear=True):
        """
        Comienza la simmulacion, y continua hasta que el tiempo actual alcanza
        el tiempo final. (120 dias)
        """

        self.arreglos_mensuales()
        self.arreglos_diarios()

        while self.actual.date() <= self.fecha_final.date():

            evento = self.prox_evento

            if evento == "arreglos diarios":
                self.arreglos_diarios()
            elif evento == "arreglos mensuales":
                self.arreglos_mensuales()
            elif evento == "instalacion":
                self.realizar_instalacion()
            elif evento == "llega miembro":
                self.llega_miembro()
            elif evento == "atender cliente":
                self.atender_cliente()
            elif evento == "decidir comer":
                self.decidir_comer()
            elif evento == "trasladarse":
                self.trasladarse()
            elif evento == "snack":
                self.comprar_snack()
            elif evento == "llamada":
                self.llamar()
            elif evento == "revision":
                self.revisar()

        results = self.imprimir_estadisticas(printear)

        if results:
            return results

if __name__ == "__main__":

    semestre= Semestre()
    semestre.obtener_parametros()
    semestre.obtener_personas()
    semestre.obtener_productos()
    semestre.run()






