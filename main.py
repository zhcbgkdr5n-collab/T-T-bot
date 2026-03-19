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
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log(f"load_data error: {e}")
    return {}

def save_data(data):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"save_data error: {e}")

last_videos = load_data()

def send_video(video_url, caption=""):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
            data={
                "chat_id": CHAT_ID,
                "video": video_url,
                "caption": caption[:1000]
            },
            timeout=60
        )
        log(f"send_video status: {r.status_code}, response: {r.text[:300]}")
        return r.status_code == 200
    except Exception as e:
        log(f"send_video error: {e}")
        return False

def get_latest_video(user):
    """
    Пытаемся получить последнее видео через tikwm.
    Если API не отдал id/play, вернём None.
    """
    profile_url = f"https://www.tiktok.com/@{user}"

    for attempt in range(3):
        try:
            r = requests.post(
                "https://tikwm.com/api/",
                data={"url": profile_url},
                timeout=25
            )
            log(f"{user} tikwm status: {r.status_code}")
            data = r.json()
            log(f"{user} tikwm response keys: {list(data.keys())}")

            if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
                item = data["data"]
                video_id = item.get("id")
                play_url = item.get("play")

                if video_id and play_url:
                    return video_id, play_url

        except Exception as e:
            log(f"{user} get_latest_video attempt {attempt+1} error: {e}")

        time.sleep(2)

    return None, None

def bot_loop():
    send_message("✅ Бот запущен и начал проверку аккаунтов")

    while True:
        try:
            for user in users:
                log(f"checking @{user}")
                video_id, video_url = get_latest_video(user)

                if not video_id or not video_url:
                    log(f"no video data for @{user}")
                    continue

                old_video_id = last_videos.get(user)

                if old_video_id != video_id:
                    log(f"new video for @{user}: {video_id}")
                    ok = send_video(video_url, caption=f"@{user}")

                    if ok:
                        last_videos[user] = video_id
                        save_data(last_videos)
                        log(f"saved new video id for @{user}: {video_id}")
                    else:
                        send_message(f"⚠️ Не удалось отправить видео от @{user}")

                else:
                    log(f"no new video for @{user}")

                time.sleep(2)

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            log(f"bot_loop fatal error: {e}")
            send_message(f"❌ Ошибка в цикле бота: {e}")
            time.sleep(5)

def run_bot():
    while True:
        try:
            bot_loop()
        except Exception as e:
            log(f"run_bot restart error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)