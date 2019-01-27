import socket
import threading
import json
from pykeyboard import PyKeyboard

class Client(threading.Thread):

    def __init__(self, conn):
        super(Client, self).__init__()
        self.conn = conn
        self.daemon = True
        self.data =""

    def run(self):
        while True:
            self.data = self.data + self.conn.recv(1024)
            if self.data != "":
                macro_json = json.loads(self.data.decode("ASCII"))
                if "system" in macro_json.keys():
                    pass
                self.update_json(macro_json)
                self.data=""

    def update_json(self, macro_data):
        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        parsed_data = self.parse_payload(macro_data[payload])

        if not parsed_data:
            return

        data["macros"].append(macro_data["payload"])

        with open("../../data.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        

    def parse_payload(self, payload):
        macro = payload["macro"]
        macro = macro.strip().split("+")

        try:
            macro = [SPECIAL_KEYS_DICT[key] for key in macro]
        except KeyError:
            return False

        payload["macro"] = macro

        return payload
#{type:MACRO_POST, payload:{name:"", keys:""}}
    
    def get_system_data(self)
        

    def close_connection(self):
        self.conn.close()

## server = ConfigController(family-socketa, socket-type, ip_address=, port=)  --> (ip_address, port su kwargs)

class ConfigController:
    
    def __init__(self, family, sock_type, ip_address="192.168.0.17", port=5300):
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((ip_address, port))

    def run(self):
        conn, address = self.sock.accept()
        client = Client(conn)
        client.start()


        
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