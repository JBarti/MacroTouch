import socket
import json


class MacroController:
    def __init__(self, ip_address="192.168.0.17", port=5200):
        self.address = (ip_address, port)

    def spawn_socket(self, family, sock_type):
        return socket.socket(family, sock_type)

    def send_key_press(self, key):
        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            dict_data = {"type":"RUN_MACRO", "payload":key}

            data = bytes(json.dumps(dict_data), "UTF-8")

            sock.sendto(data, self.address)

    def send_key_combo(self, list_of_macros):  # type(key_combo) --> string
        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

            dict_data = {"type":"RUN_MACRO", "payload":list_of_macros}

            data = bytes(json.dumps(dict_data), "UTF-8")

            sock.sendto(data, self.address)