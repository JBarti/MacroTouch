from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "common.kv"))


class MacroButtonBackground(Widget):
    pass


class CToggleButton(ToggleButton):
    """
    Botuni koji se nalaze u glavnom izborniku
    """

    def __init__(self, **kwargs):
        """
        Postavlja početnu vrijednost elementa na
        ne odabran
        """

        super(CToggleButton, self).__init__(**kwargs)
        self.toggled = False

    def down(self):
        pass

    def update(self):
        """
        Prilikom promjene stanja botuna
        ikona se mijenja
        """

        self.ids["background"].toggled = self.toggled

    def on_state(self, _, state):
        """Poziva update funkciju prilikom
        promjene stanja botuna
        
        Arguments:
            state {[str]} -- ["down" ili "normal" ovisno o tome je li botun stisnut]
        """

        self.toggled = self.state == "down"
        print(self.toggled)
        if self.state:
            self.down()
            self.update()

    def on_press(self):
        """
        Mijenja stanje botuna na klik 
        """

        self.toggled = self.toggled == self.toggled


class MacroButton(Button):
    """
    Botun sa sivom pozadinom i ljujbičastim obrubom
    """

    def __init__(self, **kwargs):
        """
        Postavlja stanje botuna na ne kliknut
        """

        super(MacroButton, self).__init__(**kwargs)
        self.update(False)

    def click(self):
        pass

    def str(self, text):
        return str(text)

    def update(self, pressed):
        """
        Ažurira sliku botuna
        """
        try:
            self.background.pressed = pressed
        except:
            pass

    def on_press(self):
        """
        Klikom na botun pokreće funkcije za ažuriranje
        """

        self.update(True)
        self.click()

    def on_release(self):
        """
        Otpuštanjem botuna vrača se u normalu
        """

        self.update(False)


class Seperator(Widget):
    pass


class DisplayText(Label):
    pass
