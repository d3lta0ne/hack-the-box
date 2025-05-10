import re

def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def validate_ip(ip):
    pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    return re.match(pattern, ip) is not None

def validate_port(port):
    return port.isdigit() and 0 < int(port) <= 65535
