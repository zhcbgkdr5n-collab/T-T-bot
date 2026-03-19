import requests
import time
import re

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

# 🔥 добавляй сюда аккаунты
users = [
    "khaby.lame",
    "therock",
    "zachking",
    "bellapoarch",
    "mrbeast"
]

sent = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except:
        pass

def get_videos(user):
    url = f"https://www.tiktok.com/@{user}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text

        ids = re.findall(r'"id":"(\d+)"', html)

        links = []
        for vid in ids[:5]:
            links.append(f"https://www.tiktok.com/@{user}/video/{vid}")

        return links
    except:
        return []

while True:
    for user in users:
        videos = get_videos(user)

        for video in videos:
            if video not in sent:
                send_message(f"🔥 @{user}\n{video}")
                sent.add(video)

        time.sleep(3)  # пауза между аккаунтами

    time.sleep(60)
