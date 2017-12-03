import app
import usuarios as usu


class Menu :

    def __init__(self):
        self.appl = app.Aplicacion()
        self.appl.leer_base_datos()

    #Muestra todos los menus, dependiendo de el usuario
    def mostrar_menu_principal(self) :
        print("Bienvenido al sistema DCCapital Exchange." "\n"
              "Para entrar, debes estar registrado." "\n"
              "Elije una de las opciones" "\n"
              "  1. Registrarse" "\n"
              "  2. Ingresar al sistema")


    def menu_uderaged(self):
        print("Estas registrado al sistema como un usuario Underaged." "\n"
              "Elige una de las siguientes opciones" "\n"
              "1. Lista de Mercados Disponibles" "\n"
              "2. Lista de Mercados en los que esta registrado" "\n"
              "3. Registrarse a un Mercado" "\n"
              "4. Lista de orders" "\n"
              "5. Lista de orders activas" "\n"
              "6. Desplegar Informacion (Global/Especifica)" "\n"
              "7. Consultar Saldo" "\n"
              "8. Consultas del Sistema" "\n"
              "9. Salir del sistema")


    def menu_traders(self):
        print("Estas registrado al sistema como un usuario Trader." "\n"
              "Elige una de las siguientes opciones" "\n"
              "1. Lista de Mercados Disponibles" "\n"
              "2. Lista de Mercados en los que esta registrado" "\n"
              "3. Registrarse a un Mercado" "\n"
              "4. Lista de orders" "\n"
              "5. Lista de orders activas" "\n"
              "6. Ingresar ask" "\n"
              "7. Ingresar bid" "\n"
              "8. Cancelar Order" "\n"
              "9. Desplegar Informacion (Global/Especifica)" "\n"
              "10. Realizar transferencia" "\n"
              "11. Consultar Saldo" "\n"
              "12. Consultas del Sistema" "\n"    
              "13. Convertirse en usuario Investor" "\n"
              "14. Salir del sistema")


    def menu_investors(self):
        print("Estas registrado al sistema como un usuario Investor." "\n"
              "Elige una de las siguientes opciones" "\n"
              "1. Lista de Mercados Disponibles" "\n"
              "2. Lista de Mercados en los que esta registrado" "\n"
              "3. Registrarse a un Mercado" "\n"
              "4. Lista de orders" "\n"
              "5. Lista de orders activas" "\n"
              "6. Ingresar ask" "\n"
              "7. Ingresar bid" "\n"
              "8. Cancelar Order" "\n"
              "9. Desplegar Informacion (Global/Especifica)" "\n"
              "10. Realizar transferencia" "\n"
              "11. Consultar Saldo" "\n"
              "12. Consultas del Sistema" "\n"
              "13. Salir del Sistema")

    def filtros_orders(self):
        print("Elige el filtro por el cual deseas buscar orders: " "\n"
              "    1. Orders del dia" "\n"
              "    2. Orders en fecha especifica" "\n"
              "    3. Orders en un rango de fechas" "\n"
              "    4. Orders en mercado especifico")

    def mercados_info(self):
        print("   ")
        print("Elige que tipo de informacion deseas obtener: " "\n"
              "    1. Informacion de Mercado Especifico" "\n"
              "    2. Informacion de todos los Mercados")

    def consultas(self):
        print("   ")
        print("Elige que tipo de consulta deseas realizar:" "\n"
              "    1. Consulta de usuarios registrados" "\n"
              "    2. Historial de matches" "\n"
              "    3. Informacion de Moneda")

    #Ejecuta el programa
    def run(self) :
        running = True
        while running :
            self.mostrar_menu_principal()
            eleccion = input("Ingrese su opcion: ")

            iniciar = False

            if eleccion == "1" :
                self.appl.registro()
                iniciar , cliente = self.appl.iniciar_sesion()

            elif eleccion == "2" :
                iniciar , cliente = self.appl.iniciar_sesion()


            while iniciar :

                cliente.informacion_entrada(self.appl)

                if isinstance(cliente,usu.Underaged) :
                    seguir = True
                    while seguir :
                        self.menu_uderaged()
                        opcion = input("Ingresa una opcion: ")

                        if opcion == "1" :
                            self.appl.mercados_disponibles()
                        elif opcion == "2" :
                            self.appl.mercados_registrados(cliente)
                        elif opcion == "3" :
                            mercado = input("Ingresa el ticket del mercado al que deseas ingresar: ")
                            self.appl.registrar_mercado(cliente,mercado)
                            registrado = self.appl.registrar_mercado(cliente, mercado)
                            if not registrado:
                                print("Fuiste registrado en el mercado {} exitosamente".format(mercado))
                                print("   ")
                        elif opcion == "4" :
                            self.filtros_orders()
                            print("  ")
                            filtro = input("Elige el filtro de busqueda: ")

                            if filtro == "1" :
                                self.appl.lista_orders_dia(cliente)
                            elif filtro == "2" :
                                self.appl.lista_orders_fecha(cliente)
                            elif filtro == "3" :
                                self.appl.lista_orders_entre(cliente)
                            elif filtro == "4" :
                                ticket = input("Ingresa el ticker del mercado: ")
                                self.appl.lista_orders_mercado(ticket,cliente)
                        elif opcion == "5" :
                            self.appl.lista_orders_activas(cliente)
                        elif opcion == "6" :
                            self.mercados_info()
                            eleccion = input("Elige una opcion: ")
                            if eleccion == "1":
                                print("    ")
                                mer_ticker = input("Ingresa el ticker del Mercado: ")
                                self.appl.desplegar_informacion(mer_ticker)
                            elif eleccion == "2":
                                self.appl.desplegar_informacion()

                        elif opcion == "7" :
                            self.appl.consultar_saldo(cliente)

                        elif opcion == "8" :
                            self.consultas()
                            seleccion = input("Ingresa la opcion que deseas: ")
                            if seleccion == "1" :
                                self.appl.consulta_usuarios()
                            elif seleccion == "2" :
                                self.appl.historial_matches()
                            elif seleccion == "3" :
                                moneda = input("Ingresa la moneda que deseas consultar: ")
                                self.appl.info_moneda(moneda)

                        elif opcion == "9" :
                            print("   ")
                            print("Hasta luego!" "\n"
                                  "El usuario {} se ha desconectado".format(cliente.usuario))
                            print("   ")
                            seguir = False
                            iniciar = False
                            self.appl.actualizar_datos()


                elif isinstance(cliente,usu.Trader) :
                    seguir = True
                    while seguir :
                        self.menu_traders()
                        opcion = input("Ingresa una opcion: ")

                        if opcion == "1" :
                            self.appl.mercados_disponibles()
                        elif opcion == "2":
                            self.appl.mercados_registrados(cliente)
                        elif opcion == "3" :
                            mercado = input("Ingresa el ticket del mercado al que deseas ingresar: ")
                            registrado = self.appl.registrar_mercado(cliente, mercado)
                            if not registrado :
                                print("Fuiste registrado en el mercado {} exitosamente".format(mercado))
                                print("   ")
                        elif opcion == "4" :
                            self.filtros_orders()
                            print("  ")
                            filtro = input("Elige el filtro de busqueda: ")

                            if filtro == "1" :
                                self.appl.lista_orders_dia(cliente)
                            elif filtro == "2" :
                                self.appl.lista_orders_fecha(cliente)
                            elif filtro == "3" :
                                self.appl.lista_orders_entre(cliente)
                            elif filtro == "4" :
                                ticket = input("Ingresa el ticker del mercado: ")
                                self.appl.lista_orders_mercado(ticket,cliente)

                        elif opcion == "5" :
                            self.appl.lista_orders_activas(cliente)

                        elif opcion == "6" :
                            cant = self.appl.revisar_activas(cliente)
                            if cant == 5 :
                                print("   ")
                                print("Lo sentimos.")
                                print("Por ser un usuario Trader solo puedes tener 5 orders activas a la vez")
                                print("Si quieres tener orders activas ilimitadas, realiza el upgrade a Investor por 300.000 DCC")
                                print("   ")
                            else :
                                order = self.appl.ingresar_ask(cliente)

                                if order :
                                    self.appl.buscar_matches(order,True)

                        elif opcion == "7" :
                            order = self.appl.ingresar_bid(cliente)
                            if order :
                                self.appl.buscar_matches(order,True)

                        elif opcion == "8" :
                            order_id = input("Ingresa el id del order que deseas cancelar:")
                            self.appl.cancelar_order(cliente,order_id)

                        elif opcion == "9" :
                            self.mercados_info()
                            eleccion = input("Elige una opcion: ")
                            if eleccion == "1" :
                                print("    ")
                                mer_ticker = input("Ingresa el ticker del Mercado: ")
                                self.appl.desplegar_informacion(mer_ticker)
                            elif eleccion == "2" :
                                self.appl.desplegar_informacion()

                        elif opcion == "10" :
                            self.appl.banco(cliente)

                        elif opcion == "11" :
                            self.appl.consultar_saldo(cliente)

                        elif opcion == "12" :
                            self.consultas()
                            seleccion = input("Ingresa la opcion que deseas: ")
                            if seleccion == "1":
                                self.appl.consulta_usuarios()
                            elif seleccion == "2" :
                                self.appl.historial_matches()
                            elif seleccion == "3" :
                                moneda = input("Ingresa la moneda que deseas consultar: ")
                                self.appl.info_moneda(moneda)

                        elif opcion == "13" :
                            print("Para realizar el upgrade debes entregar 300000 DCC" "\n"
                                  "Seguro que deseas continuar?" "\n"
                                  "   1. Si" "\n"
                                  "   2. No")
                            eleccion = input("Elige una opcion: ")
                            if eleccion == "1" :
                                nuevo = self.appl.upgrade(cliente)
                                if nuevo :
                                    cliente = nuevo
                            else :
                                print("   ")
                                print("Considera convertirte en Investor mas adelante!")
                                print("   ")


                        elif opcion == "14" :
                            print("   ")
                            print("Hasta luego!" "\n"
                                  "El usuario {} se ha desconectado".format(cliente.usuario))
                            print("   ")
                            seguir = False
                            iniciar = False
                            self.appl.actualizar_datos()


                elif isinstance(cliente,usu.Investor) :
                    seguir = True
                    while seguir :
                        self.menu_investors()
                        opcion = input("Ingresa una opcion: ")

                        if opcion == "1":
                            self.appl.mercados_disponibles()
                        elif opcion == "2":
                            self.appl.mercados_registrados(cliente)
                        elif opcion == "3":
                            mercado = input("Ingresa el ticket del mercado al que deseas ingresar: ")
                            registrado = self.appl.registrar_mercado(cliente, mercado)
                            if not registrado:
                                print("Fuiste registrado en el mercado {} exitosamente".format(mercado))
                                print("   ")
                        elif opcion == "4":
                            self.filtros_orders()
                            print("  ")
                            filtro = input("Elige el filtro de busqueda: ")

                            if filtro == "1":
                                self.appl.lista_orders_dia(cliente)
                            elif filtro == "2":
                                self.appl.lista_orders_fecha(cliente)
                            elif filtro == "3":
                                self.appl.lista_orders_entre(cliente)
                            elif filtro == "4":
                                ticket = input("Ingresa el ticker del mercado: ")
                                self.appl.lista_orders_mercado(ticket, cliente)

                        elif opcion == "5":
                            self.appl.lista_orders_activas(cliente)

                        elif opcion == "6":
                            order = self.appl.ingresar_ask(cliente)
                            if order :
                                self.appl.buscar_matches(order,True)

                        elif opcion == "7":
                            order = self.appl.ingresar_bid(cliente)
                            if order :
                                self.appl.buscar_matches(order,True)

                        elif opcion == "8" :
                            order_id = input("Ingresa el id del order que deseas cancelar:")
                            self.appl.cancelar_order(cliente, order_id)

                        elif opcion == "9":
                            self.mercados_info()
                            eleccion = input("Elige una opcion: ")
                            if eleccion == "1":
                                print("    ")
                                mer_ticker = input("Ingresa el ticker del Mercado: ")
                                self.appl.desplegar_informacion(mer_ticker)
                            elif eleccion == "2":
                                self.appl.desplegar_informacion()

                        elif opcion == "10" :
                            self.appl.banco(cliente)

                        elif opcion == "11" :
                            self.appl.consultar_saldo(cliente)

                        elif opcion == "12" :
                            self.consultas()
                            seleccion = input("Ingresa la opcion que deseas: ")
                            if seleccion == "1":
                                self.appl.consulta_usuarios()
                            elif seleccion == "2" :
                                self.appl.historial_matches()
                            elif seleccion == "3" :
                                moneda = input("Ingresa la moneda que deseas consultar: ")
                                self.appl.info_moneda(moneda)

                        elif opcion == "13":
                            print("   ")
                            print("Hasta luego!" "\n"
                                  "El usuario {} se ha desconectado".format(cliente.usuario))
                            print("   ")
                            seguir = False
                            iniciar = False
                            self.appl.actualizar_datos()



if __name__ == '__main__':
    menu = Menu()
    menu.run()


