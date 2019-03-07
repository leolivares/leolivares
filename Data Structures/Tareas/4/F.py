


def handle_names():
    current_names = dict()
    library = dict()

    n = int(input())

    for _ in range(n):
        old, new = input().split()

        if old not in library:
            current_names[old] = [new]
            library[new] = old
            library[old] = old


        else:
            library[new] = library[old]
            parent = library[old]
            current_names[parent].append(new)


    return current_names


if __name__ == '__main__':
    current_names = handle_names()
    print(len(current_names))
    for name in current_names:
        print(name, current_names[name][-1])
