class MetaPokemon(type):
    def __new__(meta, name, bases, clsdict):
        print("Meta: {}".format(meta))
        print("Name: {}".format(name))
        print("Bases: {}".format(bases))
        print("Dict: {}".format(clsdict))
        return super().__new__(meta, name, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        print(args)
        return super().__call__(*args, **kwargs)


class A:
    pass


class Pokemon(A, metaclass=MetaPokemon):
    tipo = "electrico"

    def __init__(self, entrenador, nombre):
        self.entrenador = entrenador
        self.nombre = nombre


class MetaOrganizacion(type):

    instances = dict()

    def __new__(meta, name, bases, clsdict):
        def see_members(self):
            for i, members in enumerate(self.members):
                print("Miembro {}: {}".format(i, members))

        def change_boss(self, new_boss):
            self.boss = new_boss

        def new_call(self, *args, **kwargs):
            print("Nombre de Jefe: {} ; Cantidad de Empleados {}"
                  .format(self.boss, len(self.empleados)))

        clsdict.update({"__call__": new_call})
        clsdict.update({"see_members": see_members})
        clsdict.update({"replace_boss": change_boss})
        return super().__new__(meta, name, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == "Organization":
            if args[0] in instances:
                return None
            instance = super.__call_(self, *args, **kwargs)
            MetaOrganizacion.instances.update({args[0], instance})
            return instance


class Organizacion(metaclass=MetaOrganizacion):
    def __init__(self):
        pass


class MetaPersona(type):

    def __new__(meta, name, bases, clsdict):
        if "Boss" in name:
            pass

    def __call__(cls, *args, **kwargs):
        orga = args[0]
        instance = super().__call__(orga.name, *args[1:], **kwargs)
        setattr(instance, "name", random.choice(name_list))
        setattr(instance, "last_name", random.choice(last_name_list))
        setattr(instance, "age", random.choice(age_list))
        return instance

