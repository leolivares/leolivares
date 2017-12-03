from pi import pi

tamanos = {1: 12000, 2: 11235, 3: 6000, 4: 15000, 5: 12345, 6: 9999,
           7: 22233, 8: 13131, 9: 24000}

algoritmos = {"par": 1, "impar": 2}

bytes_arreglados = bytearray()


def lectura_archivos():
    bytes_corrupted1 = bytearray()
    bytes_corrupted2 = bytearray()

    with open("potato.potato", "rb") as archivo:
        texto1 = archivo.read()

    with open("herp.derp", "rb") as archivo:
        texto2 = archivo.read()

    return texto1, texto2


def buscar_chunks(texto1, texto2):

    for i in range(1):

        print(int(pi[i]))
        if int(pi[i]) == 0:
            cambiar_algoritmos()

        else:
            print("entr")
            tamano = tamanos[int(pi[i])]
            print(tamano)
            archivo1 = texto1
            archivo2 = texto2

            if i % 2 == 0:
                print("ene")
                chunk = archivo1[:tamano]
                texto1 = archivo1[tamano:]
            else:
                chunk = archivo2[:tamano]
                texto2 = archivo2[tamano:]


            if int(pi[i]) % 2 == 0:
                algoritmo = algoritmos["par"]
            else:
                print("im")
                algoritmo = algoritmos["impar"]

            if algoritmo == 1:
                print("n")
                algoritmo_uno(chunk)
            elif algoritmo == 2:
                algoritmo_dos(chunk)



def algoritmo_uno(chunk):

    for i in range(0, len(chunk), 3):
        corrupted_ints = list(map(int, chunk[i:i + 3]))
        #print(corrupted_ints)




def algoritmo_dos(chunk):
    bytes = list()
    for i in range(0, len(chunk), 3):
        a = chunk[i:i+3]
        numeros = list()
        for d in a:
            numeros.append(str(d).zfill(3))

        print(numeros)

        for i in range(len(numeros)):

            if int(numeros[i][::-1]) <= 255:
                numeros[i] = int(numeros[i][::-1])
            else:
                numeros[i] = int(numeros[i])

        print(numeros)

        for i in numeros:
            bytes.append(str(i)[0])

    byte_final = "".join(bytes)
    print(byte_final)


def cambiar_algoritmos():

    alg1 = algoritmos["par"]
    alg2 = algoritmos["impar"]

    algoritmos["par"] = alg2
    algoritmos["impar"] = alg1


if __name__ == '__main__':
    texto1, texto2 = lectura_archivos()
    buscar_chunks(texto1, texto2)

