import os
import subprocess
import threading
import time
from app import create_app

app = create_app()

def run_crawler_periodically():
    while True:
        subprocess.call(["python", "./crawler/main.py"])
        time.sleep(180)

if __name__ == '__main__':
    # 只有在实际运行的子进程中启动定时任务线程
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=run_crawler_periodically, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
