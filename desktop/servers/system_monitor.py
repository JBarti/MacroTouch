import threading
import socket
import json
from utilities import SystemMonitor


class MonitorServer(threading.Thread):
    """
    
    Klasa koja nasljeđuje od Thread klase
    
    """

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5300):
        """
        
        Inicijalna metoda za MonitorServer. Stvara socket i veže ga na adresu.
        
        Argumenti:
            family {enum AddressFamily} -- tip adrese korišten za sockete
            sock_type {enum SocketKind} -- tip socketa koji će se koristiti
        
        Keyword Argumenti:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
            port {int} -- port na koji će socket biti vezan (default: {5300})
        
        """

        super(MonitorServer, self).__init__()
        self.address = (ip_address, port)
        self.rpi_address = None
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
            data, addr = self.sock.recvfrom(1024)
            self.rpi_address = addr
            if data != "":
                json_data = json.loads(data.decode("ASCII"))
                req_type = json_data["type"]
                if req_type == "GET_SYSTEM_DATA":
                    data = self.request_type[req_type]()
                    self.send_system_data(data)
                else:
                    self.sock.sendto(
                        bytes(json.dumps({"type": "PC_ADDRESS"}), "UTF-8"),
                        self.rpi_address,
                    )

    def get_system_data(self):
        """
        
        Metoda koja se pokreće kad je potrebno dohvaćanje podataka o trenutnom 
        stanju sistema.

        Return:
            [str] -- json string which holds all system data
        
        """

        monitor = SystemMonitor()
        data = monitor.get_system_data()
        json_data = json.dumps(data)
        return json_data

    def send_system_data(self, data):
        """
        
        Metoda koja se poziva kad je potrebno slati podatke o sistemu na MacroTouch.
        
        Argumenti:
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
