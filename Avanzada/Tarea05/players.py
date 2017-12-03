from math import radians ,sin, cos
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.Qt import QTest
from constantes import PUNTAJE_INICIO, PUNTAJE_ENEMIGO

class Player(QObject):

    def __init__(self):
        super().__init__()
        self._rotation = 0
        self.size = 2
        self.max_hp = (self.size * 20) + 100
        self._hp = self.max_hp
        self.velocidad = 5
        self._exp = 0
        self.sizes_level = 2

        self.margen = 28


        self.img_actual = "imagenes/b_walk1.png"
        self.att_actual = "imagenes/b_attack1.png"
        self._pos_x = 378
        self._pos_y = 328
        self.items = [None for _ in range(5)]
        self.gen_move = self.generador_move()
        self.gen_att = self.generador_ataque()
        self.hidden = False
        self._puntaje = PUNTAJE_INICIO

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value >= 360:
            v = value - 360
            self._rotation = v
        elif value < 0:
            self._rotation = 360 - abs(value)
        else:
            self._rotation = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value <= 0:
            self._hp = 0
        elif value > self.max_hp:
            self._hp = self.max_hp
        else:
            self._hp = value

    @property
    def new_hpmax(self):
        pass

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        if value < 0 + self.margen:
            self._pos_x = self.margen
        elif value > 750 + self.margen:
            self._pos_x = 750 + self.margen
        else:
            self._pos_x = value

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        if value < 0 + self.margen:
            self._pos_y = self.margen
        elif value > 610 + self.margen:
            self._pos_y = 610 + self.margen
        else:
            self._pos_y = value

    @property
    def puntaje(self):
        return self._puntaje

    @puntaje.setter
    def puntaje(self, value):
        if value <= 0:
            self._puntaje = 0
        else:
            self._puntaje = value

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        if value >= 1000:
            self._exp = 0
        else:
            self._exp = value

    @property
    def velocidad_ataque(self):
        v = 1000
        c = self.items.count("Fuerza")
        for _ in range(c):
            v -= v * (0.15)
        return v

    @property
    def velocidad_movimiento(self):
        velocidad = self.velocidad
        c = self.items.count("Velocidad")
        for _ in range(c):
            velocidad += velocidad * 0.1
        return velocidad

    @property
    def damage(self):
        return round(((self.size * self.max_hp) / 10), 0)

    def generador_move(self):
        imgs = ["b_walk1", "b_walk2", "b_walk3", "b_walk4"]
        while True:
            for img in imgs:
                imagen_actual = "imagenes/" + img + ".png"
                yield imagen_actual

    def generador_ataque(self):
        imgs = ["b_attack1", "b_attack2", "b_attack3", "b_attack4"]
        while True:
            for img in imgs:
                imagen_actual = "imagenes/" + img + ".png"
                yield imagen_actual

    def mover_adelante(self):
        radianes = radians(self.rotation)

        x = self.velocidad_movimiento * cos(radianes)
        y = self.velocidad_movimiento * sin(radianes)

        if self.rotation >= 0 and self.rotation <= 90:
            x = abs(x)
            y = abs(y)
        elif self.rotation > 90 and self.rotation <= 180:
            x = abs(x) * -1
            y = abs(y)
        elif self.rotation > 180 and self.rotation <= 270:
            x = abs(x) * -1
            y = abs(y) * -1
        elif self.rotation > 270 and self.rotation <= 360:
            x = abs(x)
            y = abs(y) * -1

        x = round(x)
        y = round(y)

        self.pos_x += x
        self.pos_y += y

        self.img_actual = next(self.gen_move)
        return self.pos_x, self.pos_y

    def mover_atras(self):

        radianes = radians(self.rotation)

        x = self.velocidad_movimiento * cos(radianes)
        y = self.velocidad_movimiento * sin(radianes)

        if self.rotation >= 0 and self.rotation <= 90:
            x = abs(x) * -1
            y = abs(y) * -1
        elif self.rotation > 90 and self.rotation <= 180:
            x = abs(x)
            y = abs(y) * -1
        elif self.rotation > 180 and self.rotation <= 270:
            x = abs(x)
            y = abs(y)
        elif self.rotation > 270 and self.rotation <= 360:
            x = abs(x) * -1
            y = abs(y)

        x = round(x)
        y = round(y)

        self.pos_x += x
        self.pos_y += y

        self.img_actual = next(self.gen_move)
        return self.pos_x, self.pos_y

    def girar_izq(self):
        self.rotation -= 5
        self.img_actual = next(self.gen_move)

    def girar_der(self):
        self.rotation += 5
        self.img_actual = next(self.gen_move)

    def bonificacion_ataque(self):
        bonificacion = 0
        cantidad = self.items.count("Fuerza")
        return bonificacion

    def atacar(self, enemigo):
        enemigo.hp -= self.damage + self.bonificacion_ataque()
        if enemigo.hp == 0:
            self.puntaje += 1000 + PUNTAJE_ENEMIGO * (enemigo.size - self.size)
            self.exp += 100 * max(enemigo.size - self.size + 3, 1)

            if self.exp >= 500 and self.sizes_level == 2:
                self.sizes_level -= 1
                self.size += 1
                self.recalcular_maxhp()
            if self.exp == 0:
                if self.sizes_level == 2:
                    self.size += 2
                    self.sizes_level -= 2
                    self.recalcular_maxhp()
                elif self.sizes_level == 1:
                    self.size += 1
                    self.sizes_level -= 1
                    self.recalcular_maxhp()
                self.sizes_level = 2

    def recalcular_maxhp(self):
        maxhp = (self.size * 20) + 100
        cant = self.items.count("Vida")
        for _ in range(cant):
            maxhp += maxhp * 0.2
        self.max_hp = maxhp

    def comprar(self, precio, slot):
        posibles = {750: "Vida", 500: "Fuerza", 250: "Velocidad"}
        if self.puntaje >= precio:
            self.puntaje -= precio
            self.items[slot-1] = posibles[precio]
            return True
        return False

