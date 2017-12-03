from form import FormRegister
import exceptions as es

if __name__ == '__main__':
    form = FormRegister()

    with open("test.txt") as test_file:

        for line in test_file:
            name, gender, rut, course, section, comment = line.split(";")
            comment = comment.strip("\n")

            try :
                form.check_rut(rut)

            except es.PuntoExcepcion as err :
                print("Error: El rut no puede tener puntos")
                rut_ult = rut[-1]
                rut_pri = rut[:len(rut)-2]
                rut_pri_n = ""

                for r in rut_pri :
                    if r != "." :
                        rut_pri_n += r

                rut = rut_pri_n + "-" + rut_ult

            except es.EspacioExcepcion as err :
                print("Error: El rut no puede contener espacios")
                rut_ult = rut[-1]
                rut_pri = rut[:len(rut)-2]
                rut_arreglado = rut_pri + "-" + rut_ult


            rut_verified = form.check_rut(rut)


            if rut_verified:

                try :
                    form.add_course(course,section)

                except es.EspacioExcepcion as err :
                    print("Error: El curso no puede tener espacios")
                    course_arreglado = ""
                    for c in course :
                        if c != " " :
                            course_arreglado += c
                    course = course_arreglado


                except es.SeccionInexistente as err :
                    print("Error: La seccion no esixte")
                    section = 0

                except es.SeccionErronea as err:
                    print("Error: Seccion mal escrita")
                    secciones = ["1","2","3","4","5","6"]
                    for s in section :
                        if s in secciones :
                            section = int(s)



                form.add_course(course, section)

                form.register_people_info(name, gender, comment)

        form.save_data("result.txt")