from epcomms.connection.packet import ASCII
from epcomms.connection.transmission import Telnet

from . import SCPIMultimeter


class TektronixDMM4050(SCPIMultimeter[ASCII]):

    def __init__(self, host: str, port: int):
        transmission = Telnet(host, port, "\n", 5)
        super().__init__(transmission, ASCII)
        self.command_remote()

    def command_remote(self) -> None:
        """
        Sends a command to the multimeter to switch to remote mode.

        This method uses the transmission interface to send the "*RST" command
        to the connected Tektronix DMM4050 multimeter, causing it to switch to
        remote mode.

        Returns:
            None
        """
        self.transmission.command(
            self._packet.from_data(self.generate_command("SYST:REM"))
        )

    def command_local(self) -> None:
        """
        Sends a command to the multimeter to switch to local mode.

        This method uses the transmission interface to send the "*RST" command
        to the connected Tektronix DMM4050 multimeter, causing it to switch to
        local mode.

        Returns:
            None
        """
        self.transmission.command(
            self._packet.from_data(self.generate_command("SYST:LOC"))
        )

    def display_text(self, text: str) -> None:
        """
        Sends a command to the multimeter to display text on the screen.

        This method uses the transmission interface to send the "DISP:TEXT"
        command to the connected Tektronix DMM4050 multimeter, causing it to
        display the specified text on the screen.

        Args:
            text (str): The text to display on the screen.

        Returns:
            None
        """
        self.transmission.command(
            self._packet.from_data(
                self.generate_command("DISP:TEXT", arguments=f'"{text}"')
            )
        )

    def clear_text(self) -> None:
        """
        Sends a command to the multimeter to clear the display.

        This method uses the transmission interface to send the "DISP:TEXT:CLEAR"
        command to the connected Tektronix DMM4050 multimeter, causing it to
        clear the display.

        Returns:
            None
        """
        self.transmission.command(
            self._packet.from_data(self.generate_command("DISP:TEXT:CLE"))
        )
