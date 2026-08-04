"""Server info utilities."""

import time
from geoip2.errors import AddressNotFoundError

from tf2log.extensions import geoip


def process_time(player_list: list) -> list:
    """Process time string in a player list.

    :param list player_list: Player list.
    :return: Player list with processed time string.
    :rtype: list
    """
    item: dict
    for item in player_list:
        item.update({"duration": int(item.get("time"))})
        duration = time.gmtime(item["duration"])
        item["time"] = time.strftime("%H:%M:%S", duration)
        if int(time.strftime("%H", duration)) == 0:
            item["time"] = time.strftime("%M:%S", duration)
    return player_list


def is_ip_fake_ip(server_ip: str) -> bool:
    """Check if an IP is a fake IP from SDR.

    :param str server_ip: IP address.
    :return: True if IP is a fake IP, False otherwise.
    :rtype: bool
    """
    if server_ip.startswith("169.254"):
        return True
    return False


def format_location(server_ip: str) -> str:
    """Get a formatted location string from an IP.

    :param str server_ip: IP address.
    :return: Formatted location string.
    :rtype: str
    """
    if is_ip_fake_ip(server_ip):
        return ""
    location = ""
    try:
        ip_geo = geoip.geoip_reader.city(server_ip)
        state_name = ip_geo.subdivisions.most_specific.name
        city_name = ip_geo.city.name
        country_name = ip_geo.country.name
        if city_name is not None and state_name is not None:
            location = f"{city_name}, {state_name} - {country_name}"
        elif city_name is None and state_name is None:
            location = country_name
        elif city_or_state_name := city_name or state_name:
            location = f"{city_or_state_name} - {country_name}"
    except AddressNotFoundError:
        pass
    return location


def is_port_valid(port: int) -> bool:
    """Check if a port is a valid port for a TF2 server.

    :param int port: Port number.
    :return: True if port is valid, False otherwide.
    :rtype: bool
    """
    if port < 2000 or port > 65535:
        return False
    return True
