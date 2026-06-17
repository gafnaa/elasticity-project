import psutil
import time
import csv
from datetime import datetime

# Input dari user
instance_count = int(input("Masukkan jumlah service instance aktif: "))
duration = int(input("Durasi monitoring (detik): "))

filename = f"monitor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print(f"\nMonitoring dimulai...")
print(f"Data akan disimpan ke: {filename}\n")

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Header CSV
    writer.writerow([
        "timestamp",
        "elapsed_time_sec",
        "cpu_usage_percent",
        "memory_usage_percent",
        "active_instances"
    ])

    start_time = time.time()

    for second in range(duration):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        timestamp = datetime.now().strftime("%H:%M:%S")
        elapsed = round(time.time() - start_time, 2)

        writer.writerow([
            timestamp,
            elapsed,
            cpu,
            memory,
            instance_count
        ])

        print(
            f"[{timestamp}] "
            f"CPU: {cpu}% | "
            f"Memory: {memory}% | "
            f"Instances: {instance_count}"
        )

print("\nMonitoring selesai.")
print(f"Log tersimpan di file: {filename}")