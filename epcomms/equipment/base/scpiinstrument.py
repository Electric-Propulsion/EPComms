from typing import Callable, TypeVar, Union


class SCPIInstrument:
    # Yar, it be a mixin!

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

        return f"{query_keyword}?{f" {arguments}" if arguments else ''}{',' if arguments and channels else ''}{f" (@{channel_str})" if channels else ''}"

    T = TypeVar("T")

    def parse_response(
        self, conversion_function: Callable[[str], T], response: str
    ) -> T | list[T]:
        value_list = response.strip("\n").split(",")
        if len(value_list) == 1:
            return conversion_function(value_list[0])
        else:
            return [conversion_function(value) for value in value_list]

    @classmethod
    def _channel_string(cls, channels: Union[int, list[int], str]) -> str:
        return (
            ",".join([str(ch) for ch in list(filter(None, channels))])
            if isinstance(channels, str)
            else str(channels)
        )
