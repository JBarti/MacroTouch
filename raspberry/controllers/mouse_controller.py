import socket

class MouseController:


    def __init__(self, family, sock_type, ip_address="192.168.0.17", port=5100):
        self.sock = socket.socket(family, sock_type)
        self.address = (ip_address, port)


    def send_location_data(self, location): #type(location) --> list
        position_x = str(location[0])
        position_y = str(location[1])

        str_mouse_location = position_x + " " + position_y
        
        location = bytes(str_mouse_location, "UTF_8") #bytes object, example of it "23 67"
        self.sock.sendto(location, self.address) #sending to 192.168.0.17:5100


    def send_click_data(self, click_type): #type(click_type) --> int
        click_type = str(click_type)

        click = bytes(click_type, "UTF-8")
        self.sock.sendto(click, self.address)
