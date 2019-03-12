import socket
import json


class MacroController:
    """

    Klasa zadužena za slanje zahtjeva za pritisak ključeva na korisničko računalo

    """

    def __init__(self, port=5200):
        """

        Inicijalna metoda klase

        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"172.21.3.114"})
            port {int} -- tip socketa koji će se koristiti (default: {5200})

        """
        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        self.address = (data["pc_host"], port)

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
            data {list/str} -- [[str, str, str], [str,str]]/str
        """

        with self.spawn_socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            if isinstance(data, list):
                dict_data = {"type": "RUN_MACRO", "payload": data}
            else:
                dict_data = {"type": "TYPE_TEXT", "payload": data}
            print(self.address)
            bytes_data = bytes(json.dumps(dict_data), "UTF-8")
            sock.sendto(bytes_data, self.address)
