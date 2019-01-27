import socket
import threading
import json
from pykeyboard import PyKeyboard

class MacroServer(threading.Thread):

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5200):
        super(MacroServer, self).__init__()
        self.daemon = True
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((ip_address, port))
        self.keyboard = PyKeyboard()

    def run(self):
        while True:
            bytes_data = self.sock.recv(1024)
            str_data = bytes_data.decode("ASCII")
            if len(str_data) == 1:
                self.keyboard.tap_key(str_data)
                continue
            self.handle_macro(str_data)

    def handle_macro(self, data):
        json_macro = json.loads(data)
        for macro in json_macro:
            self.keyboard.press_keys(macro)