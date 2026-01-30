from typing import Callable, TypeVar, Union


class SCPIInstrument:
    """
    SCPI Instrument Mixin Class.

    This mixin provides utility methods for generating SCPI command and query
    strings, as well as parsing SCPI responses.
    """

    def generate_command(
        self,
        command_keyword: str,
        arguments: Union[str, list[str], None] = None,
        channels: Union[int, list[int], None] = None,
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

        channel_str = self._channel_string(channels) if channels else None

        if isinstance(arguments, list):
            arguments = ",".join(list(filter(None, arguments)))

        # pylint: disable=line-too-long
        # IDK man it's a long line, what are you gonna do
        return f"{command_keyword}{f" {arguments}" if arguments else ''}{',' if arguments and channels else ''}{f" (@{channel_str})" if channels else ''}"

    def generate_query(
        self,
        query_keyword: str,
        arguments: Union[str, list[str], None] = None,
        channels: Union[int, list[int], None] = None,
    ) -> str:
        """
        Generates a SCPI query string.

        Args:
            query_keyword (str): The SCPI query keyword.
            channel (int, list[int]): The channel number(s) to query.

        Returns:
            str: The SCPI query string.
        """
        channel_str = self._channel_string(channels) if channels else None

        if isinstance(arguments, list):
            arguments = list(filter(None, arguments))
            arguments = ",".join(arguments)

        # pylint: disable=line-too-long
        return f"{query_keyword}?{f" {arguments}" if arguments else ''}{',' if arguments and channels else ''}{f" (@{channel_str})" if channels else ''}"

    T = TypeVar("T")

    def parse_response(
        self, conversion_function: Callable[[str], T], response: str
    ) -> T | list[T]:
        """
        Parse a SCPI response

        Args:
            conversion_function (Callable[[str], T]): callable to convert a
                scpi string into a list of values
            response (str): the SCPI response string

        Returns:
            T | list[T]: the converted value(s)
        """
        value_list = response.strip("\n").split(",")
        if len(value_list) == 1:
            return conversion_function(value_list[0])

        return [conversion_function(value) for value in value_list]

    @classmethod
    def _channel_string(cls, channels: Union[int, list[int], str]) -> str:
        return (
            ",".join([str(ch) for ch in list(filter(None, channels))])
            if isinstance(channels, list)
            else str(channels)
        )
