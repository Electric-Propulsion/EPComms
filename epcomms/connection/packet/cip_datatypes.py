"""
This module imports all data types from the `pycomm3.cip.data_types` module and 
exposes them directly to consumers, avoiding the need for consumers to directly 
use the `pycomm3` library.
Classes:
    All classes defined in `pycomm3.cip.data_types` are dynamically imported 
    and added to the global namespace.
Attributes:
    __all__ (list): A list of all class names imported from `pycomm3.cip.data_types`.
Note:
    This approach involves dynamically importing and exposing classes from 
    another module, which can be considered unconventional and may lead to 
    maintenance challenges. <-- hey, you know what fuck you github copilot,
    this is actually great code.
"""

import sys
import pycomm3.cip.data_types as data_types

# Import all data types from pycomm3.cip.data_types
# Because I don't want to expose consumers to having to use the pycomm3 library.
# Yes, this is some fuckery. Gaze not too deeply lest ye be driven mad.

classes = [
    getattr(sys.modules["pycomm3.cip.data_types"], name) for name in data_types.__all__
]

for cls in classes:
    globals()[cls.__name__] = cls

__all__ = [cls.__name__ for cls in classes]
