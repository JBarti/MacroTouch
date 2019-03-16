import threading
import socket
import json
from .monitor_utilities import SystemMonitor


class MonitorServer(threading.Thread):
    """

    Klasa koja nasljeđuje od Thread klase

    """

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5300):
        """

        Inicijalna metoda za MonitorServer. Stvara socket i veže ga na adresu.

        Arguments:
            family {enum AddressFamily} -- tip adrese korišten za sockete
            sock_type {enum SocketKind} -- tip socketa koji će se koristiti

        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
            port {int} -- port na koji će socket biti vezan (default: {5300})

        """

        super(MonitorServer, self).__init__()
        self.port = port
        self.address = (ip_address, self.port)
        self.rpi_address = (ip_address, self.port)
        self.sock = socket.socket(family, sock_type)
        self.sock.bind(self.address)
        self.request_type = {"GET_SYSTEM_DATA": self.get_system_data}

    def run(self):
        """

        Metoda run pokreće se pri pokretanju Threada. 
        Prima zahtjeve sa socketa, ovisno ozahtjevu poziva metode koje ih obrade. 
        Također šalje podatke

        """

        while True:
            data, _ = self.sock.recvfrom(1024)
            if data != b"":
                json_data = json.loads(data.decode("ASCII"))
                req_type = json_data["type"]
                data = self.request_type[req_type]()
                self.send_system_data(data)

    def get_system_data(self):
        """

        Metoda koja se pokreće kad je potrebno dohvaćanje podataka o trenutnom 
        stanju sistema.

        Returns:
            [str] -- json string which holds all system data

        """

        monitor = SystemMonitor()
        data = monitor.get_system_data()
        json_data = json.dumps(data)
        return json_data

    def send_system_data(self, data):
        """

        Metoda koja se poziva kad je potrebno slati podatke o sistemu na MacroTouch.

        Arguments:
            data {dict} -- {
            "cpus": [int, int, int, int],
            "temp": int,
            "memory": {"total": int, "used": int },
            "disk": {"total": int, "used": int }
        } 
        objekt rječnika koji sadrži sve podatke o sistemu

        """

        request = {"type": "SET_SYSTEM_DATA", "payload": data}
        bytes_data = bytes(json.dumps(request), "UTF-8")
        self.sock.sendto(bytes_data, self.rpi_address)

