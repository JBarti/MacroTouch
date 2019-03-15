import socket
import json
from subprocess import check_output


class ConnectionServer:

    """
    
    Klasa čija je namjena povezivanje sa uređajem
    
    """

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5010):
        """
        
        Inicijalna metoda klase
        
        Arguments:
            family {enum AdressFamily} -- tip adrese korišten za sockete
            sock_type {enum SocketKind} -- tip socketa koji će se korist
        
        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
        
            port {int} -- port na koji će socket biti vezan (default: {5200})
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip_address, port))
        self.user_name = bytes.decode(check_output("hostname"))[:-1]

    def start(self):

        """
        
        Metoda koja čeka na vezu od uređaja 
        
        Returns:
            [string] -- string koji predstavlja adresu uređaja
            
        """

        _, addr = self.sock.recvfrom(1024)
        self.sock.sendto(
            bytes(
                json.dumps({"type": "ADD_HOST", "payload": {"name": self.user_name}}),
                "UTF-8",
            ),
            addr,
        )
        return addr[0]
