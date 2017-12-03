import os
from random import choice, sample
import zlib
import numpy
import time

with open("image/Anime.png", "rb") as file:
    img_bytes = file.read()


def extract_bytes(img_bytes):
    i = 0
    while i < len(img_bytes):
        if i == 0:
            firm = img_bytes[:8]
            needed_bytes = firm
            i += 8
        else:
            length_bytes = img_bytes[i:i+4]
            i += 4
            length = int.from_bytes(length_bytes, byteorder="big")
            type_bytes = img_bytes[i:i+4]
            i += 4
            type = type_bytes.decode()

            if type in ["IHDR", "IDAT", "IEND"]:
                needed_bytes += length_bytes
                needed_bytes += type_bytes

                info_bytes = img_bytes[i:i+length]
                needed_bytes += info_bytes
                crc_bytes = img_bytes[i+length:i+length+4]
                needed_bytes += crc_bytes

            i += length + 4

    return needed_bytes

def classify_bytes(bytes):

    cla = {}
    idat_bytes = b''

    firm = bytes[:8]
    cla["firm"] = firm

    i = 8
    while i < len(bytes):
        length_bytes = bytes[i:i+4]
        length = int.from_bytes(length_bytes, byteorder="big")

        i += 4

        type_bytes = bytes[i:i+4]
        type = type_bytes.decode()

        i += 4

        data = bytes[i:i+length]

        i += length

        crc = bytes[i:i+4]

        i += 4

        if type == "IHDR" or type == "IEND":
            cla[type] = length_bytes + type_bytes + data + crc
        else:
            idat_bytes += data

    new_length = len(idat_bytes).to_bytes(4, byteorder="big")
    type = "IDAT".encode()
    new_crc = zlib.crc32(type+idat_bytes).to_bytes(4, byteorder="big")

    #k = zlib.decompress(idat_bytes)
    #print(k[:5])
    #print(list(k[:5]))

    cla["IDAT"] = new_length + type + idat_bytes + new_crc

    # with open("prueba.png", "wb") as file:
    #     b = cla["firm"]
    #     for c in cla:
    #         if c != "firm":
    #             b += cla[c]
    #
    #     file.write(b)

    return cla


def blurr(btes):
    k = time.time()
    colors = ["r", "b", "g"]
    dicc = classify_bytes(btes)


    ihdr_chunk = dicc["IHDR"]
    length = int.from_bytes(ihdr_chunk[:4], byteorder="big")
    type_b = ihdr_chunk[4:8]
    width = int.from_bytes(ihdr_chunk[8:12], byteorder="big")
    height = int.from_bytes(ihdr_chunk[12:16], byteorder="big")

    print(width, height)

    idat_chunk = dicc["IDAT"]

    length_b = idat_chunk[:4]
    length = int.from_bytes(length_b, byteorder="big")

    type = idat_chunk[4:8]


    a = idat_chunk[8:8+length]

    idat_dat = zlib.decompress(a)

    print(len(idat_dat))

    if height * ((width*3)+1) % len(idat_dat) == 0:
        bytes_por_pixeles = 3
    else:
        bytes_por_pixeles = 4


    matrices = []
    i = 0

    for color in colors:
        matrix = [idat_dat[n - ((width * bytes_por_pixeles) + 1):n] for n in
                  range((width * bytes_por_pixeles) + 1,
                        len(idat_dat) + ((width * bytes_por_pixeles) + 1),
                        (width * bytes_por_pixeles) + 1)]

        matrix = [filtrar(fila, i, bytes_por_pixeles) for fila in matrix]

        nueva_matriz = new_matrix(matrix)

        matrices.append(nueva_matriz)

        i += 1


    final = b''
    for _ in range(len(matrices[0])):

        row = [0]
        for i in range(len(matrices[0][0])):

            row.append(matrices[0][_][i])
            row.append(matrices[1][_][i])
            row.append(matrices[2][_][i])
        final += bytes(row)

    final = zlib.compress(final)


    new_len = len(final).to_bytes(4, byteorder="big")
    type = "IDAT".encode()
    new_crc = zlib.crc32(type+final).to_bytes(4, byteorder="big")

    with open("blurr.png", "wb") as file:
        f = dicc["firm"] + dicc["IHDR"] + new_len + type + final + new_crc + dicc["IEND"]
        file.write(f)

    b = time.time()
    print(b - k)


def filtrar(fila, i, per):
    fila = fila[1:]
    fila_nueva = [fila[n] for n in range(i, len(fila), per)]
    return bytes(fila_nueva)


