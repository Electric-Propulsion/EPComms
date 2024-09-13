from epcomms.connection.packet.cip import CIPTX, CIPRX
from epcomms.connection.packet.cip_datatypes import *

def test_init():
    class_codes = [0, 1, 255]
    instances = [0, 1, 255]
    attributes = [0, 1 , 255]
    parameters_datatypes = [{
            "params": [0, 1, 255],
            "types": [USINT, UINT, UDINT, ULINT]
        },{
            "params": [-127, -1, 0, 1, 127],
            "types": [SINT, INT, DINT, LINT]
        },{
            "params": [-1.0, 0.0, 1.0],
            "types": [REAL, LREAL]
        },{
            "params": [b'\x00',b'\x01', 0, 1],
            "types": [None]
        }]

    for class_code in class_codes:
        for instance in instances:
            for attribute in attributes:
                for param_group in parameters_datatypes:
                    for param in param_group["params"]:
                        for type_ in param_group["types"]:
                            packet = CIPTX(
                                class_code = class_code,
                                instance = instance,
                                attribute = attribute,
                                parameters = param,
                                data_type = type_
                            )
    
