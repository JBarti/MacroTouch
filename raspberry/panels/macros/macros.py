from kivy.lang import Builder
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from common import MacroButton, DisplayText
import json
import pprint

Builder.load_file(os.path.join(os.path.dirname(__file__), "macros.kv"))

pp = pprint.PrettyPrinter()


class MacrosOption(BoxLayout):
    def __init__(self, **kwargs):
        super(MacrosOption, self).__init__(**kwargs)
        self.screen_manager = self.ids["sm"]
        self.screens = []
        self.generate_screens()
        self.generate_screen_buttons()
        self.ids["edit_button"].on_press = self.change_edit_mode

    def generate_screens(self):
        with open("./data.json", "r") as data:
            data = json.loads(data.read())
            macro_pages = data["macro_pages"]
            self.screens = [MacroPage(page["name"]) for page in macro_pages]

    def generate_screen_buttons(self):
        pages = self.ids["pages"]
        pages.clear_widgets()
        page_buttons = [
            SelectPageButton(
                page_screen.page_name, self.switch_screen(), text=page_screen.page_name
            )
            for page_screen in self.screens
        ]
        [pages.add_widget(page_button) for page_button in page_buttons]

    def switch_screen(self):
        def inner(page_name):
            pp.pprint(page_name)
            screen = next(
                (
                    macro_screen
                    for macro_screen in self.screens
                    if macro_screen.page_name == page_name
                ),
                False,
            )
            self.screen_manager.switch_to(screen, direction="down")

        return inner

    def change_edit_mode(self):
        def map_callback(screen):
            screen.edit_mode = not screen.edit_mode
            return screen

        [map_callback(screen) for screen in self.screens]


class MacroPage(Screen):
    def __init__(self, page_name, **kwargs):
        super(MacroPage, self).__init__(**kwargs)
        self.page_name = page_name
        self.generate_macro_buttons()
        self.edit_mode = False
        self.bind(edit_mode=self.edit_mode_changed)

    def edit_mode_changed(self, *args, **kwargs):
        self.generate_macro_buttons()

    def get_page_macros(self):
        with open("./data.json", "r") as data:
            data = json.loads(data.read())
            macro_page = [
                macro_page
                for macro_page in data["macro_pages"]
                if macro_page["name"] == self.page_name
            ].pop()
            return macro_page["macros"]

    def generate_macro_buttons(self):
        macros = self.get_page_macros()
        grid = self.ids["grid"]
        grid.clear_widgets()
        for cols in range(5):
            for rows in range(6):
                macro = next(
                    (
                        macro
                        for macro in macros
                        if macro["position"][0] == cols and macro["position"][1] == rows
                    ),
                    False,
                )
                if macro:
                    pp.pprint(macro)
                    grid.add_widget(
                        SendMacroButton(text=macro["text"], macro=macro["macro"])
                    )
                elif self.edit_mode:
                    grid.add_widget(
                        CreateMacroButton(
                            self.generate_macro_buttons, rows, cols, self.page_name
                        )
                    )
                elif not self.edit_mode:
                    grid.add_widget(Placeholder())


class SendMacroButton(MacroButton):
    def __init__(self, macro, **kwargs):
        super(SendMacroButton, self).__init__(**kwargs)
        self.macro_controller = App.get_running_app().connector.macro_controller
        self.macro = macro

    def on_press(self):
        self.macro_controller.send_data(self.macro)


class SelectPageButton(MacroButton):
    def __init__(self, page_name, switch_screen, **kwargs):
        super(SelectPageButton, self).__init__(**kwargs)
        self.page_name = page_name
        self.switch_screen = switch_screen

    def on_press(self):
        self.switch_screen(self.page_name)


class Placeholder(Widget):
    pass


class CreateMacroButton(Button):
    def __init__(self, on_submit, x_pos, y_pos, page_name, **kwargs):
        super(CreateMacroButton, self).__init__(**kwargs)
        self.text = "<NEW>"
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.on_submit = on_submit
        self.page_name = page_name

    def on_press(self):
        CreateWidget(self.on_submit, self.x_pos, self.y_pos, self.page_name).open()


class CreateWidget(Popup):
    """
    Popup za stvaranje novog MacroButtona
    
    Arguments:
        submit {[function]} -- funkcija za submitanje macroa
        y_pos {[int]} -- y pozicija macro botuna
        x_pos {[int]} -- x pozicija macro botuna
    """

    def __init__(self, submit, x_pos, y_pos, page_name, **kwargs):
        super(CreateWidget, self).__init__(**kwargs)
        self.ids["submit"].on_press = self.press_submit
        self.ids["cancel"].on_press = self.dismiss
        self.location = [y_pos, x_pos]
        self.submit = submit
        name_input = self.name_input = self.ids["name_input"]
        macro_input = self.ids["macro_input"]
        self.focused = name_input
        name_input.focus = True
        name_input.bind(focus=self.on_focus)
        macro_input.bind(focus=self.on_focus)
        self.keyboard = self.ids["vkeyboard"]
        self.keyboard.on_key_down = self.key_press
        self.page_name = page_name

    def press_submit(self):
        """
        Submita unesene podatke o macrou i gasi popup
        """
        name = self.ids["name_input"].text
        macro = self.ids["macro_input"].text

        macro = {"macro": macro, "text": name, "position": self.location}

        with open("./data.json", "r") as data:
            json_data = json.loads(data.read())
            page = next(
                (
                    page
                    for page in json_data["macro_pages"]
                    if page["name"] == self.page_name
                )
            )
            page["macros"].append(macro)

        with open("./data.json", "w") as data:
            json.dump(json_data, data, indent=4)

        self.submit()
        self.dismiss()

    def key_press(self, key, value):
        """
        Kada se pritisne botun na on-screen tipkovnici 
        znak na tipki se dodaje u trenutno fokusiran TextInput
        
        Arguments:
            key {string} -- pritisnuti function key
            value {string} -- pritisnuti znak
        """
        if value:
            self.focused.text += value
            if self.focused == self.name_input:
                self.focused.text = self.focused.text[:10]
            return
        if key == "backspace" and len(self.focused.text):
            text = list(self.focused.text)
            text.pop()
            self.focused.text = "".join(text)

    def on_focus(self, text_input, value):
        """
        Zapisuje koji je TextInput trenutno fokusiran
        
        Arguments:
            text_input {object} -- TextInput objekt
            value {bool} -- je li TextInput fokusiran il ne
        """
        if value:
            self.focused = text_input


class EditButton(ToggleButton):
    """
    Botun u donjem lijevom kutu koji prebacuje korisnika
    u edit mode za dodavanje novih macroa
    """

    def __init__(self, **kwargs):
        super(EditButton, self).__init__(**kwargs)
        self.img_source = "./icons/edit.png"

    def on_down(self):
        pass

    def on_normal(self):
        pass

    def on_state(self, _, state):
        """
        Mijenja boju edit ikonice ovisno o tome je li
        korisnik u edit modeu ili ne
        
        Arguments:
            state {string} -- "normal" ako je botun aktiviran, "down" ako nije
        """
        if state == "down":
            self.ids["image"].source = "./icons/edit-clicked.png"
            self.on_down()
        if state == "normal":
            self.ids["image"].source = "./icons/edit.png"
            self.on_normal()
