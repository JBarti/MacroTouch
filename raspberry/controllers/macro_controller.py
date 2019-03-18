import socket
import json


class MacroController:
    """

    Klasa zadužena za slanje zahtjeva za pritisak ključeva na korisničko računalo

    """

    def __init__(self, host="0.0.0.0", port=5200):
        """

        Inicijalna metoda klase

        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"172.21.3.114"})
            port {int} -- tip socketa koji će se koristiti (default: {5200})

        """
        self.host = host
        self.port = port

    def spawn_socket(self, family, sock_type):
        """

        Metoda koja stvara objekt socketa

        Arguments:
            family {enum AddressFamily} -- tip adrese korišten za sockete 
            sock_type {enum SocketType} -- port na koji će socket biti vezan 

        Returns:
            [socket] -- virtualni socket
        """

        return socket.socket(family, sock_type)

    def send_data(self, data):
        """

        Metoda koja prima niz tipki i šale zahtjev za pritiskom tih tipki na korisničkom računalu


        Arguments:
            data {list/str} -- vraća listu koja se sastoji od nizova makro naredbi ili samo jedan makro u obliku stringa
                               [[str, str, str], [str,str], ...] ili str
        """

        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

            dict_data = {"type": "RUN_MACRO", "payload": data}
            bytes_data = bytes(json.dumps(dict_data), "UTF-8")
            sock.sendto(bytes_data, (self.host, self.port))
