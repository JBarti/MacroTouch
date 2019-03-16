from kivy.lang import Builder
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.app import App
from .keyboard import Keyboard
from .mouse import Mouse
from common import MacroButton

Builder.load_file(os.path.join(os.path.dirname(__file__), "devices.kv"))


class DevicesOption(GridLayout):
    """
    Definira grid layout unutar kojeg su 
    posloženi svi mogući uređaji.
    """

    def __init__(self, switch, **kwargs):
        super(DevicesOption, self).__init__(**kwargs)
        connector = App.get_running_app().connector
        self.mouse_controller = connector.mouse_controller
        self.macro_controller = connector.macro_controller
        self.switch = switch

        keyboard = Keyboard(self.macro_controller)
        mouse = Mouse(self.mouse_controller)

        self.generate_button(keyboard, "./icons/keyboard.png")
        self.generate_button(mouse, "./icons/mouse.png")

    def generate_button(self, panel, img_source):
        btn = MacroButton(
            on_press=self.switch_to_device(panel),
            size_hint=[None, None],
            size=[100, 100],
        )
        btn.ids["container"].add_widget(
            ButtonImage(source=img_source, pos_hint={"center_x": 0.5, "center_y": 0.5})
        )
        self.ids["devices"].add_widget(btn)

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
