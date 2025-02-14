from epcomms.connection.transmission import Telnet
from epcomms.connection.packet import ASCII

telnet = Telnet("192.168.0.136", 3490, "\r\n", ASCII)

print(telnet.poll(ASCII("*IDN?")).data)