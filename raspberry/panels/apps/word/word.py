import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App
from common import MacroButton
import socket
from pprint import PrettyPrinter

pp = PrettyPrinter()

Builder.load_file(os.path.join(os.path.dirname(__file__), "word.kv"))

buttons = [
    {"icon": "bold-text.png", "macro": "<CTRL+b>"},
    {"icon": "italicize-text.png", "macro": "<CTRL+i>"},
    {"icon": "underline-text.png", "macro": "<CTRL+u>"},
    {"icon": "undo-arrow.png", "macro": "<CTRL+z>"},
    {"icon": "font-symbol-of-letter-a.png", "macro": "<ALT+CTRL+:>"},
    {"icon": "font-symbol-of-letter-a.png", "macro": "<ALT+CTRL+;>"},
    {"icon": "left-alignment.png", "macro": "<CTRL+l>"},
    {"icon": "center-alignment.png", "macro": "<CTRL+e>"},
    {"icon": "right-alignment.png", "macro": "<CTRL+r>"},
    {"icon": "justify.png", "macro": "<CTRL+j>"},
]


class Word(GridLayout):
    def __init__(self, **kwargs):
        super(Word, self).__init__(**kwargs)
        [self.create_word_button(button_data) for button_data in buttons]

    def create_word_button(self, button_data):
        button = SendWordButton(**button_data)
        self.add_widget(button)
        return button


class SendWordButton(MacroButton):
    def __init__(self, icon, macro, **kwargs):
        super(SendWordButton, self).__init__(**kwargs)
        self.macro_controller = App.get_running_app().connector.macro_controller
        self.macro = macro
        self.src = "./icons/word/" + icon

    def on_press(self):
        pp.pprint(self.macro)
        self.macro_controller.send_data(self.macro)
