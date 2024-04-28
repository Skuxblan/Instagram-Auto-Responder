import requests
import json
import uuid
import time
import random
import datetime

class InstagramDirect:
    def __init__(self, account_data):
        self.account_data = account_data
        self.headers = {
            'user-agent': 'Instagram 329.0.0.0.58 Android (25/7.1.2; 320dpi; 900x1600; samsung; SM-G965N; star2lte; samsungexynos9810; en_US; 541635897)',
            'authorization': self.account_data['data']['IG-Set-Authorization'],
        }
        self.data = {
            'device_id': self.account_data['data']['device_id'],
            '_uuid': self.account_data['data']['uuid'],
        }
        self.proxy = self.account_data['data']['proxy']

    def get_direct_threads(self):
        params = {
            'visual_message_return_type': 'unseen',
            'persistentBadging': 'true',
            'limit': '20',
            'is_prefetching': 'false',
            'selected_filter': 'unread',
        }

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy != "no_proxy" else None
        response = requests.get('https://i.instagram.com/api/v1/direct_v2/inbox/', params=params, headers=self.headers, proxies=proxies)
        time.sleep(random.randint(3, 10))
        if response.status_code != 200:
            raise Exception(f'Failed to get direct threads: {response.text}')
        
        data = json.loads(response.text)

        if not data['inbox']['threads']:
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Could not find any unread threads.")
            return []

        user_ids = [(thread['thread_id'], thread['users'][0]['pk_id'], thread['users'][0]['username']) for thread in data['inbox']['threads']]

        return user_ids[:self.account_data['num_replies']]

    def get_direct_threads_spam(self):
        params = {
            'visual_message_return_type': 'unseen',
            'persistentBadging': 'true',
            'limit': '20',
            'is_prefetching': 'false',
        }

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy != "no_proxy" else None
        response = requests.get('https://i.instagram.com/api/v1/direct_v2/pending_inbox/', params=params, headers=self.headers, proxies=proxies)
        time.sleep(random.randint(3, 10))
        if response.status_code != 200:
            raise Exception(f'Failed to get direct threads spam: {response.text}')
        
        data = json.loads(response.text)

        if not data['inbox']['threads']:
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Could not find any unread threads in the spam inbox.")
            return []

        user_ids = [(thread['thread_id'], thread['users'][0]['pk_id'], thread['users'][0]['username']) for thread in data['inbox']['threads']]

        return user_ids[:self.account_data['num_replies']]


    def send_message(self, thread_id, message):
        client_context = str(uuid.uuid4()).replace('-', '')
        data = self.data.copy()
        data.update({
            'action': 'send_item',
            'is_x_transport_forward': 'false',
            'is_shh_mode': '0',
            'send_silently': 'false',
            'thread_ids': f'[{thread_id}]',
            'send_attribution': 'direct_thread',
            'client_context': client_context,
            'text': message,
            'mutation_token': client_context,
            'btt_dual_send': 'false',
            "nav_chain": (
                "1qT:feed_timeline:1,1qT:feed_timeline:2,1qT:feed_timeline:3,"
                "7Az:direct_inbox:4,7Az:direct_inbox:5,5rG:direct_thread:7"
            ),
            'is_ae_dual_send': 'false',
            'offline_threading_id': client_context,
        })

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy != "no_proxy" else None
        response = requests.post('https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/', headers=self.headers, data=data, proxies=proxies)
        time.sleep(random.randint(3, 10))
        if response.status_code != 200:
            raise Exception(f'Failed to send message: {response.text}')

    def test_proxy(self):
        if self.proxy == "no_proxy":
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: No proxy is being used.")
            return

        proxies = {"http": self.proxy, "https": self.proxy}
        response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
        proxy_ip = self.proxy.split('@')[1].split(':')[0]
        if response.json()['ip'] != proxy_ip:
            print(f"Expected Proxy IP: {proxy_ip}")
            print(f"Actual Proxy IP: {response.json()['ip']}")
            raise Exception(f'Proxy IP does not match: {response.text}')
        else:
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Proxy IP matches.")
