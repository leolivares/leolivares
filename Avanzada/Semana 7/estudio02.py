def ar(*args):
    et = yield
    xt1 = 0
    xt2 = 0
    while True:
        xt = (xt1 * args[0] + xt2 * args[1] + et + args[2])
        xt2 = xt1
        xt1 = xt
        et = yield xt


n = [1, 2, 3]
m = ar(-1.0, 1.0, 1.0)
m.send(None)
y = [m.send(i) for i in n]

print(y)

def ar(*args):
    et = yield(float)
    xt = [1.0 for _ in range(len(args) - 1)]

    while True:
        xtc = sum(map(lambda x: x[0] * x[1], zip(xt + [et], args)))
        xt = [xtc] + xt[:-1]
        et = yield xtc

n = [1.0, 2.0, 3.0]
m = ar(-1.0, 1.0, 3.0)
next(m)
y = [m.send(i) for i in n]

print(y)