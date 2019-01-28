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
        self.request_type = {
            "RUN_MACRO": self.handle_macro,
            "TAP_KEY": self.keyboard.tap_key,
        }

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if data != "":
                json_data = json.loads(data.decode("ASCII"))

                request_type = json_data["type"]
                request_data = json_data["payload"]

                self.request_type[json_data["type"]](json_data["payload"])

    def handle_macro(self, data):
        json_macro = json.loads(data)
        for macro in json_macro:
            self.keyboard.press_keys(macro)
