import os
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.clock import Clock
from pprint import PrettyPrinter
import random
import socket
import math

Builder.load_file(os.path.join(os.path.dirname(__file__), "system_monitor.kv"))

pp = PrettyPrinter()


class SystemMonitor(BoxLayout):
    """
    Definira BoxLayout u kojem se nalaze elementi system monitora

    """

    def __init__(self, **kwargs):
        super(SystemMonitor, self).__init__(**kwargs)
        self.monitor_controller = App.get_running_app().connector.monitor_controller
        pp.pprint(self.monitor_controller)
        self.max_usage_blocks = 37
        self.data_length = 0
        self.cpus = []
        self.use_system_data()
        Clock.schedule_interval(self.use_system_data, 1)

    def use_system_data(self, *args, **kwargs):
        """
        Dohvaća podatke sa korisnikova računala
        i mjenja trenutno stanje prikazanog system monitora
        """
        data = self.monitor_controller.get_system_data()

        print("SET_DATA")
        pp.pprint(data)

        if len(data["cpus"]) != self.data_length:
            self.cpus = self.init_cpus(data["cpus"])

        self.refresh_cpus(data["cpus"])

    def get_usage_blocks_num(self, cpu):
        num_blocks = (cpu / 100) * self.max_usage_blocks
        print("USAGE_BLOCKS")
        print(num_blocks)
        return math.trunc(num_blocks)

    def init_cpus(self, cpu_data):
        print("INIT_CPUS")
        pp.pprint(cpu_data)
        cpus = [CPUUsage(id=index, text=index) for index, _ in enumerate(cpu_data)]
        [self.add_widget(cpu) for cpu in cpus]
        return cpus

    def refresh_cpus(self, cpu_data):
        print("REFRESH_CPUS")
        pp.pprint(cpu_data)

        def map_cpus(cpu):
            index, cpu_widg = cpu
            cpu_widg.set_percentage(cpu[index])

        map(map_cpus, enumerate(cpu_data))


class UsageBlock(Widget):
    pass


class CPUUsage(StackLayout):
    def set_percentage(self, num_blocks):
        self.clear_widgets()
        [self.add_widget(UsageBlock()) for i in num_blocks]

