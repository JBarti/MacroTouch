from kivy.lang import Builder
import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from common import MacroButton
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), "macros.kv"))


class MacrosOption(BoxLayout):
    pass


class Macro(BoxLayout):
    """
    Widget koji predstavlja jedan element
    u mreži macroa
    """

    def __init__(self, button=False, **kwargs):
        """Priliko stvaranja elementa provjerava 
        treba li sadržavati botun ili biti prazno polje
        
        Keyword Arguments:
            button {bool} -- [određuje je li macro ima botun ili ne] (default: {False})
        """

        super(Macro, self).__init__(**kwargs)
        if button:
            self.add_widget(MacroButton(size_hint=[None, None]))


class ButtonGrid(GridLayout):
    """
    Mreža koja sadržava sve botuna
    """

    def __init__(self, **kwargs):
        """Predefinira broj redova i stupaca mreže
        i generira mrežu
        """

        super(ButtonGrid, self).__init__(**kwargs)
        self.cols = 12
        self.rows = 12
        self.add_macro_page()

    def add_macro_page(self):
        """
        Dohvaća podatke iz data.json filea
        izdvaja sve macroe i generira njihov
        prikaz
        """

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
