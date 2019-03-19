from kivy.uix.button import Button
from controllers.macro_controller import MacroController


class MakroBotun(Button):
    def on_press(self):
        controller = MacroController()
        controller.send_data("<ALT+TAB>")
