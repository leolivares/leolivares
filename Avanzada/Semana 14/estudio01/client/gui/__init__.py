from .gui import GUI
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

def run(custom_gui):
    app = QApplication([])
    gui = custom_gui()
    app.exec_()
