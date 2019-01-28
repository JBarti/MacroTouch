from kivy.lang import Builder
import os

from kivy.uix.boxlayout import BoxLayout

Builder.load_file(os.path.join(os.path.dirname(__file__), "macros.kv"))


class MacrosOption(BoxLayout):
    pass
