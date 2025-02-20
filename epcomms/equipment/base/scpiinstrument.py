from typing import Union


class SCPIInstrument:
    # Yar, it be a mixin!

    def generate_command(
        self, command_keyword: str, arguments: Union[str, list[str], None] = None, channels: Union[int, list[int], None] = None
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
        if isinstance(channels, list):
            channels = ",".join([str(ch) for ch in channels])

        if isinstance(arguments, list):
            arguments = ",".join(arguments)

        return f"{command_keyword}{f" {arguments}" if arguments else ''}{',' if arguments and channels else ''}{f" (@{channels})" if channels else ''}"

    def generate_query(
        self, query_keyword: str, arguments: Union[str, list[str], None] = None, channels: Union[int, list[int], None] = None
    ) -> str:
        """
        Generates a SCPI query string.

        Args:
            query_keyword (str): The SCPI query keyword.
            channel (int, list[int]): The channel number(s) to query.

        Returns:
            str: The SCPI query string.
        """
        if isinstance(channels, list):
            channels = ",".join([str(ch) for ch in channels])

        if isinstance(arguments, list):
            arguments = ",".join(arguments)


        return f"{query_keyword}?{f" {arguments}" if arguments else ''}{',' if arguments and channels else ''}{f" (@{channels})" if channels else ''}"
