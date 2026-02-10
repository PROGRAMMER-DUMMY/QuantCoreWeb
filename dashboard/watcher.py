import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add parent dir to path so we can import config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.config import PATHS

class ChangeHandler(FileSystemEventHandler):
    """
    Listens for changes in the logs folder defined in PATHS.
    When a file changes, it 'touches' dashboard/trigger.py
    to force Streamlit to re-run.
    """

    def __init__(self, trigger_file):
        self.trigger_file = trigger_file
        self.last_trigger = 0

    def on_modified(self, event):
        if event.is_directory:
            return

        # Monitor CSVs (Sim results) and Logs (Live bot output)
        if event.src_path.endswith('.csv') or event.src_path.endswith('.log'):
            current_time = time.time()

            # Debounce: Prevent double-triggering (common with file writes)
            if current_time - self.last_trigger > 1.0:
                print(f"⚡ Change detected: {os.path.basename(event.src_path)}")

                # The Magic: Touch the trigger file to reload Streamlit
                with open(self.trigger_file, 'a'):
                    os.utime(self.trigger_file, None)

                self.last_trigger = current_time

def start_watching():
    # 1. Resolve Paths using Config
    LOGS_DIR = PATHS.logs_dir
    TRIGGER_FILE = os.path.join(PATHS.base_dir, 'dashboard', 'trigger.py')

    # Ensure trigger file exists
    if not os.path.exists(TRIGGER_FILE):
        with open(TRIGGER_FILE, 'w') as f:
            f.write("# Trigger file for Streamlit auto-reload")

    # 2. Setup Watchdog
    event_handler = ChangeHandler(TRIGGER_FILE)
    observer = Observer()
    observer.schedule(event_handler, LOGS_DIR, recursive=False)
    observer.start()

    print(f"Watchdog active. Monitoring: {LOGS_DIR}")
    print(f"Trigger Target: {TRIGGER_FILE}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watching()