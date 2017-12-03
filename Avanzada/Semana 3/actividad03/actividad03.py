from collections import deque
import random


class PrograBanner:

    def __init__(self):
        self.registro_de_alumnos = list()
        self.registro_de_cursos = list()
        self.unidades = dict()
        self.cola = deque()

    def cursos_comunes(self,alumno1,alumno2):
        comparten = False

        for curso in alumno1.cursos_inscritos :

            for curs in alumno2.cursos_inscritos :
                if curso.sigla == curs.sigla :
                    comparten = True
                    print("Ambos alumnos estan juntos en: ")
                    print("   ", curso.sigla)

        if not comparten :
            print("No comparten cursos")



    def importar_datos(self,nombre):

        archivo = open(nombre,"r")
        for linea in archivo :
            linea = linea[:-1]
            lista = linea.split(",")

            if nombre == "alumnos.txt" :
                alum = Alumno(lista[0],lista[1])
                self.registro_de_alumnos.append(alum)

            elif nombre == "cursos.txt" :
                curso = Curso(lista[0],lista[3],lista[1],lista[2])
                self.registro_de_cursos.append(curso)

            elif nombre == "unidades.txt" :
                self.unidades[lista[0]] = lista[1]

        archivo.close()

    def crear_cupos(self):
        i = 1
        for curso in self.registro_de_cursos :
            cant = int(curso.n_cupos_disp)
            while cant > 0 :
                curso.cupos.append(Cupos(curso.horario,i))
                cant -= 1
                i += 1


    def cola_alumnos_aleatoria(self):
        cant = len(self.registro_de_alumnos)
        for i in range(cant+1) :
            indice = random.randint(0,cant-1)
            self.cola.append(self.registro_de_alumnos[indice])

    def alumnos_en_curso(self, nombre) :
        for curso in self.registro_de_cursos :
            if curso.sigla == nombre:
                curso.alumnos_en_curso()


    def primera_toma(self):
        for alumno in self.registro_de_alumnos :
            cursos = random.sample(self.registro_de_cursos,3)

            for curso in cursos :
                if len(alumno.cursos_inscritos) == 0 :
                    if int(curso.n_cupos_disp) > 0 :
                        alumno.agregar_curso(curso)
                        curso.agregar_alumno(alumno)

                elif len(alumno.cursos_inscritos) > 0 :
                    if self.unidades[alumno.carrera] == 0 :
                        if int(curso.n_cupos_disp) > 0:
                            alumno.agregar_curso(curso)
                            curso.agregar_alumno(alumno)

                    else :
                        if int(curso.n_cupos_disp) > 0:
                            se_puede = True
                            for cur in alumno.cursos_inscritos :
                                if cur.horario == curso.horario :
                                    se_puede = False

                            if se_puede :
                                alumno.agregar_curso(curso)
                                curso.agregar_alumno(alumno)

    def reajuste(self):
        pass


class Curso:

    def __init__(self,sigla,horario,n_cupos_disp,n_sobrecupos):
        self.sigla = sigla
        self.horario = horario
        self.n_cupos_disp = n_cupos_disp
        self.n_sobrecupos = n_sobrecupos
        self.alumnos_inscritos = deque()
        self.cupos = list()

    def abrir_sobrecupos(self):
        pass

    def agregar_alumno(self,alumno):
        self.alumnos_inscritos.append(alumno)

    def alumno_en_curso(self,alumno):
        if alumno in self.alumnos_inscritos :
            print("Alumno del curso {}. Numero de Alumnno: {}".format(self.sigla,alumno.num_alumno))


    def alumnos_en_curso(self):

        for alumno in self.alumnos_inscritos :
            print("Alumno registrado", alumno.num_alumno)
            for curso in alumno.cursos_inscritos :
                if curso.sigla == self.sigla :
                    for cupo in alumno.registro_cupos :
                        for cup in self.cupos :
                            if cupo.id == cup.id :
                                print("Cupo:",cupo.id, "\n")






class Alumno:

    def __init__(self,num_alumno,carrera):
        self.num_alumno = num_alumno
        self.carrera = carrera
        self.registro_cupos = list()
        self.cursos_inscritos = deque()


    def agregar_curso(self,curso):
        self.cursos_inscritos.append(curso)



class Cupos:

    def __init__(self,horario, id):
        self.horario = horario
        self.id = id


    def __repr__(self):
        return "{} {}".format(self.id,self.horario)


if __name__ == "__main__" :
    banner = PrograBanner()
    banner.importar_datos("alumnos.txt")
    banner.importar_datos("cursos.txt")
    banner.importar_datos("unidades.txt")


    banner.cola_alumnos_aleatoria()
    banner.crear_cupos()
    banner.primera_toma()

    banner.alumnos_en_curso("IIC9748")