def new_matrix(matrix):
    new_matr = []

    i = 0
    for fila in matrix:
        j = 0
        new_row = []
        for byte in fila:
            new_row.append(ponderar(byte, i, j, matrix))
            j += 1
        new_matr.append(new_row)
        i += 1

    return new_matr


def ponderar(byte, i, j, original):
    up = 0
    down = 0
    left = 0
    right = 0
    up_right = 0
    up_left = 0
    lo_right = 0
    lo_left = 0

    center = original[i][j]*4


    if i - 1 > 0:
        up = original[i-1][j] * 2
    if i + 1 < len(original):
        down = original[i+1][j] * 2
    if j - 1 > 0:
        left = original[i][j-1] * 2
    if j + 1 < len(original[0]):
        right = original[i][j+1] * 2

    if i - 1 > 0 and j + 1 < len(original[0]):
        up_right = original[i-1][j+1]
    if i - 1 > 0 and j - 1 > 0:
        up_left = original[i-1][j-1]
    if i + 1 < len(original) and j + 1 < len(original[0]):
        lo_right = original[i+1][j+1]
    if i + 1 < len(original) and j - 1 > 0:
        lo_left = original[i+1][j-1]

    number = up + down + left + right + up_left + up_right + lo_left + lo_right + center
    number = number/16
    number = numpy.round(number, 0)

    return int(number)

def width_height(ihdr_chunk):
    length = int.from_bytes(ihdr_chunk[:4], byteorder="big")
    type_b = ihdr_chunk[4:8]
    width = int.from_bytes(ihdr_chunk[8:12], byteorder="big")
    height = int.from_bytes(ihdr_chunk[12:16], byteorder="big")

    return width, height


#AQUI EMPIEZA CUT

def cut(posiciones, img_bytes):

    maxi_x = max((posiciones[0][1], posiciones[1][1]))
    mini_x = min((posiciones[0][1], posiciones[1][1]))

    maxi_y = max((posiciones[0][0], posiciones[1][0]))
    mini_y = min((posiciones[0][0], posiciones[1][0]))

    print(mini_x, maxi_x)
    print(mini_y, maxi_y)

    dicc = classify_bytes(img_bytes)

    width, height = width_height(dicc["IHDR"])
    print(width, height)

    idat_bytes = dicc["IDAT"]

    length = int.from_bytes(idat_bytes[:4], byteorder="big")
    type_bytes = idat_bytes[4:8]
    idat_info = idat_bytes[8:8+length]
    idat_crc = idat_bytes[8+length:8+length+4]


    idat_dat = zlib.decompress(idat_info)

    if height * ((width * 3) + 1) % len(idat_dat) == 0:
        bytes_por_pixeles = 3
    else:
        bytes_por_pixeles = 4


    matrix = [idat_dat[n-((width*bytes_por_pixeles)+1):n]
              for n in range((width*bytes_por_pixeles)+1,
                             len(idat_dat)+((width*bytes_por_pixeles)+1),
                             (width*bytes_por_pixeles)+1)]


    final = b''

    for fila in range(mini_y):
        final += matrix[fila]


    for fila in range(mini_y, maxi_y, 1):
        array = bytearray(matrix[fila])
        if bytes_por_pixeles == 3:
            b = bytes([255, 255, 255]*(maxi_x-mini_x))
            array[(mini_x * 3)-3+1:(maxi_x*3)-3+1] = b
        else:
            b = bytes([255, 255, 255, 255]*(maxi_x - mini_x))
            array[mini_x + 1:maxi_x + 1] = b

        final += bytes(array)


    for fila in range(maxi_y, len(matrix), 1):
        final += matrix[fila]

    final = zlib.compress(final)

    new_length = len(final).to_bytes(4, byteorder="big")
    type = "IDAT".encode()
    new_crc = zlib.crc32(type+final).to_bytes(4, byteorder="big")

    with open("cut.png", "wb") as file:
        f = dicc["firm"] + dicc["IHDR"] + new_length + type + final + new_crc + dicc["IEND"]
        file.write(f)

#AQUI COMIENZA BUCKET

