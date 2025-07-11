# log_utils.py
import time

def log_status(status, log_file="log.csv"):
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write(f"{timestamp}, {status}\n")
    except Exception as e:
        print("Log yozishda xatolik:", e)