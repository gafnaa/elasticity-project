import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_file = "summary.csv"

df = pd.read_csv(csv_file)

mapping = {
    "hasil-1": "Laptop 1",
    "hasil-2": "Laptop 2"
}

df["Laptop"] = (
    df["Laptop"]
    .astype(str)
    .str.split("\\")
    .str[-1]
    .replace(mapping)
)

# Grafik 1
cpu_data = (
    df.groupby(["Laptop", "Scenario"])["CPU Avg (%)"]
      .mean()
      .unstack()
)

plt.figure(figsize=(6,4))

cpu_data.T.plot(kind="bar")

plt.ylabel("CPU Average (%)")
plt.xlabel("Scenario")
plt.title("Average CPU Usage Comparison")
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "cpu_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# Grafik 2
throughput_data = (
    df.groupby("Workload")["Throughput (req/s)"]
      .mean()
)

order = [
    "beban rendah",
    "beban sedang",
    "beban tinggi"
]

throughput_data = throughput_data.reindex(order)

plt.figure(figsize=(6,4))

plt.plot(
    throughput_data.index,
    throughput_data.values,
    marker="o"
)

plt.ylabel("Throughput (req/s)")
plt.xlabel("Workload")
plt.title("Throughput by Workload")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "throughput_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Graphs generated successfully.")