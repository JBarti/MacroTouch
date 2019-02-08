import socket
import threading
import json
from pykeyboard import PyKeyboard


class MacroServer(threading.Thread):
    """

    Klasa koja nasljeđuje od Thread klase
    
    """

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5200):
        """
        
        Inicijalna metoda za klasu MacroServer. Stvara socket te ga veže na adresu, i virtualnu tipkovnicu. 
        
        Argumenti:
            family {enum AdressFamily} -- tip adrese korišten za sockete
            sock_type {enum SocketKind} -- tip socketa koji će se koristiti
        
        Keyword Argumenti:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
            port {int} -- port na koji će socket biti vezan (default: {5200})
        
        """

        super(MacroServer, self).__init__()
        self.daemon = True
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((ip_address, port))
        self.keyboard = PyKeyboard()
        self.request_type = {
            "RUN_MACRO": self.handle_macro,
            "TAP_KEY": self.keyboard.tap_key,
        }

    def run(self):
        """
        
        Metoda run pokreće se pri pokretanju Threada. Prima zahtjeve socketa
        i ovisno o zahtjevu poziva metodu da obradi dobiveni podatak.
        
        """

        while True:
            data = self.sock.recv(1024)
            if data != "":
                json_data = json.loads(data.decode("ASCII"))

                request_type = json_data["type"]
                request_data = json_data["payload"]

                self.request_type[request_type](request_data)

    def handle_macro(self, data):
        """
        
        Metoda koja rješava pritisak slijeda od više makro naredbi
        
        Argumenti:
            data {str} -- podatci u obliku stringa koji se u ovoj funkciji obrade
            i iskoriste putem PyKeyboarda()
        
        """

        json_macro = json.loads(data)
        for macro in json_macro:
            self.keyboard.press_keys(macro)
