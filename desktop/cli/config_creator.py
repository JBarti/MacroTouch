import socket
import json


class ConfigCreator:
    def __init__(self, ip_address="192.168.0.17", port=5300):
        self.address = (ip_address, port)

    def spawn_socket(self, family, sock_type):
        return socket(family, sock_type)

    def send_data(self, data):
        if not self.check_data(data):
            return False

        data["type"] = "POST_MACRO_DATA"
        bytes_data = bytes(json.dumps(data), "UTF-8")

        with spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(bytes_data, self.address)
        return data

    def check_data(self, data):
        keys = {"position": [], "text": "str", "macro": "str"}

        if not data.keys() == keys.keys():
            return False

        for key, value in keys.items():
            if not isinstance(data[key], type(value)):
                return False

        for i in range(2):
            if not isinstance(data["position"], int):
                return False

        return data

    def create_macro(self):
        text = input("Macro name: ")
        macro = input("Key combination (ex: CTRL+A): ")
        position = map(int, input("Position (ex: 1x1): ").split("x"))

        return self.send_data({"position": position, "macro": macro, "text": text})
