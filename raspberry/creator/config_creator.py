import socket
import json
from pykeyboard import PyKeyboard

STRUCTURE = {"position": [int, int], "text": str, "macro": str}


class ConfigCreator:
    """

    Klasa koja služi stvaranju i formatiranju novih makro naredbi

    """

    def __init__(self):
        pass

    def save_macro(self, macro_data):
        """

        Metoda odgovorna za pohranjivanje makro naredbe u json file

        Argument:
            macro_data {dict} -- {"text": str, "position": [int, int], "macro": str}

        """

        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        valid = self.check_data(macro_data)

        if not valid:
            return

        if "," in macro_data["macro"]:
            macro_data["macro"] = macro_data["macro"].split(",")

        data["macros"].append(macro_data)

        with open("../../data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def check_data(self, data, struct=STRUCTURE):
        """

        Metoda koja prije parsiranja provjerava podatke, tj. dali su objekti rječnika strukturno dobri

        Return:
            [True, False] -- ovisno o točnosti podataka

        """

        if isinstance(struct, dict) and isinstance(data, dict):
            if struct.keys() != data.keys():
                return False
            return all(
                k in data and self.check_data(data[k], struct[k]) for k in struct
            )

        if isinstance(struct, list) and isinstance(data, list):
            if len(struct) != len(data):
                return False
            return all(self.check_data(c, struct[0]) for c in data)

        elif isinstance(struct, type):
            return isinstance(data, struct)

        else:
            return False
