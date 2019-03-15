import socket
import json


class MouseController:
    """

    Klasa koja se bavi slanjem lokacije miša s Raspberry Pi-a na računalo

    """

    def __init__(self, family, sock_type, host="0.0.0.0", port=5005):
        """

        Inicijalna metoda klase MouseController. Stvara svoj socket

        Arguments:
            family {enum AddressFamily} -- tip adrese korišten za sockete 
            sock_type {enum SocketType} -- port na koji će socket biti vezan

        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"172.21.3.114"})
            port {int} -- tip socketa koji će se koristiti (default: {5100})
        """

        self.sock = socket.socket(family, sock_type)
        self.host = host
        self.port = port

    def send_location_data(self, location):
        """

        Metoda klase koja se bavi slanjem lokacije miša na korisničko računalo

        Arguments:
            location {list} -- [int, int]

        """

        position_x = str(location[0])
        position_y = str(1 - location[1])

        str_mouse_location = position_x + " " + position_y

        location = bytes(str_mouse_location, "UTF_8")
        self.sock.sendto(location, (self.host, self.port))

    def send_click_data(self, click_type):
        """

        Ova metoda je u mougćnosti poslati informaciju o kliku mišem na računalo

        Arguments:
            click_type {int} -- int koji predstavlja da li je poslan lijevi klik ili desni klik
        
        """

        click_type = str(click_type)

        click = bytes(click_type, "UTF-8")
        self.sock.sendto(click, (self.host, self.port))
