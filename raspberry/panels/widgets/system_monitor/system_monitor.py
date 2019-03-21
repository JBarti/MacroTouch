import os
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from pprint import PrettyPrinter
import random
import socket
import math
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), "system_monitor.kv"))

pp = PrettyPrinter()


class SystemMonitor(BoxLayout):
    """
    Definira BoxLayout u kojem se nalaze elementi system monitora

    """

    def __init__(self, **kwargs):
        super(SystemMonitor, self).__init__(**kwargs)
        self.monitor_controller = App.get_running_app().connector.monitor_controller
        self.max_usage_blocks = 25
        self.data_length = 0
        self.cpus = []
        self.use_system_data()
        Clock.schedule_interval(self.use_system_data, 5)

    def use_system_data(self, *args, **kwargs):
        """
        Dohvaća podatke sa korisnikova računala
        i mjenja trenutno stanje prikazanog system monitora
        """
        self.monitor_controller.get_system_data()
        data = self.monitor_controller.data
        try:
            data = json.loads(data)
        except TypeError:
            print("iz fine")

        print("SET_DATA")
        if len(data["cpus"]) != self.data_length:
            self.cpus = self.init_cpus(data["cpus"])
            self.data_length = len(data["cpus"])

        self.refresh_cpus(data["cpus"])
        self.refresh_temp(data["temp"])
        self.refresh_ram(**data["memory"])

    def get_usage_blocks_num(self, cpu):
        num_blocks = (cpu / 800) * self.max_usage_blocks
        print(cpu)
        print("BLOKOVIII")
        print(num_blocks)
        return int(math.trunc(num_blocks))

    def init_cpus(self, cpu_data):
        cpus_widg = self.ids["cpus"]
        cpus = [CPUUsage(id=index, text=index) for index, _ in enumerate(cpu_data)]
        [cpus_widg.add_widget(cpu) for cpu in cpus]
        return cpus

    def refresh_cpus(self, cpu_data):
        def map_cpus(cpu):
            print("JESI SE POJRENIA")
            print(cpu)
            index, cpu_percent = cpu
            self.cpus[index].set_percentage(self.get_usage_blocks_num(cpu_percent))

        list(map(map_cpus, enumerate(cpu_data)))

    def refresh_temp(self, temp):
        temp_label = self.ids["temp"]
        temp_label.text = "[color=7f58c5]Temp: [/color]{}°C".format(temp)

    def refresh_ram(self, total=0, used=0):
        ram_label = self.ids["ram"]
        ram_label.text = "[color=7f58c5]Ram: [/color]{}/{} GB".format(total, used)


class UsageBlock(Widget):
    pass


class CPUUsage(StackLayout):
    def __init__(self, id, text, **kwargs):
        super(CPUUsage, self).__init__(**kwargs)
        self.text = "1"
        self.id = str(id)

    def set_percentage(self, num_blocks):
        self.clear_widgets()
        [self.add_widget(UsageBlock()) for i in range(num_blocks)]

