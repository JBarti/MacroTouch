import socket
from pymouse import PyMouse

UDP_IP = "192.168.0.17"
UDP_PORT = 5005
MESSAGE = "HELLO WURLD"

m = PyMouse()

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP


while True:
    x, y = m.position()
    MESSAGE = str(x) + " " + str(y)
    print("sending, ", MESSAGE)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

