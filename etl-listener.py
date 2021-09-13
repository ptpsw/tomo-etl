import sys
import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from dotenv import load_dotenv

load_dotenv()

class PatternEvent(PatternMatchingEventHandler):
    def on_created(self, event):
        notify_telegram(event)

def notify_telegram(msg):
    url = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage'
    payload = {'chat_id': {os.getenv("TELEGRAM_CHAT_ID")}, 'text': msg}
    r = requests.post(url, data=payload)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = PatternEvent(patterns=["*_SDE.csv", "*_SDR.csv"])
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()