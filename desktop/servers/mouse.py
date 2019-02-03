from pymouse import PyMouse
import threading
import socket
import json

# HONESTLY I DONT KNOW IF WE NEED THIS SINCE YOU MADE THE UDPCLIENT.JAVA BUT I MADE IT ANYWAY LOL XD


class MouseServer(threading.Thread):
    def __init__(self, family, sock_type, ip_address="0.0.0.0", port=5100):
        super(MouseServer, self).__init__()
        self.daemon = True
        self.sock = socket.socket(family, sock_type)
        self.sock.bind((ip_address, port))
        self.mouse = PyMouse()

    def run(self):
        while True:
            bytes_data = self.sock.recv(1024)
            str_data = bytes_data.decode("ASCII")
            if len(str_data) == 1:
                self.handle_click(str_data)
                continue
            lst_position = [int(percentage) for percentage in str_data.split(" ")]
            position_tup = self.parse_position(lst_position)
            self.mouse.move(position_tup[0], position_tup[1])

    def parse_position(self, data):
        screen_size = self.mouse.screen_size()
        x_position = screen_size[0] * data[0]
        y_position = screen_size[1] * data[1]
        return (x_position, y_position)

    def handle_click(self, data):
        click_type = int(data)
        position = self.mouse.position()
        self.mouse.click(position[0], position[1], click_type)
