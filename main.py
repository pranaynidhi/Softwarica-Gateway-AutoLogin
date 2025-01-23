import requests

headers = {
    'Host': 'gateway.example.com',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36',
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
print(f"VlanID Retrived: {valn_ID}")
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
