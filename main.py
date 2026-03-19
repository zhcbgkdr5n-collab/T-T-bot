import requests
import time

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

users = ["khaby.lame"]

sent = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_videos(user):
    url = f"https://www.tiktok.com/@{user}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            if "video" in r.text:
                return True
    except:
        pass
    return False

while True:
    for user in users:
        if user not in sent:
            if get_videos(user):
                send_message(f"🔥 Новое видео у @{user}\nhttps://www.tiktok.com/@{user}")
                sent.add(user)
    time.sleep(60)
