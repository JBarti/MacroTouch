from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from common import MacroButton
from .system_monitor import SystemMonitor
from .calendar import Calendar
from .calculator import Calculator
from kivy.lang import Builder
from kivy.app import App
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "widgets.kv"))


class ButtonImage(Image):
    pass


class WidgetsOption(BoxLayout):
    def __init__(self, switch, **kwargs):
        super(WidgetsOption, self).__init__(**kwargs)
        self.switch = switch
        connector = App.get_running_app().connector
        self.monitor_controller = connector.monitor_controller
        self.generate_button(SystemMonitor(), "./icons/word.png")
        self.generate_button(Calendar(), "./icons/calendar.png")
        self.generate_button(Calculator(), "./icons/calculator.png")

    def switch_to_device(self, device):
        def inner(*args, **kwargs):
            self.switch(device)()

        return inner

    def generate_button(self, page, img_source):
        """
        Generira botun za prabacivanje na određeni widget panel
        
        Arguments:
            page {object} -- widget panel
            img_source {string} -- ikona botuna
        """
        button = MacroButton(
            on_press=self.switch_to_device(page),
            size_hint=[None, None],
            size=[100, 100],
        )
        button.ids["container"].add_widget(
            ButtonImage(source=img_source, pos_hint={"center_x": 0.5, "center_y": 0.5})
        )

        self.ids["widgets"].add_widget(button)
