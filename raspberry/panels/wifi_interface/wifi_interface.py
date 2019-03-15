from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from common import MacroButton, MacroButtonBackground
from kivy.utils import get_color_from_hex as hex_to_color
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "wifi_interface.kv"))


class WifiInterfaceOption(AnchorLayout):
    def __init__(self, **kwargs):
        super(WifiInterfaceOption, self).__init__(**kwargs)


class ConnectWifi(Popup):
    def __init__(self, *args, **kwargs):
        super(ConnectWifi, self).__init__(**kwargs)
        self.keyboard = self.ids["vkeyboard"]
        self.keyboard.on_key_down = self.key_press
        self.input = self.ids["vkeyboard"]
        self.ids["cancel"].on_press = self.dismiss

    def key_press(self, key, value, currently_pressed):
        print("DRKICA")
        if value:
            self.input.text += value
            return
        if key == "backspace" and len(self.input.text):
            text = list(self.text.text)
            text.pop()
            self.input.text = "".join(text)


class WifiButton(Button):
    light_gray = "#1515155"
    gray = "#00000062"

    def __init__(self, *args, **kwargs):
        super(WifiButton, self).__init__(**kwargs)
        self.power = 3

    def on_press(self, *args, **kwargs):
        self.background_color = hex_to_color(self.gray)
        if self.power > 0:
            ConnectWifi().open()

    def on_touch_up(self, *args, **kwargs):
        self.background_color = hex_to_color(self.light_gray)
        if hasattr(self, "press"):
            self.press()