def bucket(position, img_bytes, color):

    dicc = classify_bytes(img_bytes)

    width, height = width_height(dicc["IHDR"])
    print(width, height)

    idat_bytes = dicc["IDAT"]

    length = int.from_bytes(idat_bytes[:4], byteorder="big")
    type_bytes = idat_bytes[4:8]
    idat_info = idat_bytes[8:8 + length]
    idat_crc = idat_bytes[8 + length:8 + length + 4]

    idat_dat = zlib.decompress(idat_info)

    if height * ((width * 3) + 1) % len(idat_dat) == 0:
        bytes_por_pixeles = 3
    else:
        bytes_por_pixeles = 4

    matrix = [idat_dat[n - ((width * bytes_por_pixeles) + 1):n]
              for n in range((width * bytes_por_pixeles) + 1,
                             len(idat_dat) + ((width * bytes_por_pixeles) + 1),
                             (width * bytes_por_pixeles) + 1)]


    matrix = [group_by(x, bytes_por_pixeles) for x in matrix]


    x_start = position[0]
    y_start = position[1]
    color_base = matrix[y_start][x_start]

    print(color_base)

    checked = set()
    por_revisar = [(x_start, y_start)]


    i = 0

    while len(por_revisar) != 0:
        revisar = por_revisar.pop(0)
        checked.add(revisar)

        if revisar[0] + 1 < len(matrix[0]):
            if matrix[revisar[1]][revisar[0]+1] == color_base and (revisar[0]+1, revisar[1]) not in checked and (revisar[0]+1, revisar[1]) not in por_revisar:
                por_revisar.append((revisar[0]+1, revisar[1]))

            if revisar[1] - 1 > 0:
                if matrix[revisar[1]-1][revisar[0]+1] == color_base and (revisar[0]+1, revisar[1]-1) not in checked and (revisar[0]+1, revisar[1]-1) not in por_revisar:
                    por_revisar.append((revisar[0]+1, revisar[1]-1))

            if revisar[1] + 1 < len(matrix):
                if matrix[revisar[1]+1][revisar[0]+1] == color_base and (revisar[0]+1, revisar[1]+1) not in checked and (revisar[0]+1, revisar[1]+1) not in por_revisar:
                    por_revisar.append((revisar[0]+1, revisar[1]+1))

        if revisar[1] + 1 < len(matrix):
            if matrix[revisar[1]+1][revisar[0]] == color_base and (revisar[0], revisar[1]+1) not in checked and (revisar[0], revisar[1]+1) not in por_revisar:
                por_revisar.append((revisar[0], revisar[1]+1))

        if revisar[0] - 1 > 0:
            if matrix[revisar[1]][revisar[0]-1] == color_base and (revisar[0]-1, revisar[1]) not in checked and (revisar[0]-1, revisar[1]) not in por_revisar:
                por_revisar.append((revisar[0]-1, revisar[1]))

            if revisar[1] - 1 > 0:
                if matrix[revisar[1]-1][revisar[0]-1] == color_base and (revisar[0]-1, revisar[1]-1) not in checked and (revisar[0]-1, revisar[1]-1) not in por_revisar:
                    por_revisar.append((revisar[0]-1, revisar[1]-1))

            if revisar[1] + 1 < len(matrix):
                if matrix[revisar[1]+1][revisar[0]-1] == color_base and (revisar[0]-1, revisar[1]+1) not in checked and (revisar[0]-1, revisar[1]+1) not in por_revisar:
                    por_revisar.append((revisar[0]-1, revisar[1]+1))

        if revisar[1] - 1 > 0:
            if matrix[revisar[1]-1][revisar[0]] == color_base and (revisar[0], revisar[1]-1) not in checked and (revisar[0], revisar[1]-1) not in por_revisar:
                por_revisar.append((revisar[0], revisar[1]-1))


        i += 1


    print(len(idat_dat))

    new_idat_info = b''

    r = 0
    for row in matrix:
        p = 0
        new_row = [0]
        for pixel in row:

            if (p, r) in checked:
                new_row.extend(color)
            else:
                new_row.extend(matrix[r][p])

            p += 1

        r += 1

        new_idat_info += bytes(new_row)

    print(len(new_idat_info), "rev")

    new_idat_info = zlib.compress(new_idat_info)

    new_length = len(new_idat_info).to_bytes(4, byteorder="big")
    type = "IDAT".encode()
    new_crc = zlib.crc32(type+new_idat_info).to_bytes(4, byteorder="big")

    with open("bucket.png", "wb") as file:
        f = dicc["firm"] + dicc["IHDR"] + new_length + type + new_idat_info + new_crc + dicc["IEND"]
        file.write(f)

def group_by(row_bytes, n):
    row_bytes = row_bytes[1:]
    row = [row_bytes[i:i+n] for i in range(0, len(row_bytes), n)]
    return row


if __name__ == '__main__':
    needed = extract_bytes(img_bytes)
    #blurr(needed)
    #cut([(51, 34), (196, 270)], needed)
    bucket((0,0), needed, (0,0,128,255))

