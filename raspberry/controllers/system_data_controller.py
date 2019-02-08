import socket
import threading
import json
from subprocess import check_output


class MonitorController(threading.Thread):
    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5300):
        super(MonitorController, self).__init__()

        self.address = (ip_address, port)
        self.pc_address = None
        self.sock = socket.socket(family, sock_type)
        self.sock.bind(self.address)

        self.data = {"system_data": ""}
        self.request_type = {"SET_SYSTEM_DATA": self.set_system_data}

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            self.pc_address = addr

            if data != "":
                json_data = json.loads(data.decode("ASCII"))

                req_type = json_data["type"]

                if req_type == "SET_SYSTEM_DATA":
                    req_data = json_data["payload"]
                    self.request_type[req_type](req_data)

    def get_system_data(self):
        request = {"type": "GET_SYSTEM_DATA"}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        self.sock.sendto(bytes_data, self.pc_address)

    def set_system_data(self, payload):
        self.data["system_data"] = payload

    def find_pc_address(self):
        bytes_ip = check_output("hostname -I")
        local_rpi_ip = bytes_ip.decode("ASCII")[:-1].strip()
        local_ip = ".".join(local_rpi_ip.split(".")[:-1]) + ".*"
        ip_string = check_output(["nmap", "-sP", local_ip])
        ips = " ".join(ip_string.split("\n")).split(" ")
        ips = [word for word in ips if local_ip in word]

        request = {"type": "SET_RPI_ADDRESS", "rpi_address": local_rpi_ip}

        bytes_data = bytes(json.dumps(request), "UTF-8")

        for ip in ips:
            if ip[0] == "(":
                ip = ip[1:-1]
            if ip == local_rpi_ip or ip[-3:] == "255" or ip[-1:] == "0":
                continue
            self.sock.sendto(bytes_data, (ip, 5300))
