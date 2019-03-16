import os
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import socket

Builder.load_file(os.path.join(os.path.dirname(__file__), "mouse.kv"))


class Mouse(BoxLayout):
    """
    Box layout u kojem se prikazuju
    komponente miša
    """

    orientation = "vertical"

    def __init__(self, mouse_controller, **kwargs):
        """
        Definira da na svaki pokret miša unutar aplikacije 
        se pozove funkcije mouse_move
        """

        super(Mouse, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_move)
        self.mouse_controller = mouse_controller

    def on_touch_move(self, touch):
        x_pos = touch.pos[0]
        y_pos = touch.pos[1]
        print(x_pos, " ", y_pos)
        x_min = 185
        y_min = 41
        x_max = 1018
        y_max = 590

        if x_pos > x_min and x_pos < x_max:
            if y_pos > y_min and y_pos < y_max:
                x_percent = x_pos / x_max
                y_percent = y_pos / y_max
                self.mouse_controller.send_location_data([x_percent, y_percent])

    def mouse_move(self, _, mouse_pos, **kwargs):
        """Provjerava nalazi li korsnikov prst unutar 
        dimenzija miša
        
        Arguments:
            mouse_pos {[tuple]} -- [tuple sa x i y pozicijama korisnikova prsta]
        """

        click_size = self.ids.left_click.height
        if self.parent and self.parent.current_widget is self:
            if mouse_pos[0] > self.pos[0] and mouse_pos[1] > click_size:
                print(mouse_pos)
