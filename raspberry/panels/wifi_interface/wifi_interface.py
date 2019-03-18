from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.app import App
from common import MacroButton, MacroButtonBackground
from kivy.utils import get_color_from_hex as hex_to_color
from math import ceil
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "wifi_interface.kv"))


class WifiInterfaceOption(AnchorLayout):
    def __init__(self, **kwargs):
        super(WifiInterfaceOption, self).__init__(**kwargs)
        self.connector = App.get_running_app().connector
        self.refresh_wifi()
        self.connector.scan_hosts()
        Clock.schedule_interval(self.check_for_hosts(), 5)

    def refresh_wifi(self):
        """
        Refresha prikazane wifieve
        
        Returns:
            [list] -- wifi botuni
        """
        wifis = self.connector.scan_wifis()
        wifis.sort(key=lambda wifi: int(wifi["signal"]))
        list(map(self.map_wifis(), wifis))
        return wifis

    def map_wifis(self):
        """
        Vraća funkciju za mapiranje dictionarya
        sa podatcima wifia u WifiButton i njihovo
        dodavanje na ekran
        
        Returns:
            [function] -- funkcija za mapiranje
        """

        def inner(wifi):
            name = wifi["name"]
            power = ceil(3 * (int(wifi["signal"]) / 100))
            btn = WifiButton(text=name, power=power)
            self.ids["wifis"].add_widget(btn)

        return inner

    def refresh_hosts(self, hosts):
        """
        Refresha prikazane hostove
        
        Returns:
            [list] -- host botuni
        """
        list(map(self.map_hosts(), hosts))

    def map_hosts(self):
        """
        Vraća funkciju za mapiranje dictionarya
        sa podatcima hosta u WifiButton i njihovo
        dodavanje na ekran
        
        Returns:
            [function] -- funkcija za mapiranje
        """

        def inner(host):
            name = host["name"]
            btn = WifiButton(text=name, power=0)
            self.ids["pcs"].add_widget(btn)

        return inner

    def check_for_hosts(self):
        """
        Vrača funkciju koja provjerava postoji li 
        novi host na mreži
        Sprema prethodni broj hostova
        
        Returns:
            [function] -- ako je došlo do promjene u broju spojenih 
                            hostova pokreče funkciju refresh_hosts
        """
        last_length = 0

        def get_hosts(*args, **kwargs):
            hosts = self.connector.host_finder.hosts
            nonlocal last_length
            if len(hosts) != last_length:
                print(hosts)
                self.refresh_hosts(hosts)
                last_length = len(hosts)

        return get_hosts


class ConnectWifi(Popup):
    """
    Popup za spajanje na wifi mrežu
    Prikazuje se klikom na WifiButton
    
    Arguments:
        ssid {string} -- ssid wifia ili ime hosta
    """

    def __init__(self, ssid, *args, **kwargs):
        super(ConnectWifi, self).__init__(**kwargs)
        self.keyboard = self.ids["vkeyboard"]
        self.keyboard.on_key_down = self.key_press
        self.input = self.ids["vkeyboard"]
        self.ids["cancel"].on_press = self.dismiss
        self.ids["submit"].on_release = self.connect_wifi
        self.ssid = ssid
        self.connector = App.get_running_app().connector

    def key_press(self, key, value, _):
        """
        Pokreće se kada korisnik pritisne tipku
        na on-screen tipokovnici, šalje pritisnuti znak
        u zadnje odabran text input
        
        Arguments:
            key {string} -- pritisnuta funkcijska tipka
            value {string} -- pritisnuti znak
        """
        if value:
            self.input.text += value
            return
        if key == "backspace" and len(self.input.text):
            text = list(self.text.text)
            text.pop()
            self.input.text = "".join(text)

    def connect_wifi(self):
        """
        Pokreće se klikom na submit botun
        Korisnika spaja na odabranu wifi mrežu
        """
        password = self.ids["password_input"].text
        try:
            self.connector.connect_to_wifi(self.ssid, password=password)
        except ConnectionError:
            print("FAILED TO CONNECT")
        self.dismiss()


class WifiButton(Button):
    """
    Botun/trakica koja predstavlja vidljive wifi mreže
    ili hostove vidljive na mreži
    
    Arguments:
        power {[type]} -- snaga wifia koja određuje ikonu botuna
                          ako je snaga 0 botun će promijenit funkcionalnosti
                          za spajanje na host
    """

    light_gray = "#1515155"
    gray = "#00000062"

    def __init__(self, power, *args, **kwargs):
        super(WifiButton, self).__init__(**kwargs)
        self.ids["label"].text = str(self.text).ljust(15, " ")
        print(len(self.ids["label"].text))
        self.ssid = self.text
        self.text = ""
        self.power = power
        self.connector = App.get_running_app().connector

    def on_press(self, *args, **kwargs):
        """
        Ako je snaga veća od 0 spaja se na wifi
        ako nije spaja se na host
        """
        self.background_color = hex_to_color(self.gray)
        if self.power > 0:
            ConnectWifi(ssid=self.ssid).open()
        else:
            print(self.ssid)
            self.connector.connect_to_host(self.ssid)

    def on_touch_up(self, *args, **kwargs):
        self.background_color = hex_to_color(self.light_gray)
        if hasattr(self, "press"):
            self.press()
