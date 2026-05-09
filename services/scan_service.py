from utils.network_tools import scan_port
from utils.validator import validate_ip, is_ip_allowed, validate_ports

def check_scan(ip: str, ports: list) -> dict:
    if not validate_ip(ip):
        return {"status": "error", "pesan": "⚠️ Format IP tidak valid!"}

    if not is_ip_allowed(ip):
        return {"status": "error", "pesan": "⚠️ Hanya boleh scan IP lokal!"}

    valid, pesan = validate_ports(ports)
    if not valid:
        return {"status": "error", "pesan": f"⚠️ {pesan}"}

    hasil = []
    for port in ports:
        hasil.append(scan_port(ip, port))

    return {"status": "selesai", "hasil": hasil}
