import requests
import time
import re

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

users = ["khaby.lame"]

sent = set()

def send_video(url):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
        data={"chat_id": CHAT_ID, "video": url}
    )

def get_videos(user):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(f"https://www.tiktok.com/@{user}", headers=headers)
    
    links = re.findall(r'"playAddr":"(.*?)"', r.text)
    return [l.replace("\\u0026", "&") for l in links]

while True:
    for user in users:
        try:
            videos = get_videos(user)
            for v in videos[:2]:
                if v not in sent:
                    send_video(v)
                    sent.add(v)
        except:
            pass
    time.sleep(60)
