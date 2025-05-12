"""Hostname parsing utility."""

from urllib.parse import urlsplit

def parse_hostname(server_addr: str) -> tuple[str, str]:
    """Parse server address and format into a tuple.
    
    :param str server_addr: Server address (in host:port format).
    :return: A tuple of the parsed address, first item being the hostname
                and second item being the port.
    :rtype: tuple[str, str]
    """
    parsed = urlsplit("//" + server_addr)
    return parsed.hostname, parsed.port
