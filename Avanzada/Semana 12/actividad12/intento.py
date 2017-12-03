from pi import pi

tamanos = {1: 12000, 2: 11235, 3: 6000, 4: 15000, 5: 12345, 6: 9999,
           7: 22233, 8: 13131, 9: 24000}

algoritmos = {"par": 1, "impar": 2}

bytes_global = []

def lectura_archivos():
    bytes_corrupted1 = bytearray()
    bytes_corrupted2 = bytearray()

    with open("potato.potato", "rb") as archivo:
        texto1 = archivo.read()
        bytes_corrupted1.extend(texto1)

    with open("herp.derp", "rb") as archivo:
        texto2 = archivo.read()
        bytes_corrupted2.extend(texto2)

    return bytes_corrupted1,bytes_corrupted2


def obtener_bytes_arreglados(corrupted1, corrupted2):
    bytes_arreglados = bytearray()
    continuar1 = 0
    continuar2 = 0
    k = 0
    for i in pi:
        if i == "0":
            cambiar_algoritmos()

        else:
            tamano = tamanos[int(i)]

            if k % 2 == 0:
                chunk = corrupted1[continuar1:tamano]
                continuar1 += tamano
            else:
                chunk = corrupted2[continuar2:tamano]
                continuar2 += tamano

            if int(i) % 2 == 0:
                algoritmo = algoritmos["par"]
            else:
                algoritmo = algoritmos["impar"]

            if algoritmo == 1:
                bytes_a = algoritmo1(chunk)
            else:
                bytes_a = algoritmo2(chunk)

            bytes_arreglados.extend(bytes_a)

        k += 1

    return bytes_arreglados

def algoritmo1(chunck):
    bytes_a = bytearray()

    for i in range(0, len(chunck), 3):
        a = chunck[i:i+3]
        ints = list(map(int, a))
        numero = 255 - (ints[0]*ints[1]*ints[2])
        bytes_a.extend(bytes(int((numero))))

    return bytes_a

def algoritmo2(chunck):
    bytes_a = bytearray()
    for i in range(0, len(chunck), 3):
        a = chunck[i:i+3]
        significativas = list()
        for c in a:
            a_str = str(c).zfill(3)[::-1]
            if a_str <= "255":
                significativas.append(str(int(a_str))[0])
            else:
                significativas.append(str(c)[0])


        o = "".join(significativas)
        o = bytes(int(o))
        bytes_a.extend(o)

    return bytes_a


def cambiar_algoritmos():
    alg1 = algoritmos["par"]
    alg2 = algoritmos["impar"]

    algoritmos["par"] = alg2
    algoritmos["impar"] = alg1


def crear_mp4(fixed):
    print(fixed)
    with open("alin.mp4", "wb") as archivo:
        archivo.write(fixed)


if __name__ == '__main__':
    a, b = lectura_archivos()
    fixed = obtener_bytes_arreglados(a, b)
    crear_mp4(fixed)