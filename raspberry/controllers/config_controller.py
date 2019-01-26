import socket
import threading
import json

class Client(threading.Thread):

    def __init__(self, conn):
        super(Client, self).__init__()
        self.conn = conn
        self.data =""

    def run(self):
        while True:
            self.data = self.data + self.conn.recv(2048)
            if self.data != "":
                macro_json = json.loads(self.data.decode("ASCII"))
                self.update_json(macro_json)
                self.data=""

    def update_json(self, macro_data):
        with open("../../data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data["macros"].append(macro_data["payload"])

        with open("../../data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

#{type:MACRO_POST, payload:{name:"", keys:"""}}

    def close_connection(self):
        self.conn.close()

## server = ConfigController(family-socketa, socket-type, ip_address=, port=)  --> (ip_address, port su kwargs)
## server.start() --> starta thread sa funkcijom run koja slusa za konekcije i otvara po konekciji novi thread di handlea podatke

class ConfigController(threading.Thread):
    
    def __init__(self, family, sock_type, ip_address="192.168.0.17", port=5300):
        super(ConfigController, self).__init__()
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((ip_address, port))
        self.clients = []

    def run(self):
        while True:
            conn, address = self.sock.accept()
            client = Client(conn)
            client.start()
            self.clients.append(client)
    
    def close_connections(self):
        for client in self.clients:
            client.close_connection()