from epcomms.connection.transmission import Transmission
from epcomms.connection.packet import Packet
from pytest import fail
from unittest.mock import patch, MagicMock

@patch.multiple(Transmission, __abstractmethods__=set())
@patch.multiple(Packet, __abstractmethods__=set())
def test_initialize_valid():
    transmission = Transmission(Packet)    
    assert transmission is not None
    assert isinstance(transmission, Transmission)

@patch.multiple(Transmission, __abstractmethods__=set())
def test_initialize_invalid():
    try:
        transmission = Transmission(str)
    except TypeError:
        pass
    else:
        fail("A TypeError should have been raised")

def test_init():
    try:
        transmission = Transmission(Packet)
    except TypeError:
        pass
    else:
        fail("A TypeError should have been raised")

@patch.multiple(Transmission, __abstractmethods__=set())
def test_command():
    transmission = Transmission(Packet)
    try:
        transmission.command("")
    except NotImplementedError:
        pass
    else:
        fail('A NotImplementedError should have been raised')

@patch.multiple(Transmission, __abstractmethods__=set())
def test_read():
    transmission = Transmission(Packet)
    try:
        transmission.read()
    except NotImplementedError:
        pass
    else:
        fail('A NotImplementedError should have been raised')

@patch.multiple(Transmission, __abstractmethods__=set())
def test_poll():
    for test_value in [
        "",
        "0.0005E+004"
        "a",
        "SOUR:MEAS:VOLT (@3)"
    ]:
        transmission = Transmission(Packet)

        transmission.command = MagicMock()
        transmission.read = MagicMock(return_value=test_value)

        assert transmission.poll(test_value) == test_value

        transmission.command.assert_called_once_with(test_value)
        transmission.read.assert_called_once()





    

