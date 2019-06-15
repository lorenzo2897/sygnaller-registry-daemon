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


# *****************************************
# Unit tests
# *****************************************

import unittest


class TestEntry(unittest.TestCase):

    def test_init(self):
        # make
        t = time.time()
        entry = Entry("MAC", "IP", t)
        # test
        self.assertEqual(entry.mac, "MAC")
        self.assertEqual(entry.ip, "IP")
        self.assertEqual(entry.time, int(t))

    def test_json(self):
        # make
        t = time.time()
        entry = Entry("MAC", "IP", t)
        # test
        expect = {
            "mac": "MAC",
            "ip": "IP",
            "time": int(t)
        }
        self.assertEqual(entry.toJSON(), expect)


class TestRegistry(unittest.TestCase):

    def test_empty(self):
        r = Registry()
        self.assertEqual(len(r.db), 0)

    def test_register(self):
        r = Registry()
        r.register("MAC1", "IP1")
        self.assertEqual(len(r.db), 1)
        r.register("MAC2", "IP2")
        self.assertEqual(len(r.db), 2)  # add
        r.register("MAC1", "IP2")
        self.assertEqual(len(r.db), 2)  # replace

    def test_query(self):
        r = Registry()
        r.register("MAC1", "IP1")
        self.assertEqual(r.query("MAC1").ip, "IP1")
        r.register("MAC1", "IP2")
        self.assertEqual(r.query("MAC1").ip, "IP2")
        self.assertIsNone(r.query("MAC0"))


if __name__ == '__main__':
    unittest.main()
