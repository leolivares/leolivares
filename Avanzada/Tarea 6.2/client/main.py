from PyQt5.uic import loadUiType
from PyQt5.Qt import QApplication, pyqtSignal, QMessageBox, QPixmap, QListWidgetItem, QLabel, QGraphicsScene, QImage, QGraphicsPixmapItem, QPoint, QColor, QColorDialog, QFileDialog, QDialog
from PyQt5 import QtCore
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
        self.client.username = self.loginLine.text()
        self.dashboard = DashBoardWindow(self.client)
        self.dashboard.show()
        self.close()

class DashBoardWindow(form2[0], form2[1]):

    trigger_change_buttons = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client

        self.client.trigger_update_usernames.connect(self.update_users)
        self.client.trigger_show_image.connect(self.show_image)
        self.client.trigger_change_buttons.connect(self.change_buttons)
        self.client.trigger_update_img_dashboard.connect(self.update_img)
        self.trigger_change_buttons.connect(self.client.change_buttons)

        self.file_dialog = QFileDialog()

        self.client.update_users()
        self.client.parent = self
        self.dashboard_label.setText(self.client.username + "'s Dashboard")

        self.image_labels = [(self.label, None, self.editBut1),
                             (self.label_2, None, self.editBut2),
                             (self.label_3, None, self.editBut3),
                             (self.label_4, None, self.editBut4),
                             (self.label_5, None, self.editBut5),
                             (self.label_6, None, self.editBut6),
                             (self.label_7, None, self.editBut7),
                             (self.label_8, None, self.editBut8),
                             (self.label_9, None, self.editBut9),
                             (self.label_10, None, self.editBut10),
                             (self.label_11, None, self.editBut11),
                             (self.label_12, None, self.editBut12)]

        for l in self.image_labels:
            l[2].clicked.connect(self.edit_screen)

        self.previousBut.clicked.connect(self.previous_page)
        self.nextBut.clicked.connect(self.next_page)
        self.uploadBut.clicked.connect(self.upload)

        self.client.request_images()

    def edit_screen(self):
        button = self.sender()

        if button.text() == "Edit":
            permiso = True
            button.setEnabled(False)

        elif button.text() == "Spectate":
            permiso = False
            button.setEnabled(False)

        img = list(filter(lambda x: x[2] == button, self.image_labels))[0]
        if permiso:
            self.trigger_change_buttons.emit(img[1])
        else:
            button.setEnabled(False)
        self.editscreen = EditWindow(img[1], permiso, self.client, img[3], button)
        self.editscreen.show()


    def update_users(self, online_users):
        self.usersList.clear()
        for user in online_users:
            item = QListWidgetItem(user)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.usersList.addItem(item)

    def show_image(self, image_info):
        set = False
        i = 0
        for label in self.image_labels:
            if not set and label[1] is None:
                set = True
                self.image_labels[i] = (label[0], image_info[0], label[2], self.client.dicc_bytes(bytes(image_info[1])))
                pixmap = QPixmap()
                pixmap.loadFromData(bytes(image_info[1]))

                label[0].setPixmap(pixmap.scaled(150, 200))
            i += 1

    def change_buttons(self, img):
        for label in self.image_labels:
            if label[1] == img:
                if label[2].text() == "Edit":
                    label[2].setText("Spectate")
                elif label[2].text() == "Spectate":
                    label[2].setText("Edit")
                    if not label[2].isEnabled():
                        label[2].setEnabled(True)

    def update_img(self, info):
        label = list(filter(lambda x: x[1] == info[0], self.image_labels))

        if len(label) != 0:
            pixmap = QPixmap()
            pixmap.loadFromData(self.client.create_png(label[0][3], info[1]))
            label[0][0].setPixmap(pixmap.scaled(150, 200))

    def previous_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def next_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def upload(self):
        path = self.file_dialog.getOpenFileName()[0]
        img_name = path.split("/")[-1]

        with open(path, "rb") as file:
            bts = file.read()

        if len(path) != 0:

            if path[len(path)-4:len(path)] == ".png":
                self.client.upload_image(path)

                set = False
                i = 0
                for label in self.image_labels:
                    if not set and label[1] is None:
                        set = True
                        self.image_labels[i] = (label[0], img_name, label[2], self.client.dicc_bytes(bts))
                        pixmap = QPixmap()
                        pixmap.loadFromData(bts)

                        label[0].setPixmap(pixmap.scaled(150, 200))
                    i += 1

            else:
                popup = QMessageBox.information(self, "ERROR:" , "El archivo debe ser de extension .png")


