from utils.network_tools import ping
from utils.validator import validate_ip

def check_ping(ip: str) -> dict:
    if not validate_ip(ip):
        return {"status": "error", "pesan": "⚠️ Format IP tidak valid!"}

    hasil = ping(ip)

    if hasil == "online":
        return {"status": "online", "pesan": f"🟢 {ip} → ONLINE! Perangkat aktif."}
    elif hasil == "offline":
        return {"status": "offline", "pesan": f"🔴 {ip} → OFFLINE! Tidak ada respon."}
    else:
        return {"status": "error", "pesan": "⚠️ Gangguan teknis. Coba lagi."}
