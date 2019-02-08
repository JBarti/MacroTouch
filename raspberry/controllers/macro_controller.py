import socket
import json


class MacroController:
    """

    Klasa zadužena za slanje zahtjeva za pritisak ključeva na korisničko računalo
    
    """

    def __init__(self, ip_address="172.21.3.114", port=5200):
        """
        
        Inicijalna metoda klase
        
        Keyword Argumenti:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"172.21.3.114"})
            port {int} -- tip socketa koji će se koristiti (default: {5200})
        """

        self.address = (ip_address, port)

    def spawn_socket(self, family, sock_type):
        """
        
        Metoda koja stvara objekt socketa
        
        Argumenti:
            family {enum AddressFamily} -- tip adrese korišten za sockete 
            sock_type {enum SocketType} -- port na koji će socket biti vezan 
        
        Return:
            [socket] -- virtualni socket
        """

        return socket.socket(family, sock_type)

    def send_key_press(self, key):
        """
        
        Metoda koja prima tipku i šale zahtjev za pritiskom te tipke na korisničkom računalu
        
        Arguments:
            key {str} -- numerička oznaka tipke ili samo slovo tipke

        """

        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

            dict_data = {"type": "RUN_MACRO", "payload": key}
            data = bytes(json.dumps(dict_data), "UTF-8")
            sock.sendto(data, self.address)

    def send_key_combo(self, list_of_macros):
        """

        Metoda koja prima niz tipki i šale zahtjev za pritiskom tih tipki na korisničkom računalu

        
        Argumenti:
            list_of_macros {list} -- lista listi, gdje svaka podlista djeluje kao makro naredba
        """

        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            dict_data = {"type": "RUN_MACRO", "payload": list_of_macros}
            data = bytes(json.dumps(dict_data), "UTF-8")
            sock.sendto(data, self.address)
