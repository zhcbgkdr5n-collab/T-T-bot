import requests
import time
from flask import Flask
import threading

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

# сюда вставляй до 5 аккаунтов
users = [
    "khaby.lame",
    "username2",
    "username3",
    "username4",
    "username5"
]

sent = set()

# --- WEB СЕРВЕР (АНТИСОН) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def run_web():
    app.run(host="0.0.0.0", port=10000)

# --- ОТПРАВКА СООБЩЕНИЯ ---
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# --- ОТПРАВКА ВИДЕО ---
def send_video(video_url):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    requests.post(url, data={"chat_id": CHAT_ID, "video": video_url})

# --- ПРОВЕРКА ВИДЕО ---
def get_video_link(user):
    url = f"https://www.tiktok.com/@{user}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            # простая проверка (можно улучшить позже)
            if "video" in r.text:
                return f"https://www.tiktok.com/@{user}"
    except:
        pass

    return None

# --- ЗАПУСК ВЕБ-СЕРВЕРА ---
threading.Thread(target=run_web).start()

# --- ОСНОВНОЙ ЦИКЛ ---
while True:
    for user in users:
        video = get_video_link(user)

        if video and video not in sent:
            send_message(f"🔥 Новое видео у @{user}")
            send_message(video)
            # если найдём прямую ссылку — будет отправлять как видео
            # send_video(video)

            sent.add(video)

    time.sleep(60)
