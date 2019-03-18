from .connection_controller import ConnectionController
from .wifi_controller import WifiController
from .system_data_controller import MonitorController
from .macro_controller import MacroController
from .mouse_controller import MouseController
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
        self.macro_controller = MacroController()
        self.mouse_controller = MouseController(socket.AF_INET, socket.SOCK_DGRAM)
        self.monitor_controller = MonitorController(socket.AF_INET, socket.SOCK_DGRAM)
        self.connected_ip = ""

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
            [str] -- vraća ime računala, u slučaju da nije povezan podiže se ConnectionError
        """

        return self.wifi.connect_to_wifi(name, password=password)

    def scan_hosts(self):

        """
        
        Skenira sva računala koja imaju pokrenut server aplikacije na sebi
        
        Returns:
            [list] -- lista podataka svih raučunala na kojima je pokrenut server
        """

        self.host_finder.start()

    def connect_to_host(self, name):

        """
        
        Metoda koja se spaja na određeno računalo danog imena
        
        Returns:
            [string] -- ime računala koje na sebi ima pokrenut serverski dio aplikacije, ili podiže
                        ConnectionError u slučaju nemogućnosti spajanja

        """

        selected_host = None

        for host in self.host_finder.hosts:
            if host["name"] == name:
                selected_host = host

        if selected_host is None:
            raise ConnectionError()

        self.connected_ip = selected_host["address"]
        self._set_ip()

        return name

    def _set_ip(self):

        """
        
        Metoda koja na poziv postavlja host od računala 

        """
        print(self.connected_ip)
        self.macro_controller.host = self.connected_ip
        self.mouse_controller.host = self.connected_ip
