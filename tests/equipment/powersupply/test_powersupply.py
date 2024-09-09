from epcomms.equipment.powersupply import PowerSupply
from epcomms.connection.transmission import Transmission
from epcomms.connection.packet import Packet
from pytest import fail
from inspect import signature

from unittest.mock import patch

@patch.multiple(PowerSupply, __abstractmethods__=set())
@patch.multiple(Transmission, __abstractmethods__=set())
def test_init_patched():
    for transmission in [None, Transmission(Packet)]:
        supply = PowerSupply(transmission)
        assert supply.transmission == transmission

def test_init_unpatched():
    try:
        supply=PowerSupply(None)
    except TypeError:
        pass
    else:
        fail("A TypeError should have been raised")

@patch.multiple(PowerSupply, __abstractmethods__=set())
def test_not_implemented():
    supply = PowerSupply(None)

    for method_name in [
        "set_voltage",
        "measure_voltage",
        "set_current",
        "measure_current",
        "enable_output",
        "disable_output",
    ]:
        try:
            method = getattr(supply, method_name)
            params = dict(signature(method).parameters)
            params.pop("channel")
            method(supply,0) if len(params) == 1 else method(supply)
        except NotImplementedError:
            pass # Expected
        else:
            fail("a NotImplementedError should have been raised")
