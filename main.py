import requests
import time
import os
import json
import re
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
CHECK_INTERVAL = 120

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def log(text):
    print(text, flush=True)

def send_message(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text[:4000]},
            timeout=20
        )
    except Exception as e:
        log(f"send_message error: {e}")

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)

last_videos = load_data()

# --- отправка видео ---
def send_video(video_url, user):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
            data={
                "chat_id": CHAT_ID,
                "video": video_url,
                "caption": f"🔥 @{user}"
            },
            timeout=60
        )
        log(f"send_video: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        log(f"send_video error: {e}")
        return False

# --- новый парсер ---
def get_latest_video(user):
    try:
        url = f"https://www.tiktok.com/@{user}"
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            return None, None

        text = r.text

        ids = re.findall(r'"id":"(\d+)"', text)

        if not ids:
            return None, None

        video_id = ids[0]

        api = "https://tikwm.com/api/"
        res = requests.post(api, data={
            "url": f"https://www.tiktok.com/@{user}/video/{video_id}"
        }, timeout=15)

        data = res.json()

        if "data" in data:
            return video_id, data["data"]["play"]

    except Exception as e:
        log(f"парсинг ошибка: {e}")

    return None, None

# --- основной цикл ---
def bot_loop():
    send_message("🚀 Бот запущен")

    while True:
        try:
            for user in users:
                log(f"checking @{user}")

                video_id, video_url = get_latest_video(user)

                if not video_id:
                    log(f"нет видео у @{user}")
                    continue

                if last_videos.get(user) != video_id:
                    log(f"новое видео у @{user}")

                    ok = send_video(video_url, user)

                    if ok:
                        last_videos[user] = video_id
                        save_data(last_videos)
                        log("сохранили")
                    else:
                        send_message(f"❌ ошибка отправки @{user}")

                else:
                    log(f"без изменений @{user}")

                time.sleep(2)

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            log(f"ошибка цикла: {e}")
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