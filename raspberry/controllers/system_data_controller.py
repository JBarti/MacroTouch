import socket
import threading
import json
from subprocess import check_output


class MonitorController(threading.Thread):
    """

    Klasa koja nasljeđuje od Threada. Šalje zahtjeve i dobiva povratni zahtjev s podacima o korištenju 

    """

    def __init__(self, family, sock_type, pc_host, ip_address="0.0.0.0", port=5300):
        """

        Inicijalna metoda klase MonitorController. Stvara svoj socket i binda ga na danu adresu.

        Argumenti:
            family {enum AddressFamily} -- tip adrese korišten za sockete
            sock_type {[type]} -- port na koji će socket biti vezan

        Keyword Argumenti:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
            port {int} -- tip socketa koji će se koristiti (default: {5300})
        """

        super(MonitorController, self).__init__()

        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        self.pc_address = (data["pc_host"], port)

        self.address = (ip_address, port)
        self.sock = socket.socket(family, sock_type)
        self.sock.bind(self.address)

        self.data = {"system_data": ""}
        self.request_type = {"SET_SYSTEM_DATA": self.set_system_data}

    def run(self):
        """

        Metoda run pokreće se pri pokretanju threada.
        Prima zahtjeve na socket klase te poziva funkciju koja će obraditi dobivene podatke

        """

        while True:
            data, _ = self.sock.recvfrom(1024)

            if data != b"":
                json_data = json.loads(data.decode("ASCII"))
                req_type = json_data["type"]
                req_data = json_data["payload"]
                self.request_type[req_type](req_data)

    def get_system_data(self):
        """

        Metoda koja šalje zahtjev na računalo kako bi dobila povratni zahtjev s podacima System monitora

        """

        request = {"type": "GET_SYSTEM_DATA"}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        self.sock.sendto(bytes_data, self.pc_address)

    def set_system_data(self, payload):
        """

        Metoda koja postavlja svojstvo klase na danu vrijednost payloada.

        Argumenti:
            payload {dict} -- {
            "cpus": [int, int, int, int],
            "temp": int,
            "memory": {"total": int, "used": int },
            "disk": {"total": int, "used": int }
        }
        """

        self.data["system_data"] = payload
