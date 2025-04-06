import time
import sys

def progress_bar(duration):
    for i in range(duration):
        percent = (i + 1) / duration * 100
        bar = "#" * int(percent / 2) + "-" * (50 - int(percent / 2))
        sys.stdout.write(f"\r[{bar}] {percent:.1f}%")
        sys.stdout.flush()
        time.sleep(1)
