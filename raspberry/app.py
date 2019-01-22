import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.animation import Animation
from panels.apps import AppsOption
from panels.widgets import WidgetsOption
from panels.devices import DevicesOption
from panels.macros import MacrosOption
from server import Server
from common import *


class BluetoothPending(BoxLayout):
    pass


class MainLayout(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        # Server()
        return MainLayout()


class Content(BoxLayout):
    screens = {
        "apps": AppsOption(),
        "devices": DevicesOption(),
        "widgets": WidgetsOption(),
        "macros": MacrosOption(),
    }

    hide_show_animation = Animation(opacity=0.2, duration=0) + Animation(
        opacity=1, duration=0.1
    )

    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.switch("apps")

    def switch(self, screen):
        try:
            self.clear_widgets()
            if type(screen) is str:
                self.add_widget(self.screens[screen])
            else:
                self.add_widget(screen)
                self.current_widget = screen
            self.hide_show_animation.start(self.children[0])
        except Exception as err:
            print(err)
            self.add_widget(Label(text="Error"))


class MainScreen(Screen):
    pass


if __name__ == "__main__":
    MyApp().run()
