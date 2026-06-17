# Data Center Elasticity Simulation Project

Final Project — Pengembangan Pusat Komputasi Data

## Deskripsi Project

Project ini merupakan simulasi sederhana monitoring sumber daya dan elastisitas layanan pada data center menggunakan laptop sebagai environment utama.

Tujuan project:

* Memahami konsep **resource monitoring**
* Memahami konsep **elasticity (scale-out & scale-in)**
* Mengamati hubungan antara:

  * CPU usage
  * Memory usage
  * Latency
  * Throughput
  * Jumlah service instance

Project ini dibuat tanpa cloud, Docker, VM, atau tools berat seperti Kubernetes dan Grafana.

---

# Project Structure

```bash
dc-elasticity-project/
│
├── service.py
├── load_generator.py
├── monitor.py
├── requirements.txt
└── README.md
```

---

# Requirements

Install Python 3 terlebih dahulu.

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies:

* psutil
* requests

---

# Program Overview

## 1. service.py

Program ini mensimulasikan **service instance** pada data center.

Fungsi:

* Menjalankan HTTP server lokal
* Menerima request
* Melakukan komputasi sederhana untuk menaikkan CPU load

Contoh instance:

* Instance 1 → Port 8001
* Instance 2 → Port 8002
* Instance 3 → Port 8003

Menjalankan service:

```bash
python service.py 8001
```

Instance kedua:

```bash
python service.py 8002
```

---

## 2. load_generator.py

Program ini mensimulasikan beban pengguna dengan mengirim banyak request ke service.

Metrik yang dihitung:

* Total request
* Success request
* Failed request
* Average latency
* Throughput (request/sec)

Contoh:

1 instance:

```bash
python load_generator.py 8001
```

2 instance:

```bash
python load_generator.py 8001 8002
```

3 instance:

```bash
python load_generator.py 8001 8002 8003
```

---

## 3. monitor.py

Program monitoring resource laptop.

Metrik yang dicatat:

* Timestamp
* Elapsed time
* CPU usage (%)
* Memory usage (%)
* Jumlah service aktif

Output:

* Console monitoring
* File CSV untuk analisis dan grafik

Menjalankan:

```bash
python monitor.py
```

---

# Experiment Scenarios

## 1. Baseline

Menjalankan:

* 1 service instance

Tujuan:

* Mendapatkan performa awal sistem

Beban:

* Rendah
* Sedang
* Tinggi

Data yang dicatat:

* CPU usage
* Memory usage
* Latency
* Throughput
* Request success/fail

---

## 2. Scale-Out

Menambah jumlah service instance.

Contoh:

* 1 → 2 instance
* 2 → 3 instance

Tujuan:
Mengamati apakah:

* Latency menurun
* Throughput meningkat
* CPU usage berubah

---

## 3. Scale-In

Mengurangi jumlah instance ketika beban turun.

Contoh:

* 3 → 1 instance

Tujuan:
Mengamati apakah:

* CPU usage menurun
* Memory usage menurun

---

# Expected Output

Setelah eksperimen selesai, data digunakan untuk membuat:

## Tabel

Berisi:

* Laptop specs
* Jumlah instance
* CPU usage
* Memory usage
* Latency
* Throughput

## Grafik

Minimal 2 grafik:

1. CPU usage vs waktu / jumlah instance
2. Latency atau throughput sebelum dan sesudah scale-out

---

# Notes

* Project ini adalah simulasi skala kecil.
* Hasil scale-out tidak selalu lebih baik.
* Pada laptop dengan resource terbatas, penambahan instance dapat meningkatkan overhead dan memperburuk performa.

Konsep utama:

> Monitoring memberikan data kondisi sistem, sedangkan elastisitas adalah tindakan menambah atau mengurangi kapasitas berdasarkan data tersebut.
