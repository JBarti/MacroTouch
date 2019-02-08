import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex

from kivy.config import Config
from kivy.animation import Animation
from panels.apps import AppsOption
from panels.widgets import WidgetsOption
from panels.devices import DevicesOption
from panels.macros import MacrosOption
from common import Seperator, DisplayText, CToggleButton
from common import CToggleButton
from kivy.core.window import Window


Window.size = (1024, 600)

# Definiranje veličine aplikacije na veličinu touch displaya
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "600")


# Glavni layout u kojem se nalazi ostatak aplikacije
class MainLayout(BoxLayout):
    pass


class MyApp(App):
    """
    Root klasa aplikacija
    """

    def build(self):
        """
        Prilikom pokretanja aplikacije na ekran se dodaje objekt klase MainLayout
        """
        return MainLayout()


class Content(BoxLayout):
    """
    Dio ekrana gdje se izmjenjuju paneli
    """

    # Dictionairy sa objektima svih mogućih panela
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
        """Funkcije koja mijenja sadržaj content klase
        
        Arguments:
            screen {objekt} -- objekt koji treba prikazati unutar contenta
        
        Returns
            return_function {funkcija} -- potrebno je vratiti funkciju koja 
                                          se kivy elementu prosljeđuje kao callback
        """

        def return_function():
            try:
                self.clear_widgets()
                if type(screen) is str:
                    self.add_widget(self.screens[screen])
                else:
                    self.add_widget(screen)
                    self.current_widget = screen
            except Exception as err:
                print(err)
                self.add_widget(Label(text="Error"))

        return return_function


class MainScreen(Screen):
    pass


if __name__ == "__main__":
    MyApp().run()
