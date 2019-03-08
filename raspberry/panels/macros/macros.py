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
from kivy.core.window import Window
from common import MacroButton, DisplayText
import json

Builder.load_file(os.path.join(os.path.dirname(__file__), "macros.kv"))


class CreateWidget(Popup):
    def __init__(self, submit, y_pos, x_pos, **kwargs):
        super(CreateWidget, self).__init__(**kwargs)
        self.ids["submit"].on_press = self.press_submit
        self.submit = submit
        self.y_pos = y_pos
        self.x_pos = x_pos
        name_input = self.name_input = self.ids["name_input"]
        macro_input = self.ids["macro_input"]
        self.focused = name_input
        name_input.focus = True
        name_input.bind(focus=self.on_focus)
        macro_input.bind(focus=self.on_focus)
        self.keyboard = self.ids["vkeyboard"]
        self.keyboard.on_key_down = self.key_press

    def press_submit(self):
        name = self.ids["name_input"].text
        macro = self.ids["macro_input"].text
        self.submit(name, macro, self.y_pos, self.x_pos)
        self.dismiss()

    def key_press(self, key, value, currently_pressed):
        if value:
            self.focused.text += value
            if self.focused == self.name_input:
                print("DA")
                self.focused.text = self.focused.text[:10]
            return
        if key == "backspace" and len(self.focused.text):
            text = list(self.focused.text)
            text.pop()
            self.focused.text = "".join(text)

    def on_focus(self, text_input, value):
        if value:
            self.focused = text_input


class MacrosOption(BoxLayout):
    def __init__(self, macro_controller, **kwargs):
        super(MacrosOption, self).__init__(**kwargs)
        self.ids["edit"].on_down = self.edit_down
        self.ids["edit"].on_normal = self.edit_normal
        self.generate_page_buttons()
        self.macro_controller = macro_controller
        self.build_macro_page = self.ids["grid"].build_macro_page
        self.ids["grid"].press_macro = self.send_macro

    def send_macro(self, macro):  # macro --> ["CTRL+A", "DELETE"]
        def inner():
            self.macro_controller.send_data(macro)

        return inner

    def edit_down(self):
        page = App.get_running_app().MACRO_PAGE
        self.build_macro_page(editable=True, page=page)

    def edit_normal(self):
        page = App.get_running_app().MACRO_PAGE
        self.build_macro_page(editable=False, page=page)

    def generate_page_buttons(self):
        pages = self.ids["pages"]
        with open("./data.json", "r+") as data:
            data = json.load(data)
            for page in data["macro_pages"]:
                button = MacroButton(
                    text=page["name"],
                    size_hint=[0.9, 0.15],
                    on_press=self.change_page(page["name"]),
                )
                pages.add_widget(button)

    def change_page(self, page):
        def inner(_):
            editable = self.ids["edit"].state == "down"
            App.get_running_app().MACRO_PAGE = page
            self.build_macro_page(editable=editable, page=page)

        return inner


class EditButton(ToggleButton):
    def __init__(self, **kwargs):
        super(EditButton, self).__init__(**kwargs)
        self.img_source = "./icons/edit.png"

    def on_down(self):
        pass

    def on_normal(self):
        pass

    def on_state(self, _, state):
        if state == "down":
            self.ids["image"].source = "./icons/edit-clicked.png"
            self.on_down()
        if state == "normal":
            self.ids["image"].source = "./icons/edit.png"
            self.on_normal()


class Macro(BoxLayout):
    """
    Widget koji predstavlja jedan element
    u mreži macroa
    """

    def __init__(
        self,
        button=False,
        editable=False,
        y_pos=0,
        x_pos=0,
        rebuild=None,
        text="",
        press=None,
        **kwargs
    ):
        """Prilikom stvaranja elementa provjerava 
        treba li sadržavati botun ili biti prazno polje
        
        Keyword Arguments:
            button {bool} -- [određuje je li macro ima botun ili ne] (default: {False})
        """

        super(Macro, self).__init__(**kwargs)
        self.rebuild = rebuild
        if button:
            btn = MacroButton(size_hint=[None, None], text=text)
            btn.on_press = press
            self.add_widget(btn)
        elif editable:
            button_new = Button(size_hint=[None, None], text="<NEW>")
            button_new.on_press = self.create_macro(y_pos, x_pos)
            self.add_widget(button_new)

    def submit_macro(self, name, macro, y_pos, x_pos):
        page = App.get_running_app().MACRO_PAGE
        with open("./data.json", "r+") as data:
            x_pos = int(x_pos)
            y_pos = int(y_pos)
            json_data = json.load(data)
            macros = json_data["macro_pages"]
            macros = json_data["macro_pages"][0]["macros"]
            if page:
                macros = list(filter(lambda x: x["name"] == page, macros))[0]["macros"]
            new_macro = {"position": [x_pos, y_pos], "text": name, "macro": macro}
            macros.append(new_macro)
            data.seek(0)
            data.truncate()
            json.dump(json_data, data)
        page = App.get_running_app().MACRO_PAGE
        self.rebuild(editable=True, page=page)

    def create_macro(self, y_pos, x_pos, page=None):
        def inner():
            CreateWidget(self.submit_macro, y_pos, x_pos).open()

        return inner


class ButtonGrid(GridLayout):
    """
    Mreža koja sadržava sve botuna
    """

    def __init__(self, **kwargs):
        """Predefinira broj redova i stupaca mreže
        i generira mrežu
        """

        super(ButtonGrid, self).__init__(**kwargs)
        self.cols = 6
        self.rows = 5
        self.build_macro_page()

    def build_macro_page(self, editable=False, page=None):
        """
        Dohvaća podatke iz data.json filea
        izdvaja sve macroe i generira njihov
        prikaz
        """
        self.clear_widgets()

        with open("./data.json") as data:
            data = json.load(data)
            macros = data["macro_pages"][0]["macros"]
            if page:
                macros = list(filter(lambda x: x["name"] == page, data["macro_pages"]))[
                    0
                ]["macros"]
            macros.sort(key=lambda macro: macro["position"][0])

            for rows in range(self.rows):
                macro_row = list(
                    filter(lambda macro: macro["position"][1] == rows, macros)
                )
                for cols in range(self.cols):
                    visible = len(macro_row) and macro_row[0]["position"][0] == cols
                    if visible:
                        press = App.get_running_app().send_macro
                        new_macro = macro_row.pop(0)
                        new_widg = Macro(
                            button=visible,
                            editable=editable,
                            y_pos=rows,
                            x_pos=cols,
                            rebuild=self.build_macro_page,
                            text=new_macro["text"],
                            press=press(new_macro["macro"].split(",")),
                        )
                        self.add_widget(new_widg)
                    else:
                        self.add_widget(
                            Macro(
                                button=visible,
                                editable=editable,
                                y_pos=rows,
                                x_pos=cols,
                                rebuild=self.build_macro_page,
                            )
                        )
