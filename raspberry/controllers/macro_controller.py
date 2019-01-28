import socket
import json


class MacroController:
    def __init__(self, ip_address="192.168.0.17", port=5200):
        self.address = (ip_address, port)

    def spawn_socket(self, family, sock_type):
        return socket(family, sock_type)

    def send_key_press(self, key):
        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as socket:
            key = bytes(key, "UTF-8")

            socket.sendto(key, self.address)

    def send_key_combo(self, list_of_macros):  # type(key_combo) --> string
        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as socket:
            str_of_macros = json.dumps(list_of_macros)

            socket.sendto(bytes(str_of_macros, "UTF-8"), self.address)


# {type:"RUN_MACRO", payload:[]}
# {type:"TAP_KEY", payload:""}
