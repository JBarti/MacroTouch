from bluetooth import *
from pynput.mouse import Controller
from threading import Thread
from pynput.mouse import Controller
import pyautogui

server_mac_adress = "B8:27:EB:F8:29:80"
port = 0x1001
size = 2048
mouse = Controller()


def change_mouse_pos(data):
    try:
        print(data)
        data = data.decode('UTF-8')
        data = list(map(int, data.split(" ")))
        x, y = data
        pyautogui.moveTo(x, y, 0.01)
    except ValueError:
        print("VALUE ERROR")


socket = BluetoothSocket(L2CAP)
socket.connect((server_mac_adress, port))
while 1:
    data = socket.recv(1024)
    Thread(target=change_mouse_pos, args=(data, )).start()
