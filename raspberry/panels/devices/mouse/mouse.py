import os
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Builder.load_file(os.path.join(os.path.dirname(__file__), "mouse.kv"))


class Mouse(BoxLayout):
    """
    Box layout u kojem se prikazuju
    komponente miša
    """

    orientation = "vertical"

    def __init__(self, **kwargs):
        """
        Definira da na svaki pokret miša unutar aplikacije 
        se pozove funkcije mouse_move
        """

        super(Mouse, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_move)

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
