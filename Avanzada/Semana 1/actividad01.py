class Ciudad:
    def __init__(self, nombre):
        self.nombre = nombre
        self.comunas = []

    def agregar_comuna(self, comuna):
        self.comunas += [comuna]

    def estadisticas(self):
        cant, depend = self.cant_total()
        print(
            "Hay {} medidores en la ciudad de Santiago , {} electrodependientes".format(
                cant, depend))
        for comuna in self.comunas:
            comuna.estadistica()
            for casa in comuna.casas:
                casa.estadistica()
            for edif in comuna.edificios:
                for depa in edif.departamentos:
                    depa.estadistica()

    def cant_total(self):
        cant = 0
        depend = 0
        for comuna in (self.comunas):
            cant += comuna.cant_medidores()
            depend += comuna.dependientes()
        return cant, depend


class Comuna:
    def __init__(self, nombre):
        self.nombre = nombre
        self.casas = []
        self.edificios = []

    def agregar_vivienda(self, vivienda):

        if isinstance(vivienda, Casa):
            self.casas += [vivienda]
        elif isinstance(vivienda, Edificio):
            self.edificios += [vivienda]
        else:
            print("Esta no es una vivienda valida")

    def cant_medidores(self):
        cant = 0
        cant += len(self.casas)
        cant += len(self.edificios)
        for edificio in self.edificios:
            cant += len(edificio.departamentos)
        return cant

    def dependientes(self):
        depend = 0
        for casa in self.casas:
            if casa._depend:
                depend += 1
        for edi in self.edificios:
            for depa in edi.departamentos:
                if depa._depend:
                    depend += 1
        return depend

    def estadistica(self):
        cant = self.cant_medidores()
        depend = self.dependientes()
        print(
            "    Hay {} medidores en la comuna de {}, {} son elecrtrodependientes y el ultimo consumo fue de".format(
                cant, self.nombre, depend))


class Casa:
    def __init__(self, medidor, direccion, cliente):
        self.medidor = medidor
        self.direccion = direccion
        self._depend = False
        self.cliente = cliente

    @property
    def depend(self):
        return depend

    @depend.setter
    def depend(self, value):
        self._depend = value

    def estadistica(self):
        if len(self.medidor._consumos) != 0:
            print(
                "        El ultimo consumo de la casa del cliente {} fue de {}. Electrodependiente: {}".format(
                    self.cliente.rut, self.medidor._consumos[-1],
                    self._depend))

    def agregar_consumo(self, valor):
        self.medidor.consumos = ("Casa", valor)


class Edificio:
    def __init__(self, direccion, nombre, medidor):
        self.direccion = direccion
        self.nombre = nombre
        self.medidor = medidor
        self.departamentos = []

    def agregar_departamento(self, depa):
        if isinstance(depa, Departamento):
            self.departamentos += [depa]
        else:
            print("Este no es un departamento")

    def consumo_total(self):
        total = 0
        depend = 0
        for consumo in self.medidor._consumos:
            total += consumo
        for depa in self.departamentos:
            if depa._depend:
                depend += 1
            for cons in depa.medidor._consumos:
                cons += total
        return total, depend

    def agregar_consumo(self, valor):
        self.medidor.consumos = ("Edificio", valor)

    def estadistica(self):
        total, depend = self.consumo_total()
        if len(self.medidor._consumos) != 0:
            print(
                "El ultimo consumo comun del Edificio {} fue de {} y total de {}. Hay {} electro dependientes".format(
                    self.nombre, self.medidor._consumos[-1], total, depend))
        for depa in self.departamentos:
            depa.estadistica()


class Departamento:
    def __init__(self, medidor, numero, cliente):
        self.medidor = medidor
        self.numero = numero
        self.cliente = cliente
        self._depend = False

    @property
    def depend(self):
        return depend

    @depend.setter
    def depend(self, value):
        if value == 0:
            self._depend = False
        elif value == 1:
            self._depend = True
        else:
            print("No es una opcion valida")

    def estadistica(self):
        if len(self.medidor._consumos) != 0:
            print(
                "        El ultimo consumo del departamento del cliente {} fue de {}. Electrodependiente: {}".format(
                    self.cliente.rut, self.medidor._consumos[-1],
                    self._depend))

    def agregar_consumo(self, valor):
        self.medidor.consumos = ("Departamento", valor)


class Cliente:
    def __init__(self, nombre, rut):
        self.nombre = nombre
        self.rut = rut


class Medidor:
    def __init__(self):
        self._consumos = []

    @property
    def consumos(self):
        return self._consumos

    @consumos.setter
    def consumos(self, value):

        val, vol = value
        print(val, vol, "w")
        if vol < 0:
            print("El minimo valor posible es 0")
        elif val == "Casa":
            if vol > 5000:
                print("El valor se excede")
            else:
                self._consumos += [vol]
        elif val[0] == "Departamento":
            if vol[1] > 4000:
                print("El valor se excede")
            else:
                self._consumos += [vol]
        elif val[0] == "Edificio":
            if vol[1] > 10000:
                print("El valor se excede")
            else:
                self._consumos += [vol]


client = Cliente("Leo", 1234)
medidor1 = Medidor()
medidor2 = Medidor()
medidor3 = Medidor()
medidor4 = Medidor()
ciudad = Ciudad("Santiago")
comuna1 = Comuna("Las Condes")
comuna2 = Comuna("San Joaquin")
casa1 = Casa(medidor1, "cal", client)
casa2 = Casa(medidor2, "cal", client)
edif1 = Edificio("Calle 1", "edif1", medidor1)
edif2 = Edificio("Calle 2", "edif2", medidor2)

depa1 = Departamento(medidor3, 12, client)
depa2 = Departamento(medidor4, 10, client)

ciudad.agregar_comuna(comuna1)
ciudad.agregar_comuna(comuna2)
comuna1.agregar_vivienda(edif1)
comuna1.agregar_vivienda(casa1)
comuna2.agregar_vivienda(edif2)
comuna2.agregar_vivienda(casa2)
edif1.agregar_departamento(depa1)

casa1.depend = 1

casa1.agregar_consumo(3000)

ciudad.estadisticas()
