import unittest
import platform
import logging

import numpy as np

from src.bpod import Bpod
from mock_serial import MockSerial

logging.basicConfig(level=logging.DEBUG)

if platform.system() == "Linux":
    hw_description = b"\x00\x01d\x00Z\x10\x08\x10\x0cUUUUUXBBPPPP\x10UUUUUXBBPPPPVVVV"

    device = MockSerial()
    device.open()
    device.stub(name="uint8", receive_bytes=b"A", send_bytes=b"B")
    device.stub(name="array", receive_bytes=b"Ba", send_bytes=b"OK")
    device.stub(
        name="get_firmware_version",
        receive_bytes=b"F",
        send_bytes=(22).to_bytes(2, "little") + (3).to_bytes(2, "little"),
    )
    device.stub(name="handshake", receive_bytes=b"6", send_bytes=b"5")
    device.stub(
        name="get_timestamp_transmission",
        receive_bytes=b"G",
        send_bytes=(1).to_bytes(1, "little"),
    )

    device.stub(
        name="get_hardware_description", receive_bytes=b"H", send_bytes=hw_description
    )
    device.stub(
        name="enable_ports",
        receive_bytes=b"E\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01",
        send_bytes=b"\x01",
    )
    device.stub(name="set_sync_channel", receive_bytes=b"K\xff\x01", send_bytes=b"\x01")
    device.stub(
        name="get_modules", receive_bytes=b"M", send_bytes=b"\x00\x00\x00\x00\x00"
    )
    device.stub(
        name="set_number_of_events_per_module",
        receive_bytes=b"%\x0f\x0f\x0f\x0f\x0f\x0f",
        send_bytes=b"\x01",
    )
    device.stub(
        name="disconnect_state_machine",
        receive_bytes=b"Z",
        send_bytes=b"",
    )


@unittest.skipUnless(platform.system() == "Linux", "MockSerial depends on Linux OS")
class TestSerial(unittest.TestCase):
    def test_datatypes(self):
        bpod = Bpod(port=device.port, timeout=0.1)
        assert bpod.is_open
        assert bpod.query(b"A") == b"B"
        assert bpod.query(np.uint8(65)) == b"B"
        assert bpod.query([np.uint8(66), "a"], 2) == b"OK"
        bpod.close()
        assert not bpod.is_open

    def test_initialization(self):
        bpod = Bpod(port=device.port, timeout=0.1)
        assert bpod.version["major"] == 22
        assert bpod.hardware["input_description_array"] == b"UUUUUXBBPPPP"
        assert bpod.hardware["output_description_array"] == b"UUUUUXBBPPPPVVVV"
        bpod.close()
