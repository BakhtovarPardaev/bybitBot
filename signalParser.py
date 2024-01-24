import re
import csv
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVHandler(FileSystemEventHandler):

    def __init__(self, timeout=1):
        super().__init__()
        self.timeout = timeout
        self.last_modified = 0

    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('.csv') and time.time() - self.last_modified > self.timeout:
            self.last_modified = time.time()
            print(f"File {event.src_path} has been modified")
            process_csv(event.src_path)

def process_csv(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not exist.")
        return

    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        input_text = '\n'.join(','.join(row) for row in csv_reader)

    match_symbol = re.search(r'#(\w+)', input_text)
    match_direction = re.search(r'Направление:\s*(\w+)', input_text)
    match_take = re.findall(r'(\d+\.\d+)', input_text)

    instrum = match_symbol.group(1) if match_symbol else None
    direction = match_direction.group(1) if match_direction else None
    take_values = match_take if match_take else []

    if instrum and direction and take_values:
        print(instrum)
        print(direction)
        for i, value in enumerate(take_values, 1):
            print(f"{i}) {value}")
    else:
        print("Не удалось извлечь инф")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(CSVHandler(), path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()