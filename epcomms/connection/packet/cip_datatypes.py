import pycomm3.cip.data_types as data_types
import sys

# Import all data types from pycomm3.cip.data_types
# Because I don't want to expose consumers to having to use the pycomm3 library.
# Yes, this is some fuckery. Gaze not too deeply lest ye be driven mad.

classes = [
    getattr(sys.modules["pycomm3.cip.data_types"], name) for name in data_types.__all__
]

for cls in classes:
    globals()[cls.__name__] = cls

__all__ = [cls.__name__ for cls in classes]
