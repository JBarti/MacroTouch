import psutil
import math


class SystemMonitor:
    def __init__(self):
        pass

    def get_system_data(self):
        return {
            "cpus": self.__get_cpus(),
            "temp": self.__get_temp(),
            "memory": self.__get_memory(),
            "disk": self.__get_disk_usage(),
        }

    def __get_cpus(self):
        return [cpu * 10 for cpu in psutil.cpu_percent(percpu=True)]

    def __get_temp(self):
        temps = [temp for temp in psutil.sensors_temperatures()["coretemp"]]
        return max([temp.current for temp in temps])

    def __get_memory(self):
        memory = psutil.virtual_memory()
        total = self.__convert_to_gb(memory.total)
        used = self.__convert_to_gb(memory.used)
        return {"used": used, "total": total}

    def __get_disk_usage(self):
        disk = psutil.disk_usage("/")
        total = self.__convert_to_gb(disk.total)
        used = self.__convert_to_gb(disk.used)
        return {"used": used, "total": total}

    def __convert_to_gb(self, byte_memory):
        return round(byte_memory / math.pow(1024, 3), 1)
