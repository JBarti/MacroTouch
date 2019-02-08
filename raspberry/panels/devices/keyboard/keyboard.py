import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button

Builder.load_file(os.path.join(os.path.dirname(__file__), "keyboard.kv"))

# popis svih potrebnih tipki
keys = [list("1234567890"), list("qwertyuiop"), list("asdfghjkl"), list("zxcvbnm")]


class Key(Button):
    pass


class KeyRow(BoxLayout):
    margin_left = 20


class Spacebar(Key):
    pass


class Keyboard(BoxLayout):
    """
    Glavni layout tipkovnice
    """

    orientation = "vertical"
    key_buttons = []
    caps_lock = False

    def __init__(self, **kwargs):
        """
        Algoritam koji izrađuje mrežu botuna
        """

        super(Keyboard, self).__init__(**kwargs)
        for row in keys:
            padding_left = KeyRow.margin_left + ((10 - len(row)) * 25)
            stack = KeyRow(padding=[padding_left, 0, 0, 0])
            list(map(stack.add_widget, map(self.create_keyboard_key, row)))
            self.add_widget(stack)

        controls_row = KeyRow(padding=[KeyRow.margin_left, 0, 0, 0])
        caps_lock_key = Key()
        spacebar_key = Spacebar()
        controls_row.add_widget(caps_lock_key)
        controls_row.add_widget(spacebar_key)
        self.add_widget(controls_row)

        caps_lock_key.on_press = self.caps_lock_press

    def caps_lock_press(self):
        """
        Povećava sva slova pritiskom na tipku caps lock
        """

        if self.caps_lock:
            self.keyboard_lowercase()
            self.caps_lock = not self.caps_lock
        else:
            self.keyboard_upercase()
            self.caps_lock = not self.caps_lock

    def create_keyboard_key(self, letter):
        """Generira botun widget za tipkovnicu
        
        Arguments:
            letter {str} -- [slovo koje piše na tipki]
        
        Returns:
            [object] -- [widget za tipku]
        """

        key = Key(text=letter)
        self.key_buttons.append(key)
        return key

    def keyboard_upercase(self):
        """
        Sve tipke postavlja na uppercase
        """

        for button in self.key_buttons:
            button.text = button.text.upper()

    def keyboard_lowercase(self):
        """
        Sve tipke postavlja na lowercase
        """

        for button in self.key_buttons:
            button.text = button.text.lower()
