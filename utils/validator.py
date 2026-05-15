import re
from config import Config

def validate_ip(ip: str) -> bool:
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if not re.match(pattern, ip):
        return False
    for part in ip.split("."):
        if int(part) > 255:
            return False
    return True

def is_ip_allowed(ip: str) -> bool:
    return any(ip.startswith(p) for p in Config.ALLOWED_PREFIXES)

def validate_ports(ports: list) -> tuple[bool, str]:
    if not ports:
        return False, "Minimal 1 port!"
    if len(ports) > Config.MAX_PORTS:
        return False, f"Maksimal {Config.MAX_PORTS} port!"
    for p in ports:
        try:
            if not (1 <= int(p) <= 65535):
                return False, f"Port {p} tidak valid!"
        except:
            return False, f"Port {p} bukan angka!"
    return True, "ok"

def validate_domain(domain: str) -> bool:
    domain = domain.replace("https://","").replace("http://","").split("/")[0]
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))

def clean_domain(domain: str) -> str:
    domain = domain.replace("https://","").replace("http://","")
    domain = domain.split("/")[0]
    domain = domain.split(":")[0]
    return domain.strip().lower()
