class Nodo:

    def __init__(self,num=None):
        self.num = num
        self.nombre = None
        self.hijos = dict()

    def add_contact(self,nombre,numero,completo):
        letra = nombre[0]
        if len(nombre) == 1:
            if letra in self.hijos:
                print("Este contacto ya existe")
            else:
                nuevo = Nodo()
                self.hijos.update({letra: nuevo})
                nuevo.num = numero
                nuevo.nombre = completo

        else:
            if letra in self.hijos:
                self.hijos[letra].add_contact(nombre[1:], numero,completo)

            else:
                nuevo = Nodo()
                self.hijos.update({letra: nuevo})
                nuevo.add_contact(nombre[1:], numero,completo)

    def buscar_contacto(self, contacto):
        letra = contacto[0]
        if len(contacto) == 1:
            if letra in self.hijos:
                return self.hijos[letra]
            else :
                return None

        else:
            if letra in self.hijos:
                contact = self.hijos[letra].buscar_contacto(contacto[1:])
                return contact

            else:
                return None


class ContactTrie:

    def __init__(self):
        self.hijos = dict()

    def add_contact(self,contacto,numero):
        nombre = contacto.upper()
        if not nombre.isalpha() :
            print("Tienes que ingresar un nombre de contacto solo con letras")

        elif not isinstance(numero,int) :
            print("El numero debe ser un entero")

        elif int(numero) <= 0:
            print("El numero no puede ser negativo")

        else :

            letra = nombre[0]
            if len(nombre) == 1 :
                if letra in self.hijos :
                    print("Este contacto ya existe")
                else :
                    nuevo = Nodo()
                    self.hijos.update({letra : nuevo})
                    nuevo.num = numero
                    nuevo.nombre = nombre

            else :
                if letra in self.hijos :
                    self.hijos[letra].add_contact(nombre[1:],numero,nombre)

                else :
                    nuevo = Nodo()
                    self.hijos.update({letra : nuevo})
                    nuevo.add_contact(nombre[1:],numero,contacto.upper())


    def buscar_contacto(self,contacto):
        nombre = contacto.upper()
        letra = nombre[0]
        if len(nombre) == 1 :
            if letra in self.hijos :
                return self.hijos[letra]
            else :
                return None

        else :
            if letra in self.hijos :
                contact = self.hijos[letra].buscar_contacto(nombre[1:])
                return contact

            else :
                return None


    def change_contact_number(self,contacto,numero):
        contact = self.buscar_contacto(contacto)

        if contact :
            contact.num = int(numero)
            print("Cambio Realizado con Exito!")
        else :
            print("Este contacto no existe")


    def ask_for_contact(self,contacto):
        contact = self.buscar_contacto(contacto)
        if contact :
            print("Nombre: {} , Numero: {}".format(contact.nombre,contact.num))

        else :
            print("Ese contacto no existe")

    def get_all_contacts(self):

        if len(self.hijos) == 0 :
            print("No hay contacto registrados")

        else :

            por_visitar = []
            for k in self.hijos.values() :
                por_visitar.append(k)

            contactos = []
            for nodo in por_visitar :
                if nodo.nombre :
                    contactos += [[nodo.nombre,nodo.num]]
                for m in nodo.hijos.values() :
                    por_visitar.append(m)

            return contactos

    def merge_tries(self,other_trie):

        if not isinstance(other_trie,ContactTrie) :
            print("Las instancias deben ser de la clase ContactTrie")


        else :
            contactos_other = other_trie.get_all_contacts()

            for contact in contactos_other :
                existe = self.buscar_contacto(contact[0])
                if not existe :
                    self.add_contact(contact[0],contact[1])
            print("Union Exitosa!")

    def __repr__(self):
        contactos = self.get_all_contacts()
        str = ""
        for contact in contactos :
            str += "Nombre: {}, Numero: {} \n".format(contact[0],contact[1])
        return str


    def __add__(self, other):
        nuevo = ContactTrie()

        if not isinstance(other,ContactTrie) :
            print("Las instancias sumadas deben ser de la clase ContactTrie")
            return None

        contactos = self.get_all_contacts()
        for contact in contactos :
            nuevo.add_contact(contact[0],contact[1])

        nuevo.merge_tries(other)
        return nuevo


if __name__ == "__main__" :

    #Poblamos el Sistema
    contact_trie = ContactTrie()
    contact_trie.add_contact("leo",1111)
    contact_trie.add_contact("leonardo",2222)
    contact_trie.add_contact("alguien",33333)

    contact_trie2 = ContactTrie()
    contact_trie2.add_contact("Mavrakis",4444)
    contact_trie2.add_contact("AvaNzada",2233)
    contact_trie2.add_contact("Ivania", 5555)
    contact_trie2.add_contact("leonardo",2222)

    #Se prueban los prints de la clase y se demuestra que se anadieron los contactos
    print("----------------------")
    print(contact_trie)
    print("----------------------")
    print(contact_trie2)
    print("----------------------")

    print("   ")

    #Se pide la informacion de contactos, existente o no
    print("**********************")
    contact_trie.ask_for_contact("leonardo")
    contact_trie2.ask_for_contact("ivania")
    contact_trie2.ask_for_contact("NoExistente")
    print("**********************")

    print("   ")

    #Se demuestra que ocurre el cambio de numero para el contacto
    print("/////////////////////////")
    contact_trie2.ask_for_contact("Ivania")
    contact_trie2.change_contact_number("Ivania","012345678")
    contact_trie2.ask_for_contact("Ivania")
    print("/////////////////////////")

    print("   ")

    #La funcion retorna la lista pedida y se hace print de esta
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(contact_trie.get_all_contacts())
    print(contact_trie2.get_all_contacts())
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    print("   ")

    #Se realiza el merge de ambas instancias, y el contacttrie recibe los contactos que no posee
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print(contact_trie)
    contact_trie.merge_tries(contact_trie2)
    print(contact_trie)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    print("   ")

    #Por ultimo, se verifica que la suma entrega una nueva instancia con la union de las dos anteriores
    print(".............................")
    nueva = contact_trie + contact_trie2
    print(nueva)
    print(".............................")
