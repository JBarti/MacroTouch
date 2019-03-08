import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from common import MacroButton
from controllers import MacroController
import socket

Builder.load_file(os.path.join(os.path.dirname(__file__), "word.kv"))

# popis svih potrebnih tipki
keys = [list("1234567890"), list("qwertyuiop"), list("asdfghjkl"), list("zxcvbnm")]


class Word(BoxLayout):
    pass
