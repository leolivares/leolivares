class Fundacion :
    def __init__(self,nombre,web,direcc) :
        self.nombre = nombre
        self.web = web
        self.direcc = direcc
        self.cuadrillas = []

    def crear_cuadrilla(self,i,f,l) :
        if f - i == 7 :
            self.cuadrillas += [Cuadrilla(i,f,l)]
        else :
            print("Minimo 7 dias de voluntariado")


class Cuadrilla :

    num_id = 0

    def __init__(self,inicio,fin,lugar):
        self.id = Cuadrilla.num_id
        self.lugar = lugar
        self.inicio = inicio
        self.fin = fin
        self.voluntarios = []
        Cuadrilla.num_id += 1



    def agregar_voluntarios(self,voluntario):

        if len(self.voluntarios) == 4 :
            print("No se admiten mas voluntarios")

        elif len(voluntario.fechas) == 0 :
            self.voluntarios += [voluntario]
            voluntario.fechas += [[self.inicio,self.fin]]
            print("buena")

        else :
            valido = True
            for fecha in voluntario.fechas :
                if fecha[0] == self.inicio or fecha[0] == self.fin or fecha[1] == self.inicio or fecha[1] == self.fin :
                    print("Las fechas no cuadran")
                    valido = False
                elif (fecha[0] > self.inicio and fecha[0] < self.fin) or (fecha[1] > self.inicio and fecha[1] < self.fin) :
                    print("Las fechas no cuadran")
                    valido = False

            if valido :
                self.voluntarios += [voluntario]
                voluntario.fechas += [[self.inicio, self.fin]]
                print("buenisima")
            else :
                print("No cuadran")


class Voluntario :
    def __init__(self,nombre,tlf,email):
        self.nombre = nombre
        self.tlf = tlf
        self.email = email
        self.fechas = []


vzla = Fundacion("Venezuela","venezuela.com","caracas")
vzla.crear_cuadrilla(1,8,"me")
vzla.crear_cuadrilla(5,12,"ac")
vzla.crear_cuadrilla(9,16,"re")
print(vzla.cuadrillas)

vol1 = Voluntario("Leo",1234,"leo.com")
vol2 = Voluntario("Ori",1234,"ori.com")

for cuadrilla in vzla.cuadrillas :
    cuadrilla.agregar_voluntarios(vol1)
print(vol1.fechas)





