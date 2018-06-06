import cv2
import re
import requests
import serial
import syslog
import time
from PIL import Image
from pyzbar.pyzbar import decode


PORT = '/dev/cu.wchusbserial1410'
ard = serial.Serial(PORT, 9600, timeout=5)
URL = 'http://149.28.111.146/insert/record/'


def get_rut(code):
    c = code.data
    c = c.decode('utf-8')
    rut = re.search('[0-9]*-[0-9K]', c)
    return rut.group()


def get_rutq():
    rut = None
    done = False
    capture = cv2.VideoCapture(0)

    while not done:

        ret, frame = capture.read()
        cv2.imshow('Current', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        image = Image.fromarray(gray)
        code = decode(image)

        if code:
            try:
                rut = get_rut(code[0])

            except AttributeError:
                print("Este código QR no es válido")
                print(code)

        cv2.waitKey(1)
        if cv2.waitKey(1) and rut:
            done = True

    return rut


def post(rut, weights):
    total_w = sum(weights)
    payload = {'inserted_by': rut, 'material': 1,
               'peso': total_w, 'redeemed': False}
    r = requests.post(URL, data=payload, verify=False)
    print(r)

def run():

    while True:
        done = False
        rut = get_rutq()
        print("Bienvenido, usuario {}".format(rut))

        if rut:
            print(len(rut), "RUTL")
            response = "getw"
            ard.flush()
            print("Python value sent: {}".format(response))
            ard.write(response.encode('utf-8'))
            time.sleep(1)

            pesos = list()

            while not done:
                msg_btes = ard.read(ard.inWaiting())
                decoded = msg_btes.decode('utf-8').strip()
                if msg_btes:
                    print("Message from arduino: {}"
                          .format(decoded))

                    if "kg" in decoded:
                        print(decoded, "DECODED")
                        w = re.search('[0-9]+\.[0-9]+', decoded)
                        weight = float(w.group(0))
                        print(weight, "chequear")
                        pesos.append(weight)

                    elif decoded == "exit":
                        done = True
                        print("ENTRE AQUI")

                time.sleep(0.5)

            post(rut, pesos)


if __name__ == '__main__':
    run()





