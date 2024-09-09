from epcomms.equipment.base import Instrument
from epcomms.connection.transmission import Visa


def test_instrument_init():
    instrument = Instrument(transmission=None)
    assert instrument is not None
    assert isinstance(instrument, Instrument)

def test_transmission_construction():
    for transmission in [
        None,
        Visa
         ]:
        instrument = Instrument(transmission)
        assert instrument.transmission == transmission