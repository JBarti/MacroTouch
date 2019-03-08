import os
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from controllers import MonitorController
import random
import socket

Builder.load_file(os.path.join(os.path.dirname(__file__), "system_monitor.kv"))


class SystemMonitor(BoxLayout):
    def __init__(self, **kwargs):
        super(SystemMonitor, self).__init__(**kwargs)
        self.use_system_data()
        Clock.schedule_interval(self.use_system_data, 2)

    def use_system_data(self, *args, **kwargs):
        stack1 = self.ids["s1"].ids["stack"]
        stack2 = self.ids["s2"].ids["stack"]
        stack3 = self.ids["s3"].ids["stack"]
        stack4 = self.ids["s4"].ids["stack"]

        start_num = 5
        more1 = random.randint(1, 4)
        more2 = random.randint(1, 4)
        more3 = random.randint(1, 4)
        more4 = random.randint(1, 4)
        stack1.clear_widgets()
        stack2.clear_widgets()
        stack3.clear_widgets()
        stack4.clear_widgets()
        for i in range(start_num + more1):
            stack1.add_widget(UsageBlock())
        for i in range(start_num + more2):
            stack2.add_widget(UsageBlock())
        for i in range(start_num + more3):
            stack3.add_widget(UsageBlock())
        for i in range(start_num + more4):
            stack4.add_widget(UsageBlock())


class UsageBlock(Widget):
    pass
