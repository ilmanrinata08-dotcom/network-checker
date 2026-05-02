import os
import re
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# ══════════════════════════════════════
#  LAYER 1: Validasi Format IP
# ══════════════════════════════════════
def validasi_ip(ip):
    pola = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if not re.match(pola, ip):
        return False
    bagian = ip.split(".")
    for angka in bagian:
        if int(angka) > 255:
            return False
    return True

# ══════════════════════════════════════
#  LAYER 2: Jalankan Ping
# ══════════════════════════════════════
def jalankan_ping(ip):
    try:
        hasil = os.system(f"ping -c 1 -W 2 {ip} > /dev/null 2>&1")
        if hasil == 0:
            return "online"
        else:
            return "offline"
    except Exception as e:
        print(f"[ERROR PING] Ada masalah: {e}")
        return "error"

# ══════════════════════════════════════
#  LAYER 3: Kirim File index.html
# ══════════════════════════════════════
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# ══════════════════════════════════════
#  LAYER 4: Endpoint Cek IP
# ══════════════════════════════════════
@app.route("/cek", methods=["POST"])
def cek_ip():
    try:
        data = request.json
        ip   = data.get("ip", "").strip()

        # Cek kosong
        if not ip:
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ IP tidak boleh kosong!"
            })

        # Cek format IP
        if not validasi_ip(ip):
            return jsonify({
                "status": "error",
                "pesan" : "⚠️ Format IP tidak valid! Contoh: 192.168.1.1"
            })

        # Jalankan ping
        hasil = jalankan_ping(ip)

        if hasil == "online":
            pesan = f"🟢 {ip} → ONLINE! Perangkat aktif."
        elif hasil == "offline":
            pesan = f"🔴 {ip} → OFFLINE! Tidak ada respon."
        else:
            pesan = "⚠️ Maaf, sedang ada gangguan teknis. Coba lagi nanti."

        return jsonify({"status": hasil, "pesan": pesan})

    except Exception as e:
        print(f"[ERROR SISTEM] {e}")
        return jsonify({
            "status": "error",
            "pesan" : "⚠️ Maaf, sedang ada gangguan teknis. Coba lagi nanti."
        })

# ══════════════════════════════════════
#  Jalankan Server di Port 8000
# ══════════════════════════════════════
if __name__ == "__main__":
    print("=" * 40)
    print("  🌐 Server aktif di localhost:8000")
    print("  📱 Buka Chrome → ketik localhost:8000")
    print("=" * 40)
    app.run(host="0.0.0.0", port=8000, debug=True)
