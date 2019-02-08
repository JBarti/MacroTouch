from kivy.lang import Builder
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from .keyboard import Keyboard
from .mouse import Mouse

Builder.load_file(os.path.join(os.path.dirname(__file__), "devices.kv"))


class DevicesOption(GridLayout):
    """
    Definira grid layout unutar kojeg su 
    posloženi svi mogući uređaji.
    """

    keyboard = Keyboard()
    mouse = Mouse()

    def __init__(self, **kwargs):
        super(DevicesOption, self).__init__(**kwargs)

    def on_parent(self, _, parent):
        """Funkcija se izvodi prilikom dodavanja
        objekta u content klasu. Content klasa se 
        veže na root svojstvo objekta kako bi mogao
        pristupit switch funkciji
        
        Arguments:
            parent {object} -- [content klasa]
        """

        self.root = parent
