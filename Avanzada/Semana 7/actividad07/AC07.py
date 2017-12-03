import json
import os
import datetime

stopwords = {'en': ['the', 'a', 'we'], 'es': ['los', 'las', 'él']}
stem = {'Porter': lambda x: x[:2], 'Snowball': lambda x: x[:3]}

##########################################################################

#                   ESCRIBE TUS DECORADORES AQUI

##########################################################################

def constructor_dec1(input_type, output_type):

    def verify_types(funcion):

        def funcion_nueva(*args, **kwargs):

            funcion_nueva.__name__ = funcion.__name__

            if not isinstance(args[0],input_type):
                raise TypeError("Debe ser del tipo indicado")

            result = funcion(*args, **kwargs)

            if not isinstance(result,output_type):
                raise TypeError("Debe ser del tipo indicado")

            funcion(*args, **kwargs)

            return result

        return funcion_nueva
    return verify_types


def to_lowercase(funcion):
    def nueva_funcion(primer,*args,**kwargs):
        nueva_funcion.__name__ = funcion.__name__
        if isinstance(primer,str):
            nuevo = primer.lower()
        elif isinstance(primer,list) :
            nuevo = [x.lower() for x in primer]
        else:
            nuevo = primer
        return funcion(nuevo,*args,**kwargs)
    return nueva_funcion

def check_file(funcion):
    def nueva_funcion(*args,**kwargs):

        nueva_funcion.__name__ = funcion.__name__
        archivo = args[0] + ".nlp"

        if not os.path.exists(archivo):
            return None

        else :
            return funcion(*args, **kwargs)

    return nueva_funcion

def timer(funcion):
    def nueva_funcion(*args, **kwargs):
        nueva_funcion.__name__ = funcion.__name__
        t1 = datetime.datetime.now()
        resultado = funcion(*args, **kwargs)

        print("El tiempo de ejecucion fue de {}".format(datetime.datetime.now() - t1))

        return resultado
    return nueva_funcion

def corregir_string(string):
    nueva = ""
    for letra in string:
        if letra.isalnum() or letra == " ":
            nueva += letra
    return nueva

def remove_special_characters(funcion):
    def nueva_funcion(primer,*args, **kwargs):
        nueva_funcion.__name__ = funcion.__name__

        if isinstance(primer,str):
            nueva = corregir_string(primer)

        elif isinstance(primer,list):
            nueva = list()
            for palabra in primer:
                nueva.append(corregir_string(palabra))
        else:
            nueva = primer

        return funcion(nueva, *args, **kwargs)

    return nueva_funcion


def get_stats(funcion):
    def nueva_funcion(*args, **kwargs):
        nueva_funcion.__name__ = funcion.__name__
        if isinstance(args[0],str):
            print("La cantidad inicial de caracteres es {}".format(len(args[0])))

        elif isinstance(args[0],list):
            cant = 0
            for palabra in args[0]:
                cant += len(palabra)

            print("La cantidad inicial de caracteres es {}".format(cant))

        resultado = funcion(*args, **kwargs)

        if isinstance(resultado, str):
            print("La cantidad final de caracteres es {}".format(len(resultado)))

        elif isinstance(resultado, list):
            cant = 0
            for palabra in resultado:
                cant += len(palabra)

            print("La cantidad final de caracteres es {}".format(cant))

        return resultado

    return nueva_funcion


def log(funcion):

    def nueva_funcion(*args, **kwargs):
        nueva_funcion.__name__ = funcion.__name__
        if not os.path.exists("log.txt"):

            with open("log.txt", "w") as file:
                print("Nombre: {} , Argumentos: {} {}, Resultado: {}".format(funcion.__name__, args, kwargs, funcion(*args, **kwargs)),file=file)

        else:

            with open("log.txt", "a") as file:
                print("Nombre: {} , Argumentos: {} {}, Resultado: {}".format(funcion.__name__, args, kwargs, funcion(*args, **kwargs)),file=file)

        return funcion(*args, **kwargs)

    return nueva_funcion



##########################################################################

#                       CODIGO A DECORAR

##########################################################################


@timer
@remove_special_characters
@constructor_dec1(str,list)
@log
def tokenize(text, sep, ngrams=1):
    text_splitted = text.split(sep)
    if ngrams == 1:
        return text_splitted

    text_splitted_ngrams = []
    number_of_tokens = int(len(text_splitted)/ngrams) + 1
    for token in range(number_of_tokens):
        text_splitted_ngrams.append(
        sep.join(text_splitted[token*ngrams:token*ngrams + ngrams]))
    return text_splitted_ngrams



@timer
@get_stats
@to_lowercase
@constructor_dec1(list,list)
@log
def remove_stopwords(text, language='es'):
    return list(filter(lambda token: token not in stopwords[language], text))


@get_stats
@log
def apply_stem(text, type_='Porter'):
    return list(map(stem[type_], text))


@timer
@log
def save(text, filename, **kwargs):
    with open(filename + '.nlp', 'w+') as file:
        content = {'text': text}
        content.update(kwargs)
        json.dump(content, file)


@timer
@check_file
@log
def read(filename):
    with open(filename + '.nlp', 'r') as file:
        content = json.load(file)
    text = content['text']
    del content['text']
    return text, content

    
if __name__ == "__main__":
    try:
        archivo = read("archivo")
    except FileNotFoundError as err:
        print("Esto no es un archivo")

    eng = read("ingles")
    esp = read("español")


    print("Esto son los datos sin procesar como lista")
    list_ = tokenize(esp[0], " ", 1)
    print(list_)
    print(tokenize(eng[0], " ", 2))

    print("--------------------------------------\n")

    print("Probado stem")

    print(apply_stem(list_, type_='Porter'))
    print(apply_stem(list_, type_='Snowball'))

    print("--------------------------------------\n")

    print(" Ahora le quitaremos las palabras extra")

    lists = tokenize(esp[0], ' ', 1)
    lists = remove_stopwords(lists, language='es')


    liste = tokenize(eng[0], ' ', 1)
    liste = remove_stopwords(liste, language='en')

    string = " ".join(liste)+" : "+" ".join(lists)
    save(string, "resultados", iluminador = "Hernan")
