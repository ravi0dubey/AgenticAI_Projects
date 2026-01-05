import time
import winsound  # Only works on Windows

def beep_at_interval(interval, duration, repetitions):
    for _ in range(repetitions):
        winsound.Beep(1000, duration)  # Frequency 1000 Hz, duration in milliseconds
        time.sleep(interval)

if __name__ == "__main__":
    interval = float(input("Enter the interval between beeps (in seconds): "))
    duration = int(input("Enter the duration of each beep (in milliseconds): "))
    repetitions = int(input("Enter the number of beeps: "))

    beep_at_interval(interval, duration, repetitions)