from subprocess import check_output
import re


class WifiController:

    """

    Klasa koja se kontrolira pristup wifiu

    """

    def __init__(self):
        """
        
        Inicijalna metoda klase

        """

        self.wifis = self.find_nearby_wifis()

    def connect_to_wifi(self, name, password=None):

        """
        
        Metoda koja povezuje uređaj na wifi

        Returns:
            [bool] -- True ako je uspješno povezan, False ako nije

        """

        if password is not None:
            output = check_output(
                ["nmcli", "device", "wifi", "connect", name, "password", password]
            )
        else:
            output = check_output(["nmcli", "device", "wifi", "connect", name])

        output = bytes.decode(output)

        if output[:5] == "Error":
            return False

        return True

    def find_nearby_wifis(self):

        """
        
        Metoda koja skenira sve wifie u blizini
        
        Returns:
            [list] -- lista podataka o svakom wifiu u blizini
        """

        bytes_wifis = check_output(["nmcli", "d", "wifi", "list"])
        parsed_data = self.parse_wifi_data(bytes_wifis)

        return parsed_data

    def parse_wifi_data(self, bytes_data):

        """
        
        Metoda koja parsira podatke wifia
        
        Returns:
            [list] -- lista podataka o svakom wifiu u blizini
        """

        roughly_parsed = bytes.decode(bytes_data).split("\n")[1:]
        stripped_parsed = [wifi.strip() for wifi in roughly_parsed]
        list_parsed = [re.sub("  +", "$", wifi).split("$") for wifi in stripped_parsed]

        parsed = [self.to_data_dict(wifi_data) for wifi_data in list_parsed]

        return parsed

    def to_data_dict(self, lst_data):

        """
        
        Metoda koja pretvara str podataka o wifiu u dictionary sa danim podatcima iz stringa
        
        Returns:
            [dict] -- podatci o wifiu u obliku dictionarya
        """

        k = 1 if lst_data[0] == "*" else 0
        data = {
            "name": lst_data[0 + k],
            "signal": lst_data[4 + k],
            "security": None if lst_data[6 + k] == "--" else lst_data[6 + k],
            "connected": k == 1,
        }
        return data
