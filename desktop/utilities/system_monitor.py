import psutil
import math


class SystemMonitor:
    """

    Klasa koja služi za dobavljanje podataka o sistemu

    """

    def __init__(self):
        pass

    def get_system_data(self):
        """

        Metoda koja okuplja sve privatne metode i izvlači podatke iz njih.

        Return:
            [dict] -- objekt rječnika koji sadrži sve podatke o sistemu
        """

        return {
            "cpus": self.__get_cpus(),
            "temp": self.__get_temp(),
            "memory": self.__get_memory(),
            "disk": self.__get_disk_usage(),
        }

    def __get_cpus(self):
        """

        Metoda koja dobavlja postotke korištenosti pojedine jezgre procesora

        Return:
            [list] -- [int, int, int, int] postotak korištenja pojedinog cpua
        """

        return [cpu * 10 for cpu in psutil.cpu_percent(percpu=True)]

    def __get_temp(self):
        """

        Metoda koja dobavlja temperaturu jezgara

        Return:
            [int] -- temperatura korištenih jezgri

        """
        try:
            temps = [temp for temp in psutil.sensors_temperatures()[
                "coretemp"]]
        except:
            temps = []
        return max([temp.current for temp in temps])

    def __get_memory(self):
        """

        Metoda koja dobavlja trenutno korištenu količinu radne meorije

        Return:
            [dict] -- {"used":int, "total":int} objekt rječnika koji sadrži podatke o korištenju RAM-a 

        """

        memory = psutil.virtual_memory()
        total = self.__convert_to_gb(memory.total)
        used = self.__convert_to_gb(memory.used)
        return {"used": used, "total": total}

    def __get_disk_usage(self):
        """

        Metoda koja dobavlja količinu memorije zauzete na disku

        Return:
            [dict] -- {"used":int, "total":int} objekt rječnika koji sadrži podatke o korišteju stalne memorije

        """

        disk = psutil.disk_usage("/")
        total = self.__convert_to_gb(disk.total)
        used = self.__convert_to_gb(disk.used)
        return {"used": used, "total": total}

    def __convert_to_gb(self, byte_memory):
        """

        Metoda koja pretvara byteove u kilobyteove

        Argumenti:
            byte_memory {int} -- veličina memorije u byteovima

        Return:
            [float] -- količina memorije u gb

        """

        return round(byte_memory / math.pow(1024, 3), 1)
