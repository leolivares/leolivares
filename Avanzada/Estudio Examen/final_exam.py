from collections import deque
import re

def rec(lista):
    print(len(lista))
    print(lista)
    if len(lista) == 0:
        print(0)
        return []

    elif len(lista) == 1 and isinstance(lista[0], int):
        print(" 1 int")
        return [lista[0]**2]

    elif len(lista) == 1 and isinstance(lista[0], list):
        print("1 list")
        return rec(lista)

    else:
        if isinstance(lista[0], int):
            return [lista[0]**2] + rec(lista[-1])
        elif isinstance(lista[0], list):
            return rec(lista[0]) + rec(lista[:len(lista)-1])


print(rec([1, 2, [3, 4, [3, 5]]]))
