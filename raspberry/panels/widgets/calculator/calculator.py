from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from common import MacroButton
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "calculator.kv"))


class Calculator(BoxLayout):
    pass


class Buttons(GridLayout):
    keys = [
        ["7", "8", "9", "/"],
        ["6", "5", "4", "X"],
        ["3", "2", "1", "-"],
        ["C", "0", "DEL", "+"],
    ]

    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)
        for row in range(4):
            for col in range(4):
                key = MacroButton(text=self.keys[row][col], txt_size=30)
                self.add_widget(key)
