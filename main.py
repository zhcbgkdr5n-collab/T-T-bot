import requests
import time
import os
import json
import re
from flask import Flask
from threading import Thread

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"

# ✅ ТВОЙ CHAT_ID УЖЕ ВСТАВЛЕН
CHAT_ID = "-1003764176456"

users = [
    "lifehackdailyy",
    "brainfood.ig",
    "satisfyingclipss",
    "dailyyfacts",
    "wowthingss"
]

FILE_NAME = "videos.json"
CHECK_INTERVAL = 120

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)

last_videos = load_data()

# --- отправка ссылки в группу ---
def send_link(video_url):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": video_url
            },
            timeout=20
        )
    except:
        pass

# --- получение последнего видео ---
def get_latest_video(user):
    try:
        url = f"https://www.tiktok.com/@{user}"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
        }

        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            return None

        text = r.text
        ids = re.findall(r'"id":"(\d+)"', text)

        if not ids:
            return None

        return ids[0]

    except:
        return None

# --- основной цикл ---
def bot_loop():
    while True:
        try:
            for user in users:
                video_id = get_latest_video(user)

                if not video_id:
                    continue

                if last_videos.get(user) != video_id:
                    video_url = f"https://www.tiktok.com/@{user}/video/{video_id}"

                    send_link(video_url)

                    last_videos[user] = video_id
                    save_data(last_videos)

                time.sleep(2)

            time.sleep(CHECK_INTERVAL)

        except:
            time.sleep(5)

def run_bot():
    while True:
        try:
            bot_loop()
        except:
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)