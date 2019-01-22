from bluetooth import *


class Server:
    def __init__(self):
        self.socket = BluetoothSocket(L2CAP)
        self.socket.bind(("", 0x1001))
        self.socket.listen(1)
        client, adress = self.socket.accept()
        print("Connected to client {}".format(adress))
