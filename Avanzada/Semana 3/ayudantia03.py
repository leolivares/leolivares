from collections import defaultdict

dicc = defaultdict(int)
dicc["algo"] += 1
print(dicc)

print(dicc.items())

for p, q in dicc.items():
    print(p, ":", q) +

a = ["a", "b", "b", "c", "d", "d"]
se = set(a)
print(se)
print(list(se))