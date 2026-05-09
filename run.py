import os
from flask import Flask, send_from_directory
from config import Config
from api import api_bp

app = Flask(__name__,
    template_folder="templates",
    static_folder="static"
)

app.register_blueprint(api_bp)

@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route("/favicon.ico")
def favicon():
    return "", 204

if __name__ == "__main__":
    os.system("clear")
    os.system("toilet -f pagga --metal 'CYBER LAB'")
    print(" 📡 STATUS : ONLINE  |  🛠️  MODE: SECURE")
    print("—" * 45)
    print(f"  🌐 Server aktif di localhost:{Config.PORT}")
    print(f"  ⚡ Rate Limit: {Config.RATE_LIMIT} request / {Config.RATE_WINDOW} detik")
    print("—" * 45)
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
