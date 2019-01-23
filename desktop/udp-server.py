import socket
from threading import Thread
import pyautogui
from pymouse import PyMouse

pyautogui.FAILSAFE = False
UDP_IP = "0.0.0.0"
UDP_PORT = 5005

m = PyMouse()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.bind((UDP_IP, UDP_PORT))

print("SERVER STARTED")

array = []


def change_mouse_pos(data):
    try:
        data = data.decode("UTF-8")
        data = list(map(int, data.split(" ")))
        x, y = data
        array.append((x, y))
        print("ADDDED")
        # pyautogui.moveTo(x, y, 0.01)

    except ValueError:
        print("VALUE ERROR")


def run_moveto():
    while True:
        if array:
            x, y = array.pop()
            # m.move(x,y)
            pyautogui.moveTo(x, y)


th1 = Thread(target=run_moveto)
th1.daemon = True
th1.start()


while True:
    data, addr = sock.recvfrom(1024)
    th2 = Thread(target=change_mouse_pos, args=(data,))
    th2.daemon = True
    th2.start()
