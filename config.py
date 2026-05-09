import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT         = int(os.getenv("FLASK_PORT", 8000))
    DEBUG        = os.getenv("FLASK_DEBUG", "True") == "True"
    RATE_LIMIT   = int(os.getenv("RATE_LIMIT", 5))
    RATE_WINDOW  = int(os.getenv("RATE_WINDOW", 10))
    MAX_PORTS    = int(os.getenv("MAX_PORTS", 20))

    ALLOWED_PREFIXES = ["127.", "192.168.", "10.", "172."]
    COMMON_PORTS     = [21, 22, 23, 53, 80, 443, 3306, 8080, 8291]
