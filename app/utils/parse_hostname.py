def parse_hostname(server_addr: str) -> tuple:
    parsed = urlsplit("//" + server_addr)
    return parsed.hostname, parsed.port
