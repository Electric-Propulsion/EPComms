# Load the digilent SDK 
from ctypes import *
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#check library loading errors
szerr = create_string_buffer(512)
dwf.FDwfGetLastErrorMsg(szerr)
if szerr[0] != b'\0':
    print(str(szerr.value))



# Normal __init__ stuff
from . import dwfconstants
from .analog_discovery import AnalogDiscovery