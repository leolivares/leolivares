# Bytes
test_1 = bytes(75)
test_2 = bytes([75])

print(test_1)
print(test_2)

with open("encoded.file", "rb") as file:
    corrupted = file.read()

print(len(corrupted))


def sum_ints(corrupted_ints):
    fixed_int = sum(corrupted_ints)
    return fixed_int

def replace_digits(corrupted_int):
    replace_dict = {"1": "9", "2": "8", "3": "7", "4": "6", "5": "0"}
    temp_dict = {y: x for x, y in replace_dict.items()}
    replace_dict.update(temp_dict)

    corrupted_str = str(corrupted_int)
    corrupted_str = corrupted_str.zfill(3)

    mapa = map(lambda x: replace_dict[x] ,corrupted_str)
    lista = "".join(list(mapa))
    return lista

def mirror_int(corrupted_int):
    corrupted_str = str(corrupted_int).zfill(3)
    fixed_string = corrupted_str[::-1]
    fixed_int = int(fixed_string)
    return fixed_int

def fixed_bytes(corrupted_bytes):
    fixed_bytes = bytearray()
    for i in range(0, len(corrupted_bytes), 4):
        corrupted_ints = list(map(int, corrupted_bytes[i:i+4]))
        fixed_ints = sum_ints(corrupted_ints)
        fixed_ints = replace_digits(fixed_ints)
        mirror = mirror_int(fixed_ints)
        fixed_byte = bytes([mirror])
        fixed_bytes.extend(fixed_byte)
    return fixed_bytes

def fix_file(corrupted_file_path, fixed_file_path):
    with open(corrupted_file_path, "rb") as corrupted_file, \
        open(fixed_file_path, "wb") as fixed_file:
        fixed_byte = fixed_bytes(corrupted_file.read())
        print(fixed_byte, "dss")
        fixed_file.write(fixed_byte)


fix_file('encoded.file', 'fixed.jpg')

