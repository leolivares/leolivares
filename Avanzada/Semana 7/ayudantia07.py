
def generador_decoradores(n):
    def decorador(funcion):
        def funcion_final(*args,**kwargs):
            for _ in range(n) :
                funcion(*args, **kwargs)
        return funcion_final
    return decorador


@generador_decoradores(5)
def print2(*args,**kwargs):
    print(args,kwargs)


# x = generador_decoradores(5)(print)
dec = generador_decoradores(5)
x = dec(print)

x("hola")

print2("buena")