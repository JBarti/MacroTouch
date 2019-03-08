from servers import ConnectionServer, MonitorServer, MacroServer
import socket

conn_server = ConnectionServer(socket.AF_INET, socket.SOCK_DGRAM)
rpi_host = conn_server.start()
monitor_server = MonitorServer(socket.AF_INET, socket.SOCK_DGRAM, rpi_host)
macro_server = MacroServer(socket.AF_INET, socket.SOCK_DGRAM)

monitor_server.start()
macro_server.start()
