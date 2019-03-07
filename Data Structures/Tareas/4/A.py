n_boys = int(input())
boys = []
if n_boys > 0:
    boys = input().split()
    boys = list(map(int, boys))

n_girls = int(input())
girls = []
if n_girls > 0:
    girls = input().split()
    girls = list(map(int, girls))


boys.sort(reverse=True)
girls.sort(reverse=True)

matches = 0

while boys and girls:

    if abs(int(boys[-1]) - int(girls[-1])) <= 1:
        matches += 1
        boys.pop()
        girls.pop()

    elif int(boys[-1]) > int(girls[-1]):
        x = girls.pop()

    else:
        x = boys.pop()

print(matches)