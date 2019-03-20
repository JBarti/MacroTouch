import socket
import threading
import json
from subprocess import check_output


class MonitorController(threading.Thread):
    """

    Klasa koja nasljeđuje od Threada. Šalje zahtjeve i dobiva povratni zahtjev s podacima o korištenju 

    """

    def __init__(self, family, sock_type, host="0.0.0.0", port=5300):
        """

        Inicijalna metoda klase MonitorController. Stvara svoj socket i binda ga na danu adresu.

        Arguments:
            family {enum AddressFamily} -- tip adrese korišten za sockete
            sock_type {[type]} -- port na koji će socket biti vezan

        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
            port {int} -- tip socketa koji će se koristiti (default: {5300})
        """

        super(MonitorController, self).__init__()

        self.port = port
        self.host = host
        self.rpi_host = ""
        self.my_ip = ("0.0.0.0", 5300)
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((self.host, self.port))

        self.data = {"cpus": [], "temp": 0, "memory": {"total": 0, "used": 0}}
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
                self.request_type["SET_SYSTEM_DATA"](req_data)

    def get_system_data(self):
        """

        Metoda koja šalje zahtjev na računalo kako bi dobila povratni zahtjev s podacima System monitora

        """

        request = {"type": "GET_SYSTEM_DATA"}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        if self.host[0] == "0":
            return self.data
        self.sock.sendto(bytes_data, (self.host[0], self.port))
        return self.data

    def set_system_data(self, payload):
        """

        Metoda koja postavlja svojstvo klase na danu vrijednost payloada.

        Arguments:
            payload {dict} -- {
            "cpus": [int, int, int, int],
            "temp": int,
            "memory": {"total": int, "used": int },
            "disk": {"total": int, "used": int }
        }
        """
        self.data = payload

