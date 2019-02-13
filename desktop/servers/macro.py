import socket
import threading
import json
from pykeyboard import PyKeyboard

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
    "SUPER": k.super_l_key
}


class MacroServer(threading.Thread):
    """

    Klasa koja nasljeđuje od Thread klase, zadužna za izvršavanje makro naredbi

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
        self.request_type = {
            "RUN_MACRO": self.handle_macro,
            "TYPE_TEXT": self.type_text
        }

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

    def type_text(self, data):
        for letter in data:
            k.tap_key(letter)

    def handle_macro(self, data):
        """

        Metoda koja rješava pritisak slijeda od više makro naredbi

        Argumenti:
            data {list} -- [str, str, str ,str, ...]

        """

        for str_macro in data:
            macro = self.parse_macro(str_macro)
            k.press_keys(macro)

    def parse_macro(self, payload):
        """

        Metoda koja se bavi parsiranjem macroa u nešto kasnije primjenjivo

        Argumenti:
            payload {str} -- jedna makro naredba

        Return:
            [list] -- parsed macro into a list of keys

        """

        macro = payload.strip().split("+")

        try:
            for i in range(len(macro)):
                if len(macro[i]) != 1:
                    macro[i] = SPECIAL_KEYS_DICT[macro[i]]
        except:
            return []

        return macro
