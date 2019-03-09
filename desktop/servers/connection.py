import socket
import json
from subprocess import check_output


class ConnectionServer:

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5010):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip_address, port))
        self.user_name = bytes.decode(check_output("hostname"))[:-1]

    def start(self):
        _, addr = self.sock.recvfrom(1024)
        self.sock.sendto(
            bytes(json.dumps({"type": "ADD_HOST", "payload":{"name":self.user_name}}), "UTF-8"), addr
        )
        return addr[0]
