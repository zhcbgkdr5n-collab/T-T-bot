import requests
import time
import os
import json
from flask import Flask
from threading import Thread

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

users = [
    "lifehackdailyy",
    "brainfood.ig",
    "satisfyingclipss",
    "dailyyfacts",
    "wowthingss"
]

FILE_NAME = "videos.json"

# --- загрузка памяти ---
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        last_videos = json.load(f)
else:
    last_videos = {}

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

# --- сохранить память ---
def save_data():
    with open(FILE_NAME, "w") as f:
        json.dump(last_videos, f)

# --- отправка видео ---
def send_video(video_url):
    try:
        video = requests.get(video_url, stream=True, timeout=20)
        if video.status_code == 200:
            files = {"video": video.raw}
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
                data={"chat_id": CHAT_ID},
                files=files,
                timeout=20
            )
    except:
        pass

# --- получить видео ---
def get_latest_video(user):
    for _ in range(3):
        try:
            api = "https://tikwm.com/api/"
            url = f"https://www.tiktok.com/@{user}"

            res = requests.post(api, data={"url": url}, timeout=15)
            data = res.json()

            if "data" in data:
                return data["data"]["id"], data["data"]["play"]

        except:
            time.sleep(2)

    return None, None

# --- основной цикл ---
def bot_loop():
    while True:
        try:
            for user in users:
                video_id, video_url = get_latest_video(user)

                if video_id:
                    if user not in last_videos or last_videos[user] != video_id:
                        send_video(video_url)
                        last_videos[user] = video_id
                        save_data()

                time.sleep(2)

            time.sleep(60)

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)

# --- запуск ---
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