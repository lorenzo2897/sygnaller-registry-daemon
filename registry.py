import time


class Entry:
    def __init__(self, mac, ip, t):
        self.mac = mac
        self.ip = ip
        self.time = int(t)

    def toJSON(self):
        return {
            "mac": self.mac,
            "ip": self.ip,
            "time": self.time
        }


class Registry:
    def __init__(self):
        self.db = {}

    def register(self, mac, ip):
        self.db[mac] = Entry(mac, ip, time.time())

    def query(self, mac):
        if mac in self.db:
            return self.db[mac]
        else:
            return None
