from epcomms.connection.packet import Packet
from pytest import fail
from unittest.mock import patch

def test_init_packet():
    try:
        packet = Packet()
    except TypeError:
        pass
    else:
        fail("A TypeError should have been raised")

@patch.multiple(Packet, __abstractmethods__=set())
def test_serialize_bytes():
    test_packet = Packet()
    try:
        test_packet.serialize_bytes()
    except NotImplementedError:
        pass
    else:
        fail('A NotImplementedError should have been raised')

@patch.multiple(Packet, __abstractmethods__=set())
def test_serialize_str():
    test_packet = Packet()
    try:
        test_packet.serialize_str()
    except NotImplementedError:
        pass
    else:
        fail('A NotImplementedError should have been raised')
