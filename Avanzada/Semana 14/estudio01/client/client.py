import socket
import threading
import json
from gui import GUI, run
from PyQt5.QtCore import QObject, pyqtSignal

class Client(QObject):

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5556
        self.connected = False

        self.mails = []

        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_client.connect((self.host, self.port))
            self.connected = True

            thread = threading.Thread(target=self.listen_server, daemon=True)
            thread.start()

        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionError):
            print("No se pudo conectar")
            self.socket_client.close()

    def listen_server(self):
        while True:
            msg = self.socket_client.recv(1024)
            msg = msg.decode("UTF-8")
            msg = json.loads(msg)

            self.handle_mess(msg)

    def verificar_ingreso(self, username):
        msg = {"status": "ingreso", "data": username}
        msg = json.dumps(msg)
        msg = msg.encode()

        self.socket_client.send(msg)


    def handle_mess(self, msg):
        if msg["status"] == "ingreso":
            if msg["data"]:
                pass

        if msg["status"] == "mail":
            pass



class MiGUI(GUI):

    trigger_verificar_usuario = pyqtSignal(str)
    trigger_get_mails = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cliente = Client()

        self.trigger_verificar_usuario.connect(self.cliente.verificar_ingreso)
        self.trigger_get_mails.connect(self.cliente.get_mails)

    def on_signin_dialog_signin_button_click(self, username, password):
        """Callback luego de presionar el botón `Ingresar` en diálogo de ingreso.
        Si es que no se está haciendo el BONUS, `password` será un string
        vacío.

        Retorna:
            bool -- si el ingreso es exitoso, es verdadero. En otro caso, falso.
        """
        self.trigger_verificar_usuario.emit(username)

    def on_signup_dialog_signup_button_click(self, username, password, confirm_password):
        """Callback luego de presionar el botón `Registrarse` en diálogo de registro.
        Si es que no se está haciendo el BONUS, no se muestra el botón `Registrarse`.

        Retorna:
            bool -- si el registro es exitoso, es verdadero. En otro caso, falso.
        """
        return True

    def on_main_window_load(self):
        """Callback luego de cargarse la ventana principal.
        """
        pass

    def on_main_window_inbox_button_click(self):
        """Callback luego de presionar el botón `Buzón de entrada` en ventana
        principal.
        """
        pass

    def on_main_window_outbox_button_click(self):
        """Callback luego de presionar el botón `Buzón de salida` en ventana
        principal.
        """
        pass

    def on_main_window_signout_button_click(self):
        """Callback luego de presionar el botón `Desconectarse` en ventana
        principal.
        """
        pass

    def on_main_window_item_double_click(self, row):
        """Callback luego de hacer click en alguna fila de la tabla de la
        ventana principal.

        Argumentos:
            int row -- el índice de la fila dónde se hizo click.
        """
        pass

    def on_compose_widget_send_button_click(self, recipients, subject, msg):
        """Callback luego de presionar el botón `Enviar` en la ventana de
        redacción de correos.

        Argumentos:
            str recipients -- destinatarios de correo.
            str subject    -- asunto del correo.
            str msg        -- cuerpo del correo.
        Retorna:
            bool           -- si el envío es exitoso, retorna verdadero. En
            otro caso, retorna falso.
        """
        return True

if __name__ == "__main__":
    run(MiGUI)
