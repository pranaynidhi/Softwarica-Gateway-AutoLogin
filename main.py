import subprocess
import re
import requests
import time

def get_strongest_stwcu_ssid():
    # Rescan for Wi-Fi networks
    subprocess.run(['nmcli', 'device', 'wifi', 'rescan'], capture_output=True)
    time.sleep(2)

    # Get SSID:SIGNAL list for easier parsing
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SIGNAL', 'device', 'wifi', 'list'],
                            capture_output=True, text=True)

    lines = result.stdout.strip().split('\n')
    ssid_signal = {}

    for line in lines:
        if not line.strip():
            continue
        try:
            ssid, signal = line.rsplit(':', 1)
            signal = int(signal.strip())
            if ssid.strip().startswith('STWCU'):
                ssid_signal[ssid.strip()] = signal
        except ValueError:
            continue

    if not ssid_signal:
        print("No STWCU networks found.")
        return None

    best_ssid = max(ssid_signal, key=ssid_signal.get)
    print(f"✅ Best STWCU SSID: {best_ssid} ({ssid_signal[best_ssid]}% signal)")
    return best_ssid

def connect_to_wifi(ssid):
    # Try to connect to the SSID using NetworkManager
    result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Connected to {ssid}")
        return True
    else:
        print(f"Failed to connect to {ssid}: {result.stderr}")
        return False

# Connect to strongest STWCU network
ssid = get_strongest_stwcu_ssid()
if ssid and connect_to_wifi(ssid):
    # Proceed with the original login process
    headers = {
        'Host': 'gateway.example.com',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i',
        'Connection': 'keep-alive',
    }

    response = requests.get('https://gateway.example.com/loginpages/', headers=headers, verify=False)
    valn_ID = response.text.split("var vlan_id = '")[1].split("'")[0]
    print(f"VlanID Retrieved: {valn_ID}")
    Session_cookie = response.cookies.get("Session")
    print(f"Session Cookies: {Session_cookie}")

    cookies = {
        'Session': Session_cookie,
    }

    data = {
        'username': 'softwarica',
        'password': 'coventry2019',
        'accesscode': '',
        'vlan_id': valn_ID,
    }

    response = requests.post(
        'https://gateway.example.com/loginpages/userlogin.shtml',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    print("Logged in!")
else:
    print("Could not connect to Wi-Fi or no matching SSID found.")

