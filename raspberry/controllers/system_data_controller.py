import socket
import threading
import json


class MonitorController(threading.Thread):
    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5300):
        super(MonitorController, self).__init__()

        self.address = (ip_address, port)
        self.sock = socket.socket(family, sock_type)
        self.sock.bind(self.address)

        self.data = {"system_data": ""}
        self.request_type = {"SET_SYSTEM_DATA": self.set_system_data}

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            if data != "":
                json_data = json.loads(data.decode("ASCII"))

                req_type = json_data["type"]
                req_data = json_data["payload"]

                self.request_type[req_type](req_data)

    def get_system_data(self):
        request = {type: "GET_SYSTEM_DATA"}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        self.sock.sendto(bytes_data, ("172.21.3.114", 5300))

    def set_system_data(self, payload):
        self.data["system_data"] = payload
