from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from KivyCalendarDev import CalendarWidget
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "calendar.kv"))


class Calendar(BoxLayout):
    """
    Dodaje CalendarWidget na trenutni display
    CalendarWidget je https://github.com/kiok46/Kivy-Calender library
    prepisan za python3
    """

    def __init__(self, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        self.add_widget(CalendarWidget())

