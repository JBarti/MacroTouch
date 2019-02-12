import json
from threading import Thread
import socket
from subprocess import check_output
from time import sleep


class ConnectionController:

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5010):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip_address, port))

    def start(self):
        thread = Thread(target=self.find_pc_address)
        thread.start()
        _, addr = self.sock.recvfrom(1024)
        return addr[0]

    def find_pc_address(self):
        """

        Metoda klase koja pretragom lokalne mreže pronalazi
        računalo na koje se korisnik može spojiti te izmjenjuje ip adrese s njim
        kako biomogućili daljnju komunikaciju

        """
        sleep(1)
        bytes_ip = check_output(["hostname", "-I"])
        local_rpi_ip = bytes_ip.decode("ASCII")[:-1].strip()
        local_ip = ".".join(local_rpi_ip.split(".")[:-1])
        ip_string = check_output(
            ["nmap", "-sL", local_ip+".*"]).decode("ASCII")
        ips = " ".join(ip_string.split("\n")).split(" ")
        ips = [word for word in ips if local_ip in word]

        request = {"type": "SET_RPI_ADDRESS", "rpi_address": local_rpi_ip}

        bytes_data = bytes(json.dumps(request), "UTF-8")

        for ip in ips:
            if ip[0] == "(":
                ip = ip[1:-1]
            if ip == local_rpi_ip or ip[-3:] == "255" or ip[-2:] == ".0":
                continue
            self.sock.sendto(bytes_data, (ip, 5010))
