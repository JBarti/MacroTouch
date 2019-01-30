import socket
import threading
import json
from pykeyboard import PyKeyboard

k = PyKeyboard()

SPECIAL_KEYS_DICT = {
    "CTRL": k.control_key,
    "ALT": k.alt_key,
    "F1": k.function_keys[1],
    "F2": k.function_keys[2],
    "F3": k.function_keys[3],
    "F4": k.function_keys[4],
    "F5": k.function_keys[5],
    "F6": k.function_keys[6],
    "F7": k.function_keys[7],
    "F8": k.function_keys[8],
    "F9": k.function_keys[9],
    "F10": k.function_keys[10],
    "F11": k.function_keys[11],
    "F12": k.function_keys[12],
    "TAB": k.tab_key,
    "SHIFT": k.shift_key,
    "ESCAPE": k.escape_key,
    "PRTSCR": k.print_screen_key,
    "INSERT": k.insert_key,
    "DELETE": k.delete_key,
    "PAGE_UP": k.page_up_key,
    "PAGE_DOWN": k.page_down_key,
    "HOME": k.home_key,
    "BACKSPACE": k.backspace_key,
    "SUPER": k.super_l_key,
}


class Client(threading.Thread):
    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5300):
        super(Client, self).__init__()
        
        self.address = (ip_address, port)
        self.sock = socket.socket(family, sock_type)
        self.sock.bind(self.address)
        
        self.data = {"system_data": ""}
        self.request_type = {
            "SET_SYSTEM_DATA": self.set_system_data,
            "POST_MACRO_DATA": self.post_macro,
        }

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            
            if data != "":
                json_data = json.loads(data.decode("ASCII"))

                req_type = json_data["type"]
                req_data = json_data["payload"]

                self.request_type[req_type](req_data)

    def post_macro(self, macro_data):
        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        parsed_data = self.parse_macro(macro_data["payload"])

        if not parsed_data:
            return

        data["macros"].append(macro_data["payload"])

        with open("../../data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def parse_macro(self, payload):
        macro = payload["macro"]
        macro = macro.strip().split("+")

        try:
            macro = [SPECIAL_KEYS_DICT[key] for key in macro]
        except KeyError:
            return False

        payload["macro"] = macro

        return payload

    def set_system_data(self, payload):
        self.data["system_data"] = payload

    def get_system_data(self):
        request = {type: "GET_SYSTEM_DATA"}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        self.sock.sendto(bytes_data, self.address)