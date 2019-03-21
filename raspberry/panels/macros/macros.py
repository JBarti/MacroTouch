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
        self.generate_screen_buttons(edit_mode=False)
        self.ids["edit_button"].on_press = self.change_edit_mode

    def generate_screens(self):
        with open("./data.json", "r") as data:
            data = json.loads(data.read())
            macro_pages = data["macro_pages"]
            self.screens = [MacroPage(page["name"]) for page in macro_pages]

    def generate_screen_buttons(self, edit_mode=False):
        print("ENTENRENRNERNERNE")
        pages = self.ids["pages"]
        pages.clear_widgets()
        page_buttons = [
            SelectPageButton(
                page_screen.page_name, self.switch_screen(), text=page_screen.page_name
            )
            for page_screen in self.screens
        ]
        if edit_mode:
            edit_button = SelectPageButton("", self.add_page_popup, text="<ADD_NEW>")
            page_buttons.append(edit_button)
        [pages.add_widget(page_button) for page_button in page_buttons]

    def add_page_popup(self, *args):
        AddPage(self.add_page).open()

    def add_page(self, page_name):
        with open("./data.json", "r") as data:
            json_data = json.loads(data.read())
            page = {"macros": [], "name": page_name}
            json_data["macro_pages"].append(page)

        with open("./data.json", "w") as data:
            json.dump(json_data, data, indent=4)

        self.generate_screens()
        self.generate_screen_buttons(edit_mode=True)
        self.change_edit_mode()

    def switch_screen(self):
        def inner(page_name):
            screen = next(
                (
                    macro_screen
                    for macro_screen in self.screens
                    if macro_screen.page_name == page_name
                ),
                False,
            )
            try:
                self.screen_manager.switch_to(screen, direction="down")
            except:
                pass

        return inner

    def change_edit_mode(self):
        def map_callback(screen):
            screen.edit_mode = not screen.edit_mode
            return screen

        try:
            edit_mode = self.screens[0].edit_mode
            print("EDIIIT MOOOOD")
            print(edit_mode)
        except:
            edit_mode = False
        self.generate_screen_buttons(edit_mode=not edit_mode)
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
                    grid.add_widget(
                        SendMacroButton(
                            text=macro["text"],
                            macro=macro["macro"],
                            editable=self.edit_mode,
                            x_pos=rows,
                            y_pos=cols,
                            page_name=self.page_name,
                            reload_page=self.generate_macro_buttons,
                        )
                    )
                elif self.edit_mode:
                    grid.add_widget(
                        CreateMacroButton(
                            self.generate_macro_buttons, cols, rows, self.page_name
                        )
                    )
                elif not self.edit_mode:
                    grid.add_widget(Placeholder())


class AddPage(Popup):
    def __init__(self, submit_page, **kwargs):
        super(AddPage, self).__init__(**kwargs)
        self.ids["cancel"].on_press = self.dismiss
        self.ids["submit"].on_press = self.add_page
        self.submit_page = submit_page
        self.keyboard = self.ids["vkeyboard"]
        self.keyboard.on_key_down = self.key_press

    def add_page(self):
        name = self.ids["name_input"].text
        self.submit_page(name)
        self.dismiss()

    def key_press(self, key, value, *args, **kwargs):
        """
        Kada se pritisne botun na on-screen tipkovnici 
        znak na tipki se dodaje u trenutno fokusiran TextInput
        
        Arguments:
            key {string} -- pritisnuti function key
            value {string} -- pritisnuti znak
        """
        self.focused = self.ids["name_input"]
        if value:
            self.focused.text += value
            self.focused.text = self.focused.text[:10]
            return
        if key == "backspace" and len(self.focused.text):
            text = list(self.focused.text)
            text.pop()
            self.focused.text = "".join(text)


class RemoveMacro(Popup):
    def __init__(self, delete_macro, **kwargs):
        super(RemoveMacro, self).__init__(**kwargs)
        self.ids["delete"].on_press = delete_macro
        self.ids["delete"].on_release = self.dismiss
        self.ids["cancel"].on_release = self.dismiss


class SendMacroButton(MacroButton):
    def __init__(self, macro, editable, x_pos, y_pos, page_name, reload_page, **kwargs):
        super(SendMacroButton, self).__init__(**kwargs)
        self.macro_controller = App.get_running_app().connector.macro_controller
        self.macro = macro
        self.bind(on_press=self.send_macro if not editable else self.call_delete_popup)
        self.location = [y_pos, x_pos]
        self.page_name = page_name
        self.reload_page = reload_page

    def send_macro(self, *args, **kwargs):
        self.macro_controller.send_data(self.macro)

    def call_delete_popup(self, *args, **kwargs):
        RemoveMacro(delete_macro=self.delete_macro).open()

    def delete_macro(self, *args, **kwargs):
        with open("./data.json", "r") as data:
            json_data = json.loads(data.read())
            pages = json_data["macro_pages"]
            page = next((page for page in pages if page["name"] == self.page_name))
            macro = next(
                (
                    macro
                    for macro in page["macros"]
                    if macro["position"][0] == self.location[0]
                    and macro["position"][1] == self.location[1]
                )
            )
            page["macros"].remove(macro)
        with open("./data.json", "w") as data:
            json.dump(json_data, data, indent=4)

        self.reload_page()


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
        self.location = [x_pos, y_pos]
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

    def key_press(self, key, value, *args, **kwargs):
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


class FabButton(ToggleButton):
    """
    Botun u donjem lijevom kutu koji prebacuje korisnika
    u edit mode za dodavanje novih macroa
    """

    def __init__(self, **kwargs):
        super(FabButton, self).__init__(**kwargs)
        self.bind(state=self.on_state)

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
        print("STEEEEEEEEEEEEEEEEEEJT")
        print(state)
        if state == "down":
            print("IZBORNIK")
            self.background_col = "#7f58c5"
            self.on_down()
        if state == "normal":
            print("DENA")
            self.background_col = "#151515"
            self.on_normal()
