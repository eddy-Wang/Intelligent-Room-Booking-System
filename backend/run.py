import os
import subprocess
import threading
import time
from app import create_app

app = create_app()


def run_crawler_periodically():
    while True:
        subprocess.run(["python", os.path.join("crawler", "main.py")])
        time.sleep(3600)


if __name__ == '__main__':
    # only run crawler in the subprocess that is actually running
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=run_crawler_periodically, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
