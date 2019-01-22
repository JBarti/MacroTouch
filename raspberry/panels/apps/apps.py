from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
import os

from subprocess import Popen, PIPE

Builder.load_file(os.path.join(os.path.dirname(__file__), "apps.kv"))


class AppsOption(GridLayout):
    pass


class CurrentApp(BoxLayout):
    supported = BooleanProperty()

    def get_color(self):
        if self.supported:
            return "#2ecc71"
        return "#e74c3c"

    def get_current_app(self):
        output, error = Popen(
            "xdotool getactivewindow getwindowname".split(), stdout=PIPE
        ).communicate()
        print(output)
