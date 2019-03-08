from kivy.lang import Builder
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from .keyboard import Keyboard
from .mouse import Mouse
from common import MacroButton

Builder.load_file(os.path.join(os.path.dirname(__file__), "devices.kv"))


class DevicesOption(GridLayout):
    """
    Definira grid layout unutar kojeg su 
    posloženi svi mogući uređaji.
    """

    def __init__(self, switch, mouse_controller, macro_controller, **kwargs):
        super(DevicesOption, self).__init__(**kwargs)
        self.switch = switch
        self.keyboard = Keyboard(macro_controller)
        self.mouse = Mouse(mouse_controller)
        mouse_panel = MacroButton(
            on_press=self.switch_to_device(self.mouse),
            size_hint=[None, None],
            size=[100, 100],
        )
        mouse_panel.ids["container"].add_widget(
            ButtonImage(
                source="./icons/mouse.png", pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
        )
        self.ids["devices"].add_widget(mouse_panel)

        keyboard_panel = MacroButton(
            on_press=self.switch_to_device(self.keyboard),
            size_hint=[None, None],
            size=[100, 100],
        )
        keyboard_panel.ids["container"].add_widget(
            ButtonImage(
                source="./icons/keyboard.png",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
        )
        self.ids["devices"].add_widget(keyboard_panel)

    def switch_to_device(self, device):
        def inner(*args, **kwargs):
            self.switch(device)()

        return inner

    def on_parent(self, _, parent):
        """Funkcija se izvodi prilikom dodavanja
        objekta u content klasu. Content klasa se 
        veže na root svojstvo objekta kako bi mogao
        pristupit switch funkciji
        
        Arguments:
            parent {object} -- [content klasa]
        """

        self.root = parent


class ButtonImage(Image):
    pass
