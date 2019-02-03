from kivy.lang import Builder
import os

from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

import json

Builder.load_file(os.path.join(os.path.dirname(__file__), "macros.kv"))

Config.set("graphics", "resizable", "0")


class MacrosOption(BoxLayout):
    pass


class Macro(BoxLayout):
    def __init__(self, button=False, **kwargs):
        super(Macro, self).__init__(**kwargs)
        if button:
            self.add_widget(Button(size_hint=[None, None], text="A"))


class ButtonGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonGrid, self).__init__(**kwargs)
        self.cols = 12
        self.rows = 12
        self.add_macro_page()

    def add_macro_page(self):
        with open("./data.json") as data:
            macros = json.load(data)["macro_pages"][0]["macros"]
            macros.sort(key=lambda macro: macro["position"][0])

            for rows in range(self.rows):
                macro_row = list(
                    filter(lambda macro: macro["position"][1] == rows, macros)
                )
                for cols in range(self.cols):
                    visible = len(macro_row) and macro_row[0]["position"][0] == cols
                    self.add_widget(Macro(button=visible))
                    if visible:
                        macro_row.pop(0)

