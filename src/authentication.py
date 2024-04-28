import requests
import json
import re
import random
import string

def generate_android_id():
    # Generate random Android ID
    random_id = ''.join(random.choice(string.hexdigits) for _ in range(16))
    return 'android-' + random_id

headers = {
    'user-agent': 'Instagram 329.0.0.0.58 Android (25/7.1.2; 320dpi; 900x1600; samsung; SM-G965N; star2lte; samsungexynos9810; en_US; 541635897)',
}

data = {
    'params': json.dumps({
        "client_input_params": {
            "password": "", # Password encrypted with passowrd.py
            "contact_point": "", # Must be a valid username value
            "device_id": generate_android_id(), # Android ID
        },
        "server_params": {
            "credential_type": "password",
        }
    }, indent=4),
    'bloks_versioning_id': '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a',
}

def get_login_data(proxy):
    proxies = {"http": proxy, "https": proxy} if proxy != "no_proxy" else None
    response = requests.post(
        'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',
        headers=headers,
        data=data,
        proxies=proxies,
    )
    if 'Please wait a few minutes before you try again' in response.text:
        print('Instagram error: Please wait a few minutes before you try again.')
        exit(1)
    return response



def process_response_for_all(response):
    data_str = json.dumps(response.json())
    result = {}

    # Find pk_id
    matches_pk = re.findall(r'(pk_id.{40})', data_str)
    for match in matches_pk:
        cleaned_match = match.replace('\\', '')
        result["pk_id"] = cleaned_match[8:-2]
        break  # Return after first match

    if "pk_id" not in result:
        print("Could not log in. Check your credentials and try again.")
        exit(1)

    # Find IG-Set-Authorization
    matches_auth = re.findall(r'(IG-Set-Authorization.{0,350}?)",', data_str)
    for match in matches_auth:
        cleaned_match = match.replace('\\', '')
        result["IG-Set-Authorization"] = cleaned_match[24:]
        break  # Return after first match

    # Find uuid
    matches_uuid = re.findall(r'(uuid.{0,250}?)",', data_str)
    for match in matches_uuid:
        cleaned_match = match.replace('\\', '')
        result["uuid"] = cleaned_match[8:-2]
        break  # Return after first match

    return [result]

def check_proxy_ip(proxy):
    expected_ip = proxy.split('@')[1].split(':')[0]
    try:
        response = requests.get('https://api.ipify.org?format=json', proxies={"http": proxy, "https": proxy}, timeout=5)
        returned_ip = response.json()['ip']
        if returned_ip == expected_ip:
            print("IP matches the expected IP.")
            return True
        else:
            print("IP does not match the expected IP.")
            return False
    except Exception as e:
        print(f"Error checking proxy IP: {e}")
        return False