from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "common.kv"))


class CToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super(CToggleButton, self).__init__(**kwargs)
        self.toggled = False

    def down(self):
        pass

    def update(self):
        self.ids["background"].toggled = self.toggled

    def on_state(self, widget, state):
        self.toggled = self.state == "down"
        print(self.toggled)
        if self.state:
            self.down()
            self.update()

    def on_press(self):
        self.toggled = self.toggled == self.toggled


class MacroButton(Button):
    def __init__(self, **kwargs):
        super(MacroButton, self).__init__(**kwargs)
        self.update(False)

    def click(self):
        pass

    def update(self, pressed):
        self.ids["background"].pressed = pressed

    def on_press(self):
        self.update(True)
        self.click()

    def on_release(self):
        self.update(False)


class Seperator(Widget):
    pass


class DisplayText(Label):
    pass
