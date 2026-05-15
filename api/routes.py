from flask import request, jsonify
from collections import defaultdict
import time
from config import Config
from api import api_bp
from services.ping_service import check_ping
from services.scan_service import check_scan
from services.whois_service import check_whois
from services.ssl_service import check_ssl

request_log = defaultdict(list)

def rate_limit(ip_client: str) -> bool:
    now = time.time()
    request_log[ip_client] = [
        t for t in request_log[ip_client]
        if now - t < Config.RATE_WINDOW
    ]
    if len(request_log[ip_client]) >= Config.RATE_LIMIT:
        return False
    request_log[ip_client].append(now)
    return True

@api_bp.route("/cek", methods=["POST"])
def cek_ip():
    if not rate_limit(request.remote_addr):
        return jsonify({"status":"error","pesan":"⚠️ Terlalu banyak request!"})
    ip = request.json.get("ip","").strip()
    if not ip:
        return jsonify({"status":"error","pesan":"⚠️ IP tidak boleh kosong!"})
    return jsonify(check_ping(ip))

@api_bp.route("/scan", methods=["POST"])
def scan_port():
    if not rate_limit(request.remote_addr):
        return jsonify({"status":"error","pesan":"⚠️ Terlalu banyak request!"})
    data  = request.json
    ip    = data.get("ip","").strip()
    ports = data.get("ports",[])
    return jsonify(check_scan(ip, ports))

@api_bp.route("/whois", methods=["POST"])
def whois_ip():
    if not rate_limit(request.remote_addr):
        return jsonify({"status":"error","pesan":"⚠️ Terlalu banyak request!"})
    ip = request.json.get("ip","").strip()
    if not ip:
        return jsonify({"status":"error","pesan":"⚠️ IP tidak boleh kosong!"})
    return jsonify(check_whois(ip))

@api_bp.route("/ssl", methods=["POST"])
def ssl_check():
    if not rate_limit(request.remote_addr):
        return jsonify({"status":"error","pesan":"⚠️ Terlalu banyak request!"})
    domain = request.json.get("domain","").strip()
    if not domain:
        return jsonify({"status":"error","pesan":"⚠️ Domain tidak boleh kosong!"})
    return jsonify(check_ssl(domain))
