import requests

def check_whois(ip: str) -> dict:
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = res.json()

        if data.get("status") == "success":
            return {
                "status" : "success",
                "ip"     : ip,
                "negara" : data.get("country", "-"),
                "kota"   : data.get("city", "-"),
                "isp"    : data.get("isp", "-"),
                "lat"    : data.get("lat", 0),
                "lon"    : data.get("lon", 0),
                "zona"   : data.get("timezone", "-")
            }
        else:
            return {"status": "error", "pesan": "⚠️ IP tidak ditemukan."}

    except Exception as e:
        return {"status": "error", "pesan": f"⚠️ Gagal koneksi: {str(e)}"}
