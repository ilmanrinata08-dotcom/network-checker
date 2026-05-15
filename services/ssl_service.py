import ssl
import socket
import datetime
from utils.validator import validate_domain, clean_domain

def check_ssl(domain: str) -> dict:
    domain = clean_domain(domain)

    if not validate_domain(domain):
        return {
            "status": "error",
            "pesan" : "⚠️ Format domain tidak valid! Contoh: google.com"
        }

    try:
        ctx  = ssl.create_default_context()
        conn = ctx.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain
        )
        conn.settimeout(5)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        conn.close()

        expire_str  = cert["notAfter"]
        expire_date = datetime.datetime.strptime(
            expire_str, "%b %d %H:%M:%S %Y %Z"
        )
        now       = datetime.datetime.utcnow()
        days_left = (expire_date - now).days

        issuer_data = dict(x[0] for x in cert["issuer"])
        issuer      = issuer_data.get("organizationName", "Unknown")

        subject_data = dict(x[0] for x in cert["subject"])
        common_name  = subject_data.get("commonName", domain)

        if days_left > 60:
            grade = "A"
        elif days_left > 30:
            grade = "B"
        elif days_left > 0:
            grade = "C"
        else:
            grade = "F"

        return {
            "status"     : "valid",
            "domain"     : domain,
            "common_name": common_name,
            "issuer"     : issuer,
            "expire"     : expire_date.strftime("%d %B %Y"),
            "days_left"  : days_left,
            "grade"      : grade,
            "pesan"      : f"✅ SSL Valid! Sisa {days_left} hari"
        }

    except ssl.SSLCertVerificationError:
        return {"status": "invalid", "domain": domain,
                "pesan": "❌ SSL tidak valid atau self-signed!"}
    except socket.gaierror:
        return {"status": "error", "domain": domain,
                "pesan": "⚠️ Domain tidak ditemukan!"}
    except ConnectionRefusedError:
        return {"status": "error", "domain": domain,
                "pesan": "⚠️ Port 443 tidak terbuka!"}
    except Exception as e:
        return {"status": "error", "domain": domain,
                "pesan": f"⚠️ Error: {str(e)}"}
