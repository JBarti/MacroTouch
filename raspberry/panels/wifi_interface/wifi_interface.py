from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
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

    def refresh_wifi(self):
        wifis = self.connector.scan_wifis()
        wifis.sort(key=lambda wifi: int(wifi["signal"]))
        list(map(self.map_wifis(), wifis))
        return wifis

    def map_wifis(self):
        def inner(wifi):
            name = wifi["name"]
            power = ceil(3 * (int(wifi["signal"]) / 100))
            btn = WifiButton(text=name, power=power)
            self.ids["wifis"].add_widget(btn)

        return inner


class ConnectWifi(Popup):
    def __init__(self, ssid, *args, **kwargs):
        super(ConnectWifi, self).__init__(**kwargs)
        self.keyboard = self.ids["vkeyboard"]
        self.keyboard.on_key_down = self.key_press
        self.input = self.ids["vkeyboard"]
        self.ids["cancel"].on_press = self.dismiss
        self.ids["submit"].on_release = self.connect_wifi
        self.ssid = ssid
        self.connector = App.get_running_app().connector

    def key_press(self, key, value, currently_pressed):
        if value:
            self.input.text += value
            return
        if key == "backspace" and len(self.input.text):
            text = list(self.text.text)
            text.pop()
            self.input.text = "".join(text)

    def on_dismiss(self):
        self.connector.scan_hosts()

    def connect_wifi(self):
        password = self.ids["password_input"].text
        self.connector.connect_to_wifi(self.ssid, password=password)
        self.dismiss()


class WifiButton(Button):
    light_gray = "#1515155"
    gray = "#00000062"

    def __init__(self, power, *args, **kwargs):
        super(WifiButton, self).__init__(**kwargs)
        self.ids["label"].text = str(self.text).ljust(15, " ")
        print(len(self.ids["label"].text))
        self.ssid = self.text
        self.text = ""
        self.power = power

    def on_press(self, *args, **kwargs):
        self.background_color = hex_to_color(self.gray)
        if self.power > 0:
            ConnectWifi(ssid=self.ssid).open()

    def on_touch_up(self, *args, **kwargs):
        self.background_color = hex_to_color(self.light_gray)
        if hasattr(self, "press"):
            self.press()
