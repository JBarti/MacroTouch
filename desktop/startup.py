import socket
import platform
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = platform.node()
system = platform.system()
release = platform.release()

data = {"name": name, "system": system, "release": release}


bytes_data = bytes(json.dumps(data), "UTF-8")

sock.sendto(bytes_data, ("192.168.0.17", 5300))
