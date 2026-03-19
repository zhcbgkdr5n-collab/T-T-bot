import requests
import time
import os
from flask import Flask
from threading import Thread

BOT_TOKEN = "7683490408:AAFz36DxR5zbAwytbg0n6-74z1vZCbvyI1g"
CHAT_ID = "764321364"

users = ["khaby.lame"]

sent = set()

app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def run_bot():
    while True:
        for user in users:
            try:
                url = f"https://www.tiktok.com/@{user}"
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(url, headers=headers)

                if r.status_code == 200 and user not in sent:
                    send_message(f"🔥 Новое видео у @{user}")
                    send_message(url)
                    sent.add(user)

            except:
                pass

        time.sleep(60)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except:
        pass

if __name__ == "__main__":
    Thread(target=run_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)