import socket
import json

class MouseController:
    """

    Klasa koja se bavi slanjem lokacije miša s Raspberry Pi-a na računalo

    """

    def __init__(self, family, sock_type, pc_host, port=5100):
        """

        Inicijalna metoda klase MouseController. Stvara svoj socket

        Argumenti:
            family {enum AddressFamily} -- tip adrese korišten za sockete 
            sock_type {enum SocketType} -- port na koji će socket biti vezan

        Keyword Argumenti:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"172.21.3.114"})
            port {int} -- tip socketa koji će se koristiti (default: {5100})
        """

        self.sock = socket.socket(family, sock_type)
        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        self.address = (data["pc_host"], port)

    def send_location_data(self, location):
        """

        Metoda klase koja se bavi slanjem lokacije miša na korisničko računalo

        Argumenti:
            location {list} -- [int, int]

        """

        position_x = str(location[0])
        position_y = str(location[1])

        str_mouse_location = position_x + " " + position_y

        location = bytes(str_mouse_location, "UTF_8")
        self.sock.sendto(location, self.address)

    def send_click_data(self, click_type):
        """

        Ova metoda je u mougćnosti poslati informaciju o kliku mišem na računalo

        Arguments:
            click_type {integer} -- integer which represents if it is an left or right click
        """

        click_type = str(click_type)

        click = bytes(click_type, "UTF-8")
        self.sock.sendto(click, self.address)
