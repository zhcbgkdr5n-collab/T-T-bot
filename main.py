import requests
import time
import os
from flask import Flask
from threading import Thread

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

# 🔥 активные, но не супер-миллионники
users = [
    "lifehackdailyy",
    "brainfood.ig",
    "satisfyingclipss",
    "dailyyfacts",
    "wowthingss",
    "oddlysatisfying.video"
]

sent = set()

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

# --- отправка видео ---
def send_video(video_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "video": video_url
        })
    except:
        pass

# --- получение видео без водяного знака ---
def get_video(user):
    try:
        tiktok_url = f"https://www.tiktok.com/@{user}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(tiktok_url, headers=headers)

        if r.status_code != 200:
            return None

        api = "https://tikwm.com/api/"
        res = requests.post(api, data={"url": tiktok_url})

        data = res.json()

        if "data" in data and "play" in data["data"]:
            return data["data"]["play"]

    except:
        return None

    return None

# --- бот ---
def run_bot():
    while True:
        for user in users:
            video = get_video(user)

            if video and video not in sent:
                send_video(video)
                sent.add(video)

        time.sleep(120)

if __name__ == "__main__":
    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)