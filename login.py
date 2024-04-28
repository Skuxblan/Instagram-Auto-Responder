from src.password import PasswordMixin
from src import authentication
import json
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
ensure_dir('accounts')
ensure_dir('responded_users')

while True:
    use_proxy = input("Use proxy? (yes/no): ")
    if use_proxy.lower() == "yes":
        proxy_input = input("Proxy input in ip:port:username:password format: ")
        ip, port, username, password = proxy_input.split(":")
        proxy = f"http://{username}:{password}@{ip}:{port}"
        if not authentication.check_proxy_ip(proxy):
            print("Proxy IP check failed.")
            exit(1)
        break
    elif use_proxy.lower() == "no":
        proxy = "no_proxy"
        break
    else:
        print("Incorrect input.")

username = input("Instagram username: ")
password_input = input("Instagram password: ")

mixin = PasswordMixin()
publickeyid, publickey = mixin.password_publickeys(proxy)
encrypted_password = mixin.password_encrypt(password_input, publickeyid, publickey)

device_id = authentication.generate_android_id()

authentication.headers['user-agent'] = 'Instagram 329.0.0.0.58 Android (25/7.1.2; 320dpi; 900x1600; samsung; SM-G965N; star2lte; samsungexynos9810; en_US; 541635897)'
authentication.data['params'] = json.dumps({
    "client_input_params": {
        "password": encrypted_password,
        "contact_point": username,
        "device_id": device_id,
    },
    "server_params": {
        "credential_type": "password",
    }
}, indent=4)
authentication.data['bloks_versioning_id'] = '9fc6a7a4a577456e492c189810755fe22a6300efc23e4532268bca150fe3e27a'

response = authentication.get_login_data(proxy)
cleaned_match_auth_and_uuid = authentication.process_response_for_all(response)

# Add device_id and proxy to session data
cleaned_match_auth_and_uuid[0]['device_id'] = device_id
cleaned_match_auth_and_uuid[0]['proxy'] = proxy

session_data = {
    "account": username,
    "data": cleaned_match_auth_and_uuid[0],
    "num_replies": 5, # Sample value to be changed in config file
    "messages": ["Message 1", "Message 2", "Message 3"], # Sample value to be changed in config file
}

with open(f'accounts/{username}_session.json', 'w', encoding='utf-8') as f:
    json.dump(session_data, f, ensure_ascii=False, indent=4)
    print(f"Session saved in accounts folder. File name: {username}_session.json")