from epcomms.connection.packet import ASCII
from pytest import fail

test_data = [
    "EXAMPLE:TEST:STRING 0,(@0)",
    "",
    "a"
]

def test_serialize_str():
    for string in test_data:
        packet = ASCII(string)
        assert packet.serialize_str() == string

def test_serialise_bytes():
    for string in test_data:
        packet = ASCII(string)
        try:
            packet.serialize_bytes()
        except NotImplementedError:
            pass
        else:
            fail('A NotImplementedError should have been raised')
