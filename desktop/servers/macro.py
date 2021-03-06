import socket
import threading
import json
from pykeyboard import PyKeyboard
import re
from time import sleep

k = PyKeyboard()

SPECIAL_KEYS_DICT = {
    "SPACEBAR": k.space,
    "ENTER": k.enter_key,
    "CTRL": k.control_key,
    "ALT": k.alt_key,
    "F1": k.function_keys[1],
    "F2": k.function_keys[2],
    "F3": k.function_keys[3],
    "F4": k.function_keys[4],
    "F5": k.function_keys[5],
    "F6": k.function_keys[6],
    "F7": k.function_keys[7],
    "F8": k.function_keys[8],
    "F9": k.function_keys[9],
    "F10": k.function_keys[10],
    "F11": k.function_keys[11],
    "F12": k.function_keys[12],
    "TAB": k.tab_key,
    "SHIFT": k.shift_key,
    "ESCAPE": k.escape_key,
    "PRTSCR": k.print_screen_key,
    "INSERT": k.insert_key,
    "DELETE": k.delete_key,
    "PAGE_UP": k.page_up_key,
    "PAGE_DOWN": k.page_down_key,
    "HOME": k.home_key,
    "BACKSPACE": k.backspace_key,
    "SUPER": k.super_l_key,
}


class MacroServer(threading.Thread):
    """

    Klasa koja nasljeđuje od Thread klase, zadužna za izvršavanje makro naredbi

    """

    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5200):
        """

        Inicijalna metoda za klasu MacroServer. Stvara socket te ga veže na adresu, i virtualnu tipkovnicu. 

        Arguments:
            family {enum AdressFamily} -- tip adrese korišten za sockete
            sock_type {enum SocketKind} -- tip socketa koji će se koristiti

        Keyword Arguments:
            ip_address {str} -- ip adresa na koju će socket biti vezan (default: {"0.0.0.0"})
            port {int} -- port na koji će socket biti vezan (default: {5200})

        """

        super(MacroServer, self).__init__()
        self.daemon = True
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((ip_address, port))
        self.request_type = {"RUN_MACRO": self._handle_macro}

    def run(self):
        """

        Metoda run pokreće se pri pokretanju Threada. Prima zahtjeve socketa
        i ovisno o zahtjevu poziva metodu da obradi dobiveni podatak.

        """

        while True:
            data, _ = self.sock.recvfrom(1024)
            if data != b"":
                json_data = json.loads(data.decode("ASCII"))

                request_type = json_data["type"]
                request_data = json_data["payload"]

                self.request_type[request_type](request_data)

    def _handle_macro(self, data):
        """

        Metoda koja rješava pritisak slijeda od više makro naredbi

        Arguments:
            data {str} -- list stringova koji predstavljaju makroe

        """
        i = 0
        while i < len(data):
            if data[i] == "<":
                try:
                    res = re.search("<(.+?)>", data[i:])
                    macro = self._parse_macro(res[1])
                    k.press_keys(macro)
                    i = i + len(res[0])
                    sleep(0.5)
                    continue
                except TypeError:
                    break
            k.tap_key(data[i])
            sleep(0.1)
            i += 1

    def _parse_macro(self, payload):
        """

        Metoda koja se bavi parsiranjem macroa u listu stringova koji predstavljaju makro naredbu

        Arguments:
            payload {str} -- jedna makro naredba u obliku stringa

        Returns:
            [list] -- parsiran makro u obliku liste naredbi

        """

        macro = payload.split("+")

        try:
            for i in range(len(macro)):
                if len(macro[i]) != 1:
                    macro[i] = SPECIAL_KEYS_DICT[macro[i]]
        except:
            return []

        return macro
