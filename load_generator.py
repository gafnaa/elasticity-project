import requests
import threading
import time

# Input konfigurasi
ports_input = input("Masukkan port aktif (pisahkan dengan koma, contoh 8001,8002): ")
ports = [int(p.strip()) for p in ports_input.split(",")]

TOTAL_REQUEST = int(input("Jumlah total request: "))
THREAD_COUNT = int(input("Jumlah thread/concurrent request: "))

success = 0
failed = 0
latencies = []
request_counter = 0
lock = threading.Lock()


def worker():
    global success, failed, request_counter

    while True:
        with lock:
            if request_counter >= TOTAL_REQUEST:
                return
            request_counter += 1
            current_request = request_counter

        # Round-robin port selection
        port = ports[current_request % len(ports)]
        url = f"http://localhost:{port}"

        start = time.time()

        try:
            response = requests.get(url, timeout=10)
            latency = time.time() - start

            with lock:
                if response.status_code == 200:
                    success += 1
                    latencies.append(latency)
                else:
                    failed += 1

        except Exception:
            with lock:
                failed += 1


print("\nLoad testing dimulai...\n")

threads = []
start_time = time.time()

for _ in range(THREAD_COUNT):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end_time = time.time()
total_time = end_time - start_time

avg_latency = sum(latencies) / len(latencies) if latencies else 0
throughput = success / total_time if total_time > 0 else 0

print("\n===== HASIL LOAD TEST =====")
print(f"Total Request      : {TOTAL_REQUEST}")
print(f"Request Berhasil   : {success}")
print(f"Request Gagal      : {failed}")
print(f"Average Latency    : {avg_latency:.4f} sec")
print(f"Throughput         : {throughput:.2f} req/sec")
print(f"Total Waktu Test   : {total_time:.2f} sec")