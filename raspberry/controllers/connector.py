from .connection_controller import ConnectionController
from .wifi_controller import WifiController
import socket
import json

class Connector:
    def __init__(self):
        self.wifi = WifiController()
        self.host_finder = ConnectionController(socket.AF_INET, socket.SOCK_DGRAM)

    def scan_wifis(self):
        return self.wifi.find_nearby_wifis()
    
    def connect_to_wifi(self, name, password):
        return self.wifi.connect_to_wifi(name, password=password)
    
    def scan_hosts(self):
        self.host_finder.start()
        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        return data["all_hosts"]
    
    def connect_to_host(self, name):
        with open("./data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        
        for host in data["all_hosts"]:
            if host["name"] == name:
                selected_host = host        
        
        data["pc_host"] = selected_host["address"]

        with open("./data.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        
        return True