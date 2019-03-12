import json
import socket
from time import sleep
from threading import Thread
from subprocess import check_output


class ConnectionController:

    """
    
    Klasa koja se bavi povezivanjem uređaja sa računalom korisnika
    
    """

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5010):
        """
        
        Init metoda klase ConnectionController
        
        Arguments:
            family {enum AdressFamily} -- tip adrese korišten za sockete
            sock_type {enum SocketKind} -- tip socketa koji će se korist
        
        Keyword Argumenti:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
        
            port {int} -- port na koji će socket biti vezan (default: {5200})
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip_address, port))
        self.request_type = {"ADD_HOST": self._add_host}

    def start(self):
        """
        
        Jedina "public" metoda iz klase.
        Pri pokretanju se stvara thread koji traži adrese računala koji imaju
        server aplikacije pokrenut. 

        """

        self._clear_all_hosts()

        thread = Thread(target=self._find_pc_address)
        thread.start()

        while True:
            data, addr = self.sock.recvfrom(1024)

            self.request_type[data["type"]](data["payload"], addr)

            if self._thread_is_done(thread):
                break

    def _find_pc_address(self):
        """

        Metoda klase koja pretragom lokalne mreže pronalazi
        računalo na koje se korisnik može spojiti te izmjenjuje ip adrese s njim
        kako biomogućili daljnju komunikaciju

        """
        ips, local_rpi_ip = self._find_addresses()

        request = {"type": "SET_RPI_ADDRESS", "rpi_address": local_rpi_ip}

        bytes_data = bytes(json.dumps(request), "UTF-8")

        for ip in ips:
            if ip[0] == "(":
                ip = ip[1:-1]
            if ip == local_rpi_ip or ip[-3:] == "255" or ip[-2:] == ".0":
                continue
            self.sock.sendto(bytes_data, (ip, 5010))

    def _find_addresses(self):
        """

        Privatna metoda klase koja traži sve adrese na istoj mreži
        kao i uređaj.
        
        Returns:
            list, string -- lista svih adresa na istoj mreži, adresa uređaja   
        
        """

        sleep(1)

        bytes_ip = check_output(["hostname", "-I"])
        local_rpi_ip = bytes_ip.decode("ASCII")[:-1].strip()
        local_ip = ".".join(local_rpi_ip.split(".")[:-1])

        ip_string = check_output(["nmap", "-sL", local_ip + ".*"]).decode("ASCII")

        ips = " ".join(ip_string.split("\n")).split(" ")
        ips = [word for word in ips if local_ip in word]

        return ips, local_rpi_ip

    def _add_host(self, pc_data, addr):

        """
        
        Privatna metoda koja dodaje adresu računala sa pokrenutim serverom aplikacije
        u bazu podataka (data.json)

        Arguments:
            pc_data -- podatci o imenu računala
            addr -- adresa računala koji ima na sebi pokrenut server aplikacije
        
        """

        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        pc_data["address"] = addr

        data["all_hosts"].append({pc_data})

        with open("./data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def _clear_all_hosts(self):

        """
        
        Privatna metoda koja briše iz baze podataka sva računala prije dodana

        """

        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["all_hosts"] = []

        with open("./data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def _thread_is_done(self, thread):

        """
        
        Privatna metoda koja provjerava da li je proslijeđeni Thread gotov
        
        Returns:
            threading.Thread -- thread koji treba provjeriti da li je gotov
        
        """

        if not thread.isAlive:
            sleep(2)
            return True
        return False
