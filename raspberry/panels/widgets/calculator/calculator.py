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
    """
    Definira grid layout u kojem se nalaze tipke kalkulatora
    """

    keys = [
        ["7", "8", "9", "/"],
        ["6", "5", "4", "*"],
        ["3", "2", "1", "-"],
        ["0", "(", ")", "+"],
        ["C", "Del", "Ans", "="],
    ]

    def __init__(self, **kwargs):
        super(Buttons, self).__init__(**kwargs)
        self.display = None
        self.last = ""
        for row in range(len(self.keys)):
            for col in range(len(self.keys[row])):
                key_text = self.keys[row][col]
                press = self.press_key(key_text)
                key = MacroButton(text=key_text, txt_size=30, on_press=press)
                self.add_widget(key)

    def press_key(self, text):
        """
        Vraća funkciju koja dodaje string na display kalkulatora
        
        Arguments:
            text {string} -- text tipke
        
        Returns:
            [function] -- funkcija koja se dodjeljuje botunu kalkulatora
        """

        def text_key(*args, **kwargs):
            self.display.text += text

        def clear(*args, **kwargs):
            self.display.text = ""

        def delete(*args, **kwargs):
            text = self.display.text
            self.display.text = text[: len(text) - 1 :]

        def solve(*args, **kwargs):
            solution = str(eval(self.display.text))
            self.display.text = solution
            self.last = solution

        def history(*args, **kwargs):
            self.display.text += self.last

        if text == "C":
            return clear
        elif text == "=":
            return solve
        elif text == "Del":
            return delete
        elif text == "Ans":
            return history

        return text_key

