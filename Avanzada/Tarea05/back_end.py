from PyQt5.QtCore import QThread, QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.Qt import QTest, QPixmap, QSound
from players import Player
from random import expovariate, triangular, uniform, choice
from enemies import Enemigo
from constantes import PUNTAJE_TIEMPO, PUNTAJE_NIVEL
from items import Item
import time
import os


class DCCell(QThread):

    trigger_nuevo_enemigo = pyqtSignal(object)
    trigger_mover_enemigo = pyqtSignal(object)
    trigger_enemy_attack = pyqtSignal(object)
    trigger_player_attack = pyqtSignal()
    trigger_actualizar_puntaje = pyqtSignal()
    trigger_actualizar_exp = pyqtSignal()
    trigger_aparicion_item = pyqtSignal(object)
    trigger_hide_player = pyqtSignal()
    trigger_actualizar_health = pyqtSignal(object)
    trigger_reaparecer_player = pyqtSignal()
    trigger_reajustar_puntaje = pyqtSignal(object)
    trigger_explosion_bomba = pyqtSignal(object)
    trigger_eliminar_entidad = pyqtSignal(object)
    trigger_fin_del_juego = pyqtSignal()
    trigger_change_level = pyqtSignal(int)
    trigger_actualizar_maxhp = pyqtSignal(object)

    def __init__(self, parent, cant):
        super().__init__()
        self.player1 = Player()
        self.parent = parent
        self.enemigos = list()
        self.nivel = 1
        self.finish = False
        self.tasas_aparicion = {1: [1/10, 1, 5, 1],
                                2: [1/8, 1, 6, 3],
                                3: [1/6, 3, 7, 5],
                                4: [1/4, 5, 9, 7],
                                5: [1/2, 7, 10, 9]}
        self.prox_aparicion = 0
        self.calcular_aparicion
        self.inventario_principal = [None for _ in range(5)]
        self.items = []

        self.aparacion = QTimer(self)
        self.aparacion.setInterval(self.prox_aparicion * 1000)
        self.aparacion.timeout.connect(self.aparece_enemigo)

        self.mover_enemigos = QTimer(self)
        self.mover_enemigos.setInterval(500)
        self.mover_enemigos.timeout.connect(self.move_enemies)

        self.enemigo_atacar = QTimer(self)
        self.enemigo_atacar.setInterval(50)
        self.enemigo_atacar.timeout.connect(self.enemy_attack)

        self.jugador_atacar = QTimer(self)
        self.jugador_atacar.setInterval(50)
        self.jugador_atacar.timeout.connect(self.player_attack)

        self.puntaje_supervivencia = QTimer(self)
        self.puntaje_supervivencia.setInterval(1000)
        self.puntaje_supervivencia.timeout.connect(self.survived)

        self.nuevo_item = QTimer(self)
        self.nuevo_item.setInterval(uniform(1, 30) * 1000)
        self.nuevo_item.timeout.connect(self.aparicion_item)

        self.accionar_item = QTimer(self)
        self.accionar_item.setInterval(50)
        self.accionar_item.timeout.connect(self.verificar_items)

        self.enemy_escape = QTimer(self)
        self.enemy_escape.setInterval(50)
        self.enemy_escape.timeout.connect(self.verificar_escapes)

        self.enemy_follow = QTimer(self)
        self.enemy_follow.setInterval(50)
        self.enemy_follow.timeout.connect(self.verificar_follow)

        self.trigger_nuevo_enemigo.connect(parent.nuevo_enemigo)
        self.trigger_mover_enemigo.connect(parent.move_enemy)
        self.trigger_enemy_attack.connect(parent.enemy_attack)
        self.trigger_player_attack.connect(parent.player_attack)
        self.trigger_actualizar_puntaje.connect(parent.actualizar_puntaje)
        self.trigger_actualizar_exp.connect(parent.actualizar_exp)
        self.trigger_aparicion_item.connect(parent.aparicion_item)
        self.trigger_hide_player.connect(parent.esconder_jugador)
        self.trigger_actualizar_health.connect(parent.actualizar_vida)
        self.trigger_reaparecer_player.connect(parent.reaparecer)
        self.trigger_reajustar_puntaje.connect(parent.reajustar_puntaje)
        self.trigger_explosion_bomba.connect(parent.explosion)
        self.trigger_fin_del_juego.connect(parent.finalizar_juego)
        self.trigger_change_level.connect(parent.change_level)
        self.trigger_actualizar_maxhp.connect(parent.maxhp)

    def start_game(self):
        self.start()

        self.aparacion.start()
        self.mover_enemigos.start()
        self.enemigo_atacar.start()
        self.jugador_atacar.start()
        self.puntaje_supervivencia.start()
        self.nuevo_item.start()
        self.accionar_item.start()
        self.enemy_escape.start()
        self.enemy_follow.start()

    @property
    def calcular_aparicion(self):
        self.prox_aparicion = expovariate(self.tasas_aparicion[self.nivel][0])

    def aparece_enemigo(self):
        if not self.finish:
            datos = self.tasas_aparicion[self.nivel]
            size = round(triangular(datos[1], datos[2], datos[3]))

            enemigo = Enemigo(size)

            self.trigger_nuevo_enemigo.emit(enemigo)

            self.enemigos.append(enemigo)

            self.calcular_aparicion
            self.aparacion.setInterval(self.prox_aparicion*1000)

    def survived(self):
        if self.player1.hp > 0 and not self.finish:
            self.player1.puntaje += PUNTAJE_TIEMPO
            self.trigger_actualizar_puntaje.emit()
            self.trigger_actualizar_exp.emit()

    def move_enemies(self):
        for enemigo in self.enemigos:
            if not enemigo.stop_moving:
                self.trigger_mover_enemigo.emit(enemigo)

    def enemy_attack(self):
        if not Enemigo.pause and not self.player1.hidden and not self.finish:
            for enemigo in self.enemigos:
                if self.verificar_circulo(enemigo, self.player1, enemigo.label.width()//2):
                    enemigo.stop_moving = True
                    enemigo.attack(self.player1)
                    self.trigger_enemy_attack.emit(enemigo)
                    QTest.qWait(1000)
                else:
                    enemigo.stop_moving = False

    def player_attack(self):
        if not Enemigo.pause and not self.player1.hidden and not self.finish:
            for enemigo in self.enemigos:
                if enemigo.hp > 0:
                    if self.verificar_circulo(self.player1, enemigo, enemigo.label.width()//2):
                        self.player1.atacar(enemigo)
                        self.trigger_player_attack.emit()
                        QTest.qWait(self.player1.velocidad_ataque)
                        if enemigo.hp == 0:
                            QSound.play("audios/enemy_killed.wav")
                            self.trigger_actualizar_maxhp.emit(self.player1)
                        if enemigo.hp == 0 and self.player1.exp == 0:
                            self.nivel += 1
                            self.trigger_change_level.emit(self.nivel)
                            self.player1.puntaje += 1500 + \
                                                    (PUNTAJE_NIVEL * self.nivel)
                            self.trigger_actualizar_puntaje.emit()

                else:
                    enemigo.rotate.stop()
                    enemigo.stop_moving = True
                    self.remove_enemy(enemigo)
                    enemigo.label.hide()

    def aparicion_item(self):
        if not self.finish:
            self.nuevo_item.setInterval(uniform(1, 30) * 1000)
            item = choice(["vida_extra", "bomba", "puntaje_extra", "safe_zone"])
            nuevo_item = Item(item)
            self.items.append(nuevo_item)
            self.trigger_aparicion_item.emit(nuevo_item)

    def verificar_items(self):
        cerca_item = False
        for item in self.items:
            if self.verificar_circulo(item, self.player1, self.player1.size*15):
                cerca_item = True
                self.activar_item(item)

            if item.item == "bomba":
                for enemigo in self.enemigos:
                    if self.verificar_circulo(item, enemigo, enemigo.size*15):
                        self.activar_item(item)

        if not cerca_item and self.player1.hidden:
            self.player1.hidden = False
            self.trigger_reaparecer_player.emit()

    def activar_item(self, item):
        if item.item == "safe_zone":
            if not self.player1.hidden:
                self.trigger_hide_player.emit()
                self.player1.hidden = True
        elif item.item == "vida_extra":
            QSound.play("audios/grab_health.wav")
            print(self.player1.hp, "antes")
            self.player1.hp = self.player1.max_hp
            print(self.player1.hp, "despues")
            self.trigger_actualizar_health.emit(item)
            self.items.remove(item)
        elif item.item == "bomba":
            self.bomb_explosion(item)
            self.items.remove(item)
        elif item.item == "puntaje_extra":
            QSound.play("audios/coin.wav")
            self.player1.puntaje += 1000
            self.trigger_reajustar_puntaje.emit(item)
            self.items.remove(item)
        else:
            if self.player1.hidden:
                self.trigger_hide_player.emit()
                self.player1.hidden = False

    def remove_enemy(self, enemy):
        self.enemigos.remove(enemy)

    def bomb_explosion(self, bomba):
        QTest.qWait(2000)
        bomba.label.setPixmap(QPixmap("imagenes/explode.png").scaled(35, 40))
        QSound.play("audios/explosion.wav")
        QTest.qWait(1000)

        self.trigger_explosion_bomba.emit(bomba)
        for entidad in self.enemigos + [self.player1]:
            if self.verificar_circulo(bomba, entidad, 80):
                entidad.hp = 0
                self.trigger_eliminar_entidad.emit(entidad)
                if isinstance(entidad, Enemigo):
                    entidad.rotate.stop()
                    entidad.stop_moving = True
                    self.remove_enemy(entidad)
                    entidad.label.hide()
                else:
                    self.parent.healthBar.setValue(self.player1.hp)

    def stop_game(self):
        self.aparacion.stop()
        self.puntaje_supervivencia.stop()
        self.nuevo_item.stop()
        self.accionar_item.stop()
        self.enemy_escape.stop()
        self.enemy_follow.stop()
        Enemigo.pause = True
        for enemigo in self.enemigos:
            enemigo.rotate.stop()
            enemigo.walk.stop()

    def resume_game(self):
        self.aparacion.start()
        self.puntaje_supervivencia.start()
        self.nuevo_item.start()
        self.accionar_item.start()
        self.enemy_escape.start()
        self.enemy_follow.start()
        Enemigo.pause = False
        for enemigo in self.enemigos:
            enemigo.rotate.start()
            enemigo.walk.start()

        max = self.verificar_hp_max()
        self.parent.healthBar.setMaximum(max)
        self.player1.max_hp = max

    def verificar_hp_max(self):
        max = (self.player1.size * 20) + 100
        c = self.player1.items.count("Vida")
        for _ in range(c):
            max += max * 0.2
        return max

    def new_highscore(self, datos):
        name = datos[0]
        points = datos[1]
        level = datos[2]

        if "highscores.txt" not in os.listdir():
            with open("highscores.txt", "w") as file:
                print(",".join([name, str(points), str(level)]), file=file)
                for _ in range(9):
                    print(" ,0,1", file=file)

        else:
            with open("highscores.txt", "r") as file:
                hs = [jug.strip().split(",") for jug in file]

            hs.append([name, points, level])
            hs.sort(key=lambda x: int(x[1]), reverse=True)

            with open("highscores.txt", "w") as file:
                for j in hs[:10]:
                    j = list(map(str, j))
                    print(",".join(j), file=file)

    def verificar_circulo(self, centro, otro, radio):
        circunferencia = (otro.pos_x - centro.pos_x)**2 + (otro.pos_y - centro.pos_y)**2
        if circunferencia <= (radio**2):
            return True
        return False

    def verificar_escapes(self):
        if not self.player1.hidden:
            for enemigo in self.enemigos:
                if enemigo.size < self.player1.size and not enemigo.escape:
                    if self.verificar_circulo(enemigo, self.player1, enemigo.rango_vision):
                        enemigo.escape = True
                        enemigo.escape_player(self.player1.rotation, self.player1.pos_x, self.player1.pos_y)

                elif enemigo.size < self.player1.size and enemigo.escape:
                    if self.verificar_circulo(enemigo, self.player1, enemigo.rango_escape):
                        enemigo.escape = True
                        enemigo.escape_player(self.player1.rotation, self.player1.pos_x, self.player1.pos_y)
                    else:
                        enemigo.escape = False

                else:
                    enemigo.escape = False
        else:
            for enemigo in self.enemigos:
                enemigo.escape = False

    def verificar_follow(self):
        if not self.player1.hidden:
            for enemigo in self.enemigos:
                if enemigo.size > self.player1.size and not enemigo.follow:
                    if self.verificar_circulo(enemigo, self.player1, enemigo.rango_vision):
                        enemigo.follow = True
                        enemigo.follow_player(self.player1.rotation, self.player1.pos_x, self.player1.pos_y)

                elif enemigo.size > self.player1.size and enemigo.follow:
                    if self.verificar_circulo(enemigo, self.player1, enemigo.rango_escape):
                        enemigo.follow = True
                        enemigo.follow_player(self.player1.rotation, self.player1.pos_x, self.player1.pos_y)
                    else:
                        enemigo.follow = False

                else:
                    enemigo.follow = False
        else:
            for enemigo in self.enemigos:
                enemigo.escape = False

    def run(self):
        while self.parent.healthBar.value() > 0 and self.nivel <= 5:
            pass

        self.finish = True
        self.enemigos = []

        if self.nivel == 6:
            self.trigger_fin_del_juego.emit()

        elif self.parent.healthBar.value() <= 0:
            for enemigo in self.enemigos:
                enemigo.label.hide()
            for item in self.items:
                item.label.hide()

            self.trigger_fin_del_juego.emit()

