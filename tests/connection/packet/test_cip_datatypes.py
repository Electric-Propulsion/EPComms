import sys
import pycomm3.cip.data_types as pycomm_data_types
import epcomms.connection.packet.cip_datatypes as epcomms_data_types

def test_all_identical():
    assert pycomm_data_types.__all__ == epcomms_data_types.__all__

def test_classes_identical():
    for cls_name in pycomm_data_types.__all__:
        pycomm_cls = getattr(sys.modules["pycomm3.cip.data_types"], cls_name)
        epcomms_cls = getattr(sys.modules["epcomms.connection.packet.cip_datatypes"], cls_name)

        assert pycomm_cls == epcomms_cls