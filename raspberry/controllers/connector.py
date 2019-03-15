from .connection_controller import ConnectionController
from .wifi_controller import WifiController
import socket
import json


class Connector:
    """
    
    Klasa koja u sebi wrappa ConnectionController i WifiController radi lakšeg korištenja
    
    """

    def __init__(self):
        """
        Metoda koja inicijalizira klasu
        """

        self.wifi = WifiController()
        self.host_finder = ConnectionController(socket.AF_INET, socket.SOCK_DGRAM)

    def scan_wifis(self):

        """
        
        Metoda koja skenira i nalazi sve wifie u blizini
        
        Returns:
            [list] -- lista sa podatcima wifia na u blizini
        """

        return self.wifi.find_nearby_wifis()

    def connect_to_wifi(self, name, password):

        """
        
        Metoda koja se spaja na wifi koji odgovaa proslijeđenom imenu
        
        Arguments:
            name {str} -- ime wifia na koji se korisnik želi spojiti
            password {str} -- šifra wifia ako je potrebna

        Returns:
            [bool] -- vraća True ako je spojeno a false ako je došlo do greške
        """

        return self.wifi.connect_to_wifi(name, password=password)

    def scan_hosts(self):

        """
        
        Skenira sva računala koja imaju pokrenut server aplikacije na sebi
        
        Returns:
            [list] -- lista podataka svih raučunala na kojima je pokrenut server
        """

        self.host_finder.start()
        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        return data["all_hosts"]

    def connect_to_host(self, name):

        """
        
        Metoda koja se spaja na određeno računalo danog imena
        
        Returns:
            [string] -- ime računala koje na sebi ima pokrenut serverski dio aplikacije

        """

        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        selected_host = None

        for host in data["all_hosts"]:
            if host["name"] == name:
                selected_host = host

        if selected_host is not None:
            return False

        data["pc_host"] = selected_host["address"]

        with open("./data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        return True
