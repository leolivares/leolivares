from PyQt5.uic import loadUiType
from PyQt5.Qt import QApplication, pyqtSignal, QMessageBox, QPixmap, QListWidgetItem
import sys
from clients import Client


form1 = loadUiType("interfaces/login_window.ui")
form2 = loadUiType("interfaces/dashboard.ui")
form3 = loadUiType("interfaces/edit_window.ui")

class LoginWindow(form1[0], form1[1]):

    trigger_check_username = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.client = Client(self)

        self.loginBut.clicked.connect(self.check_username)

        self.trigger_check_username.connect(self.client.check_username)

    def check_username(self):
        username = self.loginLine.text()
        self.trigger_check_username.emit(username)

    def show_popup(self, message):
        popup = QMessageBox.information(self, "ERROR:", message)

    def access_dashboard(self):
        self.dashboard = DashBoardWindow(self.client)
        self.client.trigger_show_image.connect(self.dashboard.show_image)
        self.client.trigger_online_users.connect(self.dashboard.set_users_online)
        self.client.trigger_change_buttons.connect(self.dashboard.change_buttons)
        self.dashboard.show()
        self.close()


class DashBoardWindow(form2[0], form2[1]):

    trigger_change_buttons = pyqtSignal(bytes)


    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.client.parent = self
        self.dashboard_label.setText(self.client.username + "'s Dashboard")

        self.image_labels = [(self.label, None, self.editBut1),
                             (self.label_2, None, self.editBut2),
                             (self.label_3, None, self.editBut3),
                             (self.label_4, None, self.editBut4),
                             (self.label_5, None, self.editBut5),
                             (self.label_6, None, self.editBut6)]

        for l in self.image_labels:
            l[2].clicked.connect(self.edit_screen)

        self.trigger_change_buttons.connect(self.client.change_buttons)
        self.client.request_images()


    def show_image(self, image):
        set = False
        i = 0
        for label in self.image_labels:
            if not set and label[1] is None:
                pixmap = QPixmap()
                pixmap.loadFromData(bytes(image[1]))
                self.image_labels[i] = (label[0], image[0], label[2])
                label[0].setPixmap(pixmap.scaled(150, 200))
                set = True
            i += 1

    def set_users_online(self, users):
        self.usersList.clear()
        for user in users:
            item = QListWidgetItem(user)
            self.usersList.addItem(item)

    def edit_screen(self):
        button = self.sender()

        if button.text() == "Edit":
            permiso = True
            button.setEnabled(False)

        elif button.text() == "Spectate":
            permiso = False

        img = list(filter(lambda x: x[2] == button, self.image_labels))[0][1]
        self.trigger_change_buttons.emit(img)
        self.editscreen = EditWindow(img, permiso, self.client)
        self.editscreen.show()

    def change_buttons(self, img):
        for label in self.image_labels:
            if label[1] == img:
                if label[2].text() == "Edit":
                    label[2].setText("Spectate")
                elif label[2].text() == "Spectate":
                    label[2].setText("Edit")


class EditWindow(form3[0], form3[1]):


    def __init__(self, img, permiso, client):
        super().__init__()
        print("arer")
        self.setupUi(self)
        self.client = client

        print("ggggg")
        self.permiso = permiso
        pixmap = QPixmap()
        pixmap.loadFromData(self.client.request_image)
        print("wwwww")
        self.label.setPixmap(pixmap)




if __name__ == '__main__':
    app = QApplication([])
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
