from epcomms.equipment.base import Instrument, TransmissionTypeT


class VacuumController(
    Instrument[TransmissionTypeT]
):  # pylint: disable=too-few-public-methods
    # Fat lot of good this is doing.
    # TODO: come on.
    """Abstract Base Class for all Vacuum Controllers."""
