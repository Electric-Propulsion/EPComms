from epcomms.base import Controller


def test_controller_init():
    controller = Controller()
    assert controller is not None
    assert isinstance(controller, Controller)
