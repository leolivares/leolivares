from random import randint
from PyQt5.QtWidgets import QLabel

class Item:

    def __init__(self, item):
        self.item = item
        self.pos_x = randint(20, 730)
        self.pos_y = randint(20, 580)
        self.label = QLabel()
