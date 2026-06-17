import psutil
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt

instance_count = int(input("Masukkan jumlah service instance aktif: "))
duration = int(input("Durasi monitoring (detik): "))

filename = f"monitor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
graph_name = f"monitor_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

times = []
cpu_data = []
memory_data = []

print("\nMonitoring dimulai...\n")

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "elapsed_time_sec",
        "cpu_usage_percent",
        "memory_usage_percent",
        "active_instances"
    ])

    start_time = time.time()

    for _ in range(duration):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        elapsed = round(time.time() - start_time, 2)

        times.append(elapsed)
        cpu_data.append(cpu)
        memory_data.append(memory)

        writer.writerow([elapsed, cpu, memory, instance_count])

        print(
            f"Time: {elapsed}s | "
            f"CPU: {cpu}% | "
            f"Memory: {memory}% | "
            f"Instances: {instance_count}"
        )

# Generate graph
plt.figure(figsize=(10, 5))
plt.plot(times, cpu_data, label="CPU Usage (%)")
plt.plot(times, memory_data, label="Memory Usage (%)")
plt.xlabel("Time (seconds)")
plt.ylabel("Usage (%)")
plt.title(f"Resource Monitoring ({instance_count} Instance)")
plt.legend()
plt.grid(True)
plt.savefig(graph_name)
plt.show()

print("\nMonitoring selesai.")
print(f"CSV tersimpan di: {filename}")
print(f"Grafik tersimpan di: {graph_name}")