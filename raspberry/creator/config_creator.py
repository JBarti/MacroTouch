import socket
import json
from pykeyboard import PyKeyboard

k = PyKeyboard()

SPECIAL_KEYS_DICT = {
    "CTRL": k.control_key,
    "ALT": k.alt_key,
    "F1": k.function_keys[1],
    "F2": k.function_keys[2],
    "F3": k.function_keys[3],
    "F4": k.function_keys[4],
    "F5": k.function_keys[5],
    "F6": k.function_keys[6],
    "F7": k.function_keys[7],
    "F8": k.function_keys[8],
    "F9": k.function_keys[9],
    "F10": k.function_keys[10],
    "F11": k.function_keys[11],
    "F12": k.function_keys[12],
    "TAB": k.tab_key,
    "SHIFT": k.shift_key,
    "ESCAPE": k.escape_key,
    "PRTSCR": k.print_screen_key,
    "INSERT": k.insert_key,
    "DELETE": k.delete_key,
    "PAGE_UP": k.page_up_key,
    "PAGE_DOWN": k.page_down_key,
    "HOME": k.home_key,
    "BACKSPACE": k.backspace_key,
    "SUPER": k.super_l_key,
}

STRUCTURE = {"position": [int, int], "text": str, "macro": str}


class ConfigCreator:
    def __init__(self):
        pass

    def save_macro(
        self, macro_data
    ):  ####  macro_data is dict : { "position":[int, int], "text":str, "macro":str }
        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        parsed_data = self.parse_macro(macro_data["payload"])

        if not parsed_data:
            return

        data["macros"].append(macro_data["payload"])

        with open("../../data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def parse_macro(self, payload):

        if not self.check_data(payload):
            return False

        macro = payload["macro"]
        macro = macro.strip().split("+")

        try:
            macro = [SPECIAL_KEYS_DICT[key] for key in macro]
        except KeyError:
            return False

        payload["macro"] = macro

        return payload

    def check_data(self, data, struct=STRUCTURE):

        if isinstance(struct, dict) and isinstance(data, dict):
            if struct.keys() != data.keys():
                return False
            return all(
                k in data and self.check_data(data[k], struct[k])
                for k in struct
            )

        if isinstance(struct, list) and isinstance(data, list):
            if len(struct) != len(data):
                return False
            return all(self.check_data(c, struct[0]) for c in data)

        elif isinstance(struct, type):
            return isinstance(data, struct)

        else:
            return False
