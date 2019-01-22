from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "widgets.kv"))


class WidgetsOption(BoxLayout):
    pass
