from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from common import MacroButton
from .word import Word
import os

from subprocess import Popen, PIPE

Builder.load_file(os.path.join(os.path.dirname(__file__), "apps.kv"))


class AppsOption(GridLayout):
    def __init__(self, switch, **kwargs):
        super(AppsOption, self).__init__(**kwargs)
        self.macro_controller = App.get_running_app().connector.macro_controller
        self.switch = switch
        self.layout = SupportedApp()
        self.generate_button(Word(), "./icons/word.png")
        self.ids["grid"].add_widget(self.layout)

    def generate_button(self, page, img_source):
        btn = MacroButton(
            on_press=self.switch_to_device(page),
            size_hint=[None, None],
            size=[100, 100],
        )

        btn.ids["container"].add_widget(
            ButtonImage(source=img_source, pos_hint={"center_x": 0.5, "center_y": 0.5})
        )

        self.layout.add_widget(btn)

    def switch_to_device(self, device, *args, **kwargs):
        def inner(*args, **kwargs):
            print("Test")
            self.switch(device)()

        return inner


class ButtonImage(Image):
    pass


class SupportedApp(BoxLayout):
    pass


class CurrentApp(BoxLayout):
    """
    Prikazuje aplikaciju
    koja se trenutno pokreće na računalu
    """

    supported = BooleanProperty()

    def get_color(self):
        """
        Određuje naljepnice koja stoji uz 
        pokrenutu aplikaciju
        """

        if self.supported:
            return "#2ecc71"
        return "#e74c3c"

    def get_active_window(self):
        """
        Dohvaća ekran koji se trenutno pokreće
        na računalu
        """

        output, error = Popen(
            "node ./panels/apps/getWindowTitle.js".split(), stdout=PIPE
        ).communicate()
        title = output.decode("ASCII")
        title = title[1:-2] if title[-1:] == "\n" else title[1:-1]
        print(title)
