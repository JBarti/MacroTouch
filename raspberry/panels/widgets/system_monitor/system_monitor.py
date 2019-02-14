import os
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file(os.path.join(os.path.dirname(__file__), "system_monitor.kv"))


class SystemMonitor(BoxLayout):
    pass
