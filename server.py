import socket
import os
import re
import time
from collections import defaultdict
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# ══════════════════════════════════════
#  RATE LIMITER
#  Logika: Maksimal 5 request per 10 detik
#  Cegah DDoS lokal dari teman usil
# ══════════════════════════════════════
request_log = defaultdict(list)

def rate_limit(ip_client):
    sekarang = time.time()
    request_log[ip_client] = [
        t for t in request_log[ip_client]
        if sekarang - t < 10
    ]
    if len(request_log[ip_client]) >= 5:
        return False
    request_log[ip_client].append(sekarang)
    return True

# ══════════════════════════════════════
#  VALIDASI FORMAT IP
#  Logika: Cegah Command Injection
#  Hanya terima format X.X.X.X
# ══════════════════════════════════════
def validasi_ip(ip):
    pola = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if not re.match(pola, ip):
        return False
    for angka in ip.split("."):
        if int(angka) > 255:
            return False
    return True

# ══════════════════════════════════════
#  BATASI IP YANG BOLEH DI-SCAN
#  Logika: Cegah Scanner di dalam Scanner
#  Hanya izinkan IP lokal
# ══════════════════════════════════════
def ip_diizinkan(ip):
    boleh = ["127.", "192.168.", "10.", "172."]
    for prefix in boleh:
        if ip.startswith(prefix):
            return True
    return False

# ══════════════════════════════════════
#  KIRIM index.html
# ══════════════════════════════════════
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# ══════════════════════════════════════
#  PING CHECKER
# ══════════════════════════════════════
@app.route("/cek", methods=["POST"])
def cek_ip():

    # Cek rate limit dulu
    ip_client = request.remote_addr
    if not rate_limit(ip_client):
        return jsonify({
            "status": "error",
            "pesan" : "⚠️ Terlalu banyak request! Tunggu 10 detik."
        })

    try:
        data = request.json
        ip   = data.get("ip", "").strip()

        if not ip:
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ IP tidak boleh kosong!"
            })

        # Validasi → cegah command injection
        if not validasi_ip(ip):
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ Format IP tidak valid!"
            })

        hasil = os.system(
            f"ping -c 1 -W 2 {ip} > /dev/null 2>&1"
        )

        if hasil == 0:
            return jsonify({
                "status": "online",
                "pesan" : f"🟢 {ip} → ONLINE! Perangkat aktif."
            })
        else:
            return jsonify({
                "status": "offline",
                "pesan" : f"🔴 {ip} → OFFLINE! Tidak ada respon."
            })

    except Exception as e:
        print(f"[ERROR PING] {e}")
        return jsonify({
            "status": "error",
            "pesan" : "⚠️ Gangguan teknis. Coba lagi nanti."
        })

# ══════════════════════════════════════
#  PORT SCANNER
# ══════════════════════════════════════
@app.route("/scan", methods=["POST"])
def scan_port():

    # Cek rate limit
    ip_client = request.remote_addr
    if not rate_limit(ip_client):
        return jsonify({
            "status": "error",
            "pesan" : "⚠️ Terlalu banyak request! Tunggu 10 detik."
        })

    try:
        data  = request.json
        ip    = data.get("ip", "").strip()
        ports = data.get("ports", [])

        # Validasi IP
        if not ip or not validasi_ip(ip):
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ Format IP tidak valid!"
            })

        # Cegah scan IP publik
        if not ip_diizinkan(ip):
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ Hanya boleh scan IP lokal!"
            })

        # Validasi ports
        if not ports:
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ Masukkan minimal 1 port!"
            })

        # Batasi maksimal 20 port sekali scan
        if len(ports) > 20:
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ Maksimal 20 port per scan!"
            })

        hasil_scan = []

        for port in ports:
            try:
                s = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )
                s.settimeout(1)
                result = s.connect_ex((ip, int(port)))
                s.close()

                if result == 0:
                    hasil_scan.append({
                        "port"  : port,
                        "status": "open",
                        "pesan" : f"Port {port} OPEN"
                    })
                else:
                    hasil_scan.append({
                        "port"  : port,
                        "status": "closed",
                        "pesan" : f"Port {port} CLOSED"
                    })

            except Exception as e:
                print(f"[ERROR PORT {port}] {e}")
                hasil_scan.append({
                    "port"  : port,
                    "status": "error",
                    "pesan" : f"Port {port} ERROR"
                })

        return jsonify({
            "status": "selesai",
            "hasil" : hasil_scan
        })

    except Exception as e:
        print(f"[ERROR SCAN] {e}")
        return jsonify({
            "status": "error",
            "pesan" : "⚠️ Gangguan teknis. Coba lagi nanti."
        })

# ══════════════════════════════════════
#  JALANKAN SERVER
# ══════════════════════════════════════
if __name__ == "__main__":
    print("=" * 40)
    print("  🌐 Server aktif di localhost:8000")
    print("  📱 Buka Chrome → ketik localhost:8000")
    print("=" * 40)
    app.run(host="0.0.0.0", port=8000, debug=True)
