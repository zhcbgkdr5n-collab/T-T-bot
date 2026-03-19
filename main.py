import requests
import time
import os
from flask import Flask
import threading

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

users = [
    "khaby.lame",
    "username2",
    "username3",
    "username4",
    "username5"
]

sent = set()

# --- WEB СЕРВЕР (АНТИСОН ДЛЯ RENDER) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- ОТПРАВКА СООБЩЕНИЯ ---
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except:
        pass

# --- ПРОВЕРКА ВИДЕО ---
def get_video(user):
    url = f"https://www.tiktok.com/@{user}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            if "video" in r.text:
                return f"https://www.tiktok.com/@{user}"
    except:
        return None

    return None

# --- ЗАПУСК СЕРВЕРА ---
threading.Thread(target=run_web).start()

# --- ОСНОВНОЙ ЦИКЛ ---
while True:
    for user in users:
        video = get_video(user)

        if video and video not in sent:
            send_message(f"🔥 Новое видео у @{user}")
            send_message(video)

            sent.add(video)

    time.sleep(60)