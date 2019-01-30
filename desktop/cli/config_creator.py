import socket
import json

STRUCTURE = {"position": [], "text": "str", "macro": "str"}


class ConfigCreator:
    def __init__(self, ip_address="192.168.0.17", port=5300):
        self.address = (ip_address, port)


    def spawn_socket(self, family, sock_type):
        return socket.socket(family, sock_type)


    def create_macro(self):
        text = input("Macro name: ")
        macro = input("Key combination (ex: CTRL+A): ")
        position = map(int, input("Position (ex: 1x1): ").split("x"))

        return self.send_data({"position": position, "macro": macro, "text": text})


    def check_data(self, data, struct=STRUCTURE):

        if isinstance(struct, dict) and isinstance(data, dict):
            if struct.keys() != data.keys():
                return False
            return all(k in data and self.check_data(data[k], struct[k]) for k in struct)
        
        if isinstance(struct, list) and isinstance(data, list):
            if len(struct) != len(data):
                return False
            return all(self.check_data(c, struct[0]) for c in data)
        
        elif isinstance(struct, type):
            return isinstance(data, struct)
        
        else:
            return False

    
    def send_data(self, data):
        if not self.check_data(data):
            return False

        data["type"] = "POST_MACRO_DATA"
        bytes_data = bytes(json.dumps(data), "UTF-8")

        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(bytes_data, self.address)
        return data