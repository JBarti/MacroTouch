import socket
import json


class ConnectionServer:

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5010):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip_address, port))

    def start(self):
        _, addr = self.sock.recvfrom(1024)
        self.sock.sendto(
            bytes(json.dumps({"type": "PC_ADDRESS"}), "UTF-8"), addr
        )
        return addr[0]
