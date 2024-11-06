from ctypes import *
from . import dwfconstants
import socket


from epcomms.connection.transmission.transmission import Transmission
from epcomms.equipment.daq import DAQ

from . import dwf, AnalogDiscoveryFunctionGenerator, AnalogDiscoveryDAQ


class AnalogDiscovery():

    @classmethod
    def list_devices(cls) -> dict[int, str]:
        num_devices = c_int(0)
        devices: dict[str, int] = {}  # index, serial number

        dwf.FDwfEnum(dwfconstants.enumfilterAll, byref(num_devices))
        for device_index in range(0, num_devices.value):
            device_sn = create_string_buffer(16)
            dwf.FDwfEnumSN(c_int(device_index), device_sn)
            serial_number_string = str(device_sn.value.decode("utf-8")).split(":")[-1]
            devices[serial_number_string] = device_index
        return devices

    @classmethod
    def wake_networked_device(cls, ip_addr: str):
        # I haven't really been able to test this, not sure if it works
        timeout_s = 5
        try:
            socket.setdefaulttimeout(timeout_s)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(
                (ip_addr, 17)
            )  # I don't think the port number matters (It seems to wake on ICMP packets, even) so this is QOTD lol.
        except OSError as error:
            return False
        else:
            s.close()
            return True

    def __init__(self, ip_addr: str, serial_number: str):
        devices = self.list_devices()
        if serial_number not in devices:
            # It might need to be woken
            # This hasn't been tested
            self.wake_networked_device(ip_addr)
            devices = self.list_devices()
            if serial_number not in devices:
                # The device ain't here, raise an exception
                raise ValueError("The specified serial number was not found")

        self.device_handle = c_int()

        device_index = devices[serial_number]

        dwf.FDwfDeviceOpen(c_int(device_index), byref(self.device_handle))
        dwf.FDwfParamSet(c_int(4), c_int(1))


        if self.device_handle.value == dwfconstants.hdwfNone.value:
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            raise ConnectionError(
                f"Failed to open Analog Discovery device: {szerr.value}"
            )
        
        self.function_generator = AnalogDiscoveryFunctionGenerator(self.device_handle)
        self.daq = AnalogDiscoveryDAQ(self.device_handle)

    def close(self):
        dwf.FDwfDeviceClose(self.device_handle)
        self.device_handle = None
