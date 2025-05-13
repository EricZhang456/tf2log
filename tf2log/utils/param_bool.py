"""Boolean parameter in a URL parameter."""

def param_bool(value: str):
    """Parses a boolean parameter in a URL parameter.
    
    :param str value: Value of the URL parameter.
    :return: True if the URL parameter evaluates to true, False otherwise.
    :rtype: bool
    """
    return bool(value.isnumeric() and int(value) >= 1)
