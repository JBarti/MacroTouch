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
