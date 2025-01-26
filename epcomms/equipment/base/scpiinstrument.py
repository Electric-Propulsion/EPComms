from typing import Union


class SCPIInstrument:
    # Yar, it be a mixin!

    def command_by_channel(
        self, command_keyword: str, argument: str, channel: Union[int, list[int]]
    ) -> str:
        """
        Generates a SCPI command string.

        Args:
            command_keyword (str): The SCPI command keyword.
            argument (str): The command argument.
            channel (int, list[int]): The channel number(s) to apply the command to.

        Returns:
            str: The SCPI command string.
        """
        if isinstance(channel, list):
            channel = ",".join([str(ch) for ch in channel])

        return f"{command_keyword} {argument},(@{channel})"

    def query_by_channel(
        self, query_keyword: str, channel: Union[int, list[int]]
    ) -> str:
        """
        Generates a SCPI query string.

        Args:
            query_keyword (str): The SCPI query keyword.
            channel (int, list[int]): The channel number(s) to query.

        Returns:
            str: The SCPI query string.
        """
        if isinstance(channel, list):
            channel = ",".join([str(ch) for ch in channel])

        return f"{query_keyword}? (@{channel})"
