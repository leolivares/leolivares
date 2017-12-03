class Persona :

    def __init__(self,nombre,apellido,correo,imei):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.imei = imei
        self.reportes = []

    def tiempo_promedio(self):
        cant = 0
        time = 0
        for reporte in self.reportes :
            cant += 1
            time += reporte.tiempo
        return time / cant

    def error_promedio(self):
        cant = 0
        metros = 0
        for reporte in self.reportes :
            cant += 1
            metros += reporte.error
        return metros / cant

    def actividad_frecuente(self):
        veh = 0
        cam = 0
        bici = 0
        quie = 0
        for reporte in self.reportes :
            if (reporte.actividad).tipo == "ir en vehiculo" :
                veh += 1
            elif reporte.actividad.tipo == "caminar" :
                cam += 1
            elif reporte.actividad.tipo == "ir en bici" :
                bici += 1
            else :
                quie += 1
        pass

    def agregar_reporte(self,reporte):
        self.reportes += [reporte]



class Reporte :

    def __init__(self,lat,long,error,tiempo,actividad):
        self.lat = lat
        self.long = long
        self.error = error
        self.tiempo = tiempo
        self.actividad = actividad



class Actividad :

    def __init__(self,tipo,prob):
        self.tipo = tipo
        self.prob = prob

class Pais :

    def __init__(self,nombre):
        self.nombre = nombre
        self.personas = []

    def agregar_personas(self,persona):
        self.personas += [persona]


class Continente :

    def __init__(self,nombre):
        self.nombre = nombre
        self.paises = []

    def agregar_pais(self,pais):
        self.paises += [pais]


class Mundo :

    def __init__(self):
        self.continentes = []

    def agregar_continentes(self,continente):
        self.continentes += [continente]


mundo = Mundo()
africa = Continente("Africa")
europa = Continente("Europa")
nigeria = Pais("Nigeria")
zimbabwe = Pais("Zimbabwe")
italia = Pais("Italia")
francia = Pais("Francia")
leo = Persona("Leo","Olivares","leo.com",223)
ori = Persona("Ori","Olivares","ori.com",344)
act1 = Actividad("estar quieto",0.8)
act2 = Actividad("ir en bici",0.8)
act3 = Actividad("estar quieto",0.8)
rep1 = Reporte(1,2,3,4,act1)
rep2 = Reporte(2,3,4,5,act2)
rep3 = Reporte(6,7,8,9,act3)

leo.agregar_reporte(rep1)
leo.agregar_reporte(rep2)
leo.agregar_reporte(rep3)
mundo.agregar_continentes(africa)
mundo.agregar_continentes(europa)
africa.agregar_pais(nigeria)
africa.agregar_pais(zimbabwe)
europa.agregar_pais(italia)
europa.agregar_pais(francia)


print(leo.reportes)
print(leo.tiempo_promedio())
