import os
import requests

def enable_vpn(proxy_host="68.71.249.158", proxy_port="4145"):
    proxy_url = f"socks5h://{proxy_host}:{proxy_port}"
    os.environ["HTTP_PROXY"] = proxy_url
    os.environ["HTTPS_PROXY"] = proxy_url
    print(f"VPN enabled: {proxy_url}")


def disable_vpn():
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    print("VPN disabled")


def send_request():
    try:
        response = requests.get("https://httpbin.org/ip", timeout=30)
        print("Current IP:", response.json())
    except requests.RequestException as e:
        print(f"Request failed: {e}")


send_request()
enable_vpn()
send_request()
disable_vpn()
send_request()

