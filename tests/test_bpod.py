import logging
import unittest

from src.bpod import Bpod, SerialSingleton, SerialSingletonException

logging.basicConfig(level=logging.DEBUG)


class TestBpod(unittest.TestCase):
    def test_unconnected(self):
        bpod = Bpod(connect=False)
        assert bpod.is_open is False

    def test_singleton(self):
        # create a few instances
        bpod1 = Bpod(connect=False)
        bpod2 = Bpod(connect=False)
        bpod3 = Bpod('FakePort3', connect=False)
        bpod4 = Bpod('FakePort4', connect=False)
        bpod5 = Bpod(port='FakePort4', connect=False)

        # assert that a port blocked by *another* SerialSingleton child can't be used
        with self.assertRaises(SerialSingletonException):
            SerialSingleton('FakePort4')

        # assert that port cannot be changed after initialization
        with self.assertRaises(SerialSingletonException):
            bpod5.port = 'some_other_port'

        # assert singleton behavior
        assert bpod1 is bpod2
        assert bpod1 is not bpod3
        assert bpod3 is not bpod4
        assert bpod4 is bpod5

    def test_set_port(self):
        bpod = Bpod(connect=False)
        self.assertRaises(Exception, bpod.setPort)
