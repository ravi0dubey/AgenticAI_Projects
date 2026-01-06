import time
import os
import platform

INTERVAL_SECONDS = 5   # change this (e.g., 4 sec inhale, 6 sec exhale)

def beep():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 600)  # frequency, duration(ms)
    else:
        os.system("printf '\a'")  # Linux / Mac beep

print("Breathing timer started. Press Ctrl+C to stop.")

try:
    while True:
        beep()
        time.sleep(INTERVAL_SECONDS)
except KeyboardInterrupt:
    print("\nTimer stopped.")