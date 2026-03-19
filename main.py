import requests
import time
import re
from flask import Flask
import threading

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

users = [
    "khaby.lame",
    "therock",
    "zachking",
    "bellapoarch",
    "mrbeast"
]

sent = set()

# 🔥 Flask сервер (антисон)
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# 🔥 Telegram
def send_video(video_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "video": video_url
        })
    except:
        pass

def get_videos(user):
    url = f"https://www.tiktok.com/@{user}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text

        ids = re.findall(r'"id":"(\d+)"', html)

        return [f"https://www.tiktok.com/@{user}/video/{vid}" for vid in ids[:5]]
    except:
        return []

def get_no_watermark(video_url):
    try:
        api = f"https://tikwm.com/api/?url={video_url}"
        r = requests.get(api).json()
        return r["data"]["play"]
    except:
        return None

# 🔥 основной цикл
def bot_loop():
    while True:
        for user in users:
            videos = get_videos(user)

            for video in videos:
                if video not in sent:
                    no_wm = get_no_watermark(video)

                    if no_wm:
                        send_video(no_wm)
                        sent.add(video)

            time.sleep(3)

        time.sleep(60)

# 🔥 запуск всего
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot_loop()
