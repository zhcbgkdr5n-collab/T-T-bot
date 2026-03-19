import requests
import time
import os
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

last_videos = {}

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

# --- отправка видео файлом ---
def send_video_file(video_url):
    try:
        video = requests.get(video_url, stream=True, timeout=20)

        if video.status_code == 200:
            files = {"video": video.raw}
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
                data={"chat_id": CHAT_ID},
                files=files
            )
    except:
        pass

# --- получаем последнее видео ---
def get_latest_video(user):
    try:
        api = "https://tikwm.com/api/"
        url = f"https://www.tiktok.com/@{user}"

        res = requests.post(api, data={"url": url})
        data = res.json()

        if "data" in data:
            video_url = data["data"]["play"]
            video_id = data["data"]["id"]

            return video_id, video_url

    except:
        return None, None

    return None, None

# --- основной бот ---
def run_bot():
    while True:
        for user in users:
            video_id, video_url = get_latest_video(user)

            if video_id:
                if user not in last_videos or last_videos[user] != video_id:
                    send_video_file(video_url)
                    last_videos[user] = video_id

        time.sleep(120)

if __name__ == "__main__":
    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)