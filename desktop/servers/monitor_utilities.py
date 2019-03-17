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

        Metoda koja uzima sve privatne metode i izvlači podatke iz njih.

        Returns:
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

        Metoda koja dohvaća postotke korištenosti pojedine jezgre procesora

        Returns:
            [list] -- postotak korištenja pojedinog cpua [int, int, int, int]
        """

        return [cpu * 10 for cpu in psutil.cpu_percent(percpu=True)]

    def __get_temp(self):
        """

        Metoda koja dobavlja temperaturu jezgara

        Returns:
            [int] -- temperatura korištenih jezgri

        """
        try:
            temps = [temp for temp in psutil.sensors_temperatures()["coretemp"]]
            return max([temp.current for temp in temps])
        except:
            return 0

    def __get_memory(self):
        """

        Metoda koja dobavlja trenutno korištenu količinu radne meorije

        Returns:
            [dict] -- objekt rječnika koji sadrži podatke o korištenju RAM-a {"used":int, "total":int}  

        """

        memory = psutil.virtual_memory()
        total = self._convert_to_gb(memory.total)
        used = self._convert_to_gb(memory.used)
        return {"used": used, "total": total}

    def __get_disk_usage(self):
        """

        Metoda koja dobavlja količinu memorije zauzete na disku

        Returns:
            [dict] -- objekt rječnika koji sadrži podatke o korišteju stalne memorije {"used":int, "total":int}

        """

        disk = psutil.disk_usage("/")
        total = self._convert_to_gb(disk.total)
        used = self._convert_to_gb(disk.used)
        return {"used": used, "total": total}

    def _convert_to_gb(self, byte_memory):
        """

        Metoda koja pretvara byteove u kilobyteove

        Arguments:
            byte_memory {int} -- veličina memorije u byteovima

        Returns:
            [float] -- količina memorije u gb

        """

        return round(byte_memory / math.pow(1024, 3), 1)