class EditWindow(form3[0], form3[1]):

    def __init__(self, img, permiso, client, dicc, button):
        super().__init__()
        self.setupUi(self)
        self.client = client
        self.img = img
        self.dicc = dicc
        self.client.currently_in = img
        self.button = button

        self.color_dialog = QColorDialog()

        self.client.trigger_set_image_edit.connect(self.set_image)
        self.client.trigger_load_comments.connect(self.load_comments)
        self.client.trigger_add_comment.connect(self.add_comment)
        self.client.trigger_update_img_edit.connect(self.update_img)

        self.commentBut.clicked.connect(self.comment)
        self.blurrBut.clicked.connect(self.blurr)
        self.cutBut.clicked.connect(self.cut)
        self.bucketBut.clicked.connect(self.bucket)
        self.exitBut.clicked.connect(self.close_window)
        self.downloadBut.clicked.connect(self.download)

        self.client.request_image(img)
        self.client.request_comments(img)

        self.closeEvent = self.close_event

        self.permiso = permiso
        self.tool = "Blurr"

        self.pos = []

        self.emojis = {":poop:": u'\U0001F4A9',
                       "O:)": u'\U0001F607',
                       ":D": u'\U0001f604',
                       ";)": u'\U0001F609',
                       "8)": u'\U0001F60E',
                       "U.U": u'\U0001F62D',
                       ":(": u'\U0001F61F',
                       "3:)": u'\U0001F608',
                       "o.o": u'\U0001F633' }

    def set_image(self, img):

        self.scene = QGraphicsScene()
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(bytes(img[1]))

        self.pixMapItem = QGraphicsPixmapItem()
        self.pixMapItem.setPixmap(self.pixmap)

        self.scene.addItem(self.pixMapItem)

        self.grview.setScene(self.scene)

        self.pixMapItem.mousePressEvent = self.pixelSelect
        self.pixMapItem.mouseReleaseEvent = self.pixelSelect

    def pixelSelect(self, event):
        if self.tool == "Cut":
            self.pos.append((event.pos().x(), event.pos().y()))

        elif self.tool == "Bucket":
            color = self.color_dialog.selectedColor()
            r , g, b = color.red(), color.green(), color.blue()
            self.client.bucket((event.pos().x(), event.pos().y()), (r, g, b), self.img)

        if len(self.pos) == 2:
            self.client.cut_image(self.pos, self.img)
            self.pos = []


    def comment(self):
        comment = self.commentLine.text()
        if len(comment) != 0:
            self.client.publish_comment(comment, self.img)
            self.commentLine.clear()

    def add_comment(self, data):
        user = data[1]
        comment = data[0]
        date = data[2]

        complete = "["+date+"]"+" "+user+": "+self.load_emojis(comment)

        item = QListWidgetItem()
        item.setText(complete)
        self.commentList.addItem(item)

    def load_comments(self, comments):
        for comment in comments:
            item = QListWidgetItem()
            c = "["+comment[3]+"] "+comment[1]+": "+self.load_emojis(comment[2])
            item.setText(c)
            self.commentList.addItem(item)

    def blurr(self):
        if self.permiso:
            self.client.blurr_image(self.img)

    def update_img(self, idat_bytes):
        if self.img == idat_bytes[0]:
            self.pixmap.loadFromData(self.client.create_png(self.dicc, idat_bytes[1]))
            self.pixMapItem.setPixmap(self.pixmap)

    def cut(self):
        if self.permiso:
            self.tool = "Cut"

    def bucket(self):
        if self.permiso:
            self.tool = "Bucket"
            self.color_dialog.show()

    def close_window(self):
        self.close()

    def close_event(self, event):
        if self.permiso:
            self.client.trigger_change_buttons.emit(self.img)
        else:
            self.button.setText("Edit")
            self.button.setEnabled(True)


    def download(self):
        self.client.download(self.img)

    def load_emojis(self, comment):
        for emoji in self.emojis:
            if "<"+emoji+">" in comment:
                comment = comment.replace("<"+emoji+">", emoji)

            elif emoji in comment:
                comment = comment.replace(emoji, self.emojis[emoji])
        return comment


if __name__ == '__main__':
    app = QApplication([])
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

