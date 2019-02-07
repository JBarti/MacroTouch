import threading
import socket
import json
from utilities import SystemMonitor


class MonitorServer(threading.Thread):
    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5300):
        super(MonitorServer, self).__init__()
        self.address = (ip_address, port)
        self.rpi_address = None
        self.sock = socket.socket(family, sock_type)
        self.sock.bind(self.address)
        self.request_type = {"GET_SYSTEM_DATA": self.get_system_data}

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.rpi_address = addr
            if data != "":
                json_data = json.loads(data.decode("ASCII"))
                req_type = json_data["type"]
                data = self.request_type[req_type]()
                if req_type == "GET_SYSTEM_DATA":
                    self.send_system_data(data)

    def get_system_data(self):
        monitor = SystemMonitor()
        data = monitor.get_system_data()
        json_data = json.dumps(data)
        return json_data

    def send_system_data(self, data):
        request = {"type": "SET_SYSTEM_DATA", "payload": data}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        self.sock.sendto(bytes_data, self.rpi_address)
