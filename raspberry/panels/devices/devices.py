from kivy.lang import Builder
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from .keyboard import Keyboard
from .mouse import Mouse

Builder.load_file(os.path.join(os.path.dirname(__file__), "devices.kv"))


class DevicesOption(GridLayout):
    keyboard = Keyboard()
    mouse = Mouse()

    def __init__(self, **kwargs):
        super(DevicesOption, self).__init__(**kwargs)

    def on_parent(self, screen, parent):
        self.root = parent
