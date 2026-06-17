import psutil
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt

instance_count = int(input("Masukkan jumlah service instance aktif: "))

timestamp_now = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_filename = f"monitor_log_{timestamp_now}.csv"
graph_filename = f"monitor_graph_{timestamp_now}.png"

times = []
cpu_data = []
memory_data = []

print("\nMonitoring dimulai...")
print("Tekan Ctrl + C untuk berhenti.\n")

start_time = time.time()

try:
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        elapsed = round(time.time() - start_time, 2)

        times.append(elapsed)
        cpu_data.append(cpu)
        memory_data.append(memory)

        print(
            f"Time: {elapsed}s | "
            f"CPU: {cpu}% | "
            f"Memory: {memory}% | "
            f"Instances: {instance_count}"
        )

except KeyboardInterrupt:
    print("\nMonitoring dihentikan.")

    # Simpan CSV
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "elapsed_time_sec",
            "cpu_usage_percent",
            "memory_usage_percent",
            "active_instances"
        ])

        for i in range(len(times)):
            writer.writerow([
                times[i],
                cpu_data[i],
                memory_data[i],
                instance_count
            ])

    # Generate grafik
    plt.figure(figsize=(10, 5))
    plt.plot(times, cpu_data, label="CPU Usage (%)")
    plt.plot(times, memory_data, label="Memory Usage (%)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Usage (%)")
    plt.title(f"Resource Monitoring ({instance_count} Instance)")
    plt.legend()
    plt.grid(True)
    plt.savefig(graph_filename)
    plt.show()

    print(f"CSV tersimpan: {csv_filename}")
    print(f"Grafik tersimpan: {graph_filename}")