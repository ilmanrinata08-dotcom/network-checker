import os
import socket

def ping(ip: str) -> str:
    try:
        result = os.system(f"ping -c 1 -W 2 {ip} > /dev/null 2>&1")
        return "online" if result == 0 else "offline"
    except Exception as e:
        print(f"[PING ERROR] {e}")
        return "error"

def scan_port(ip: str, port: int) -> dict:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, int(port)))
        s.close()
        status = "open" if result == 0 else "closed"
        return {"port": port, "status": status}
    except Exception as e:
        return {"port": port, "status": "error", "detail": str(e)}
