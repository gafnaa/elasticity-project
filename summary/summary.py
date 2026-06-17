import pandas as pd
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOTS = [
    BASE_DIR / "hasil-1",
    BASE_DIR / "hasil-2"
]

results = []

for laptop in ROOTS:

    for scenario in ["baseline", "scale-in", "scale-out"]:

        scenario_path = Path(laptop) / scenario

        if not scenario_path.exists():
            continue

        for workload in scenario_path.iterdir():

            if not workload.is_dir():
                continue

            csv_files = list(workload.glob("*.csv"))
            log_files = list(workload.glob("*.txt"))

            if not csv_files:
                continue

            # =====================
            # CSV
            # =====================
            df = pd.read_csv(csv_files[0])

            cpu_avg = df["cpu_usage_percent"].mean()
            cpu_max = df["cpu_usage_percent"].max()

            mem_avg = df["memory_usage_percent"].mean()
            mem_max = df["memory_usage_percent"].max()

            active_instances = df["active_instances"].max()

            total_request = None
            success = None
            failed = None
            latency = None
            throughput = None

            if log_files:

                text = log_files[0].read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                patterns = {
                    "total_request":
                        r"Total Request\s*:\s*(\d+)",

                    "success":
                        r"Request Berhasil\s*:\s*(\d+)",

                    "failed":
                        r"Request Gagal\s*:\s*(\d+)",

                    "latency":
                        r"Average Latency\s*:\s*([\d.]+)",

                    "throughput":
                        r"Throughput\s*:\s*([\d.]+)"
                }

                for key, pattern in patterns.items():

                    m = re.search(pattern, text)

                    if m:
                        value = m.group(1)

                        if key in [
                            "total_request",
                            "success",
                            "failed"
                        ]:
                            value = int(value)
                        else:
                            value = float(value)

                        locals()[key] = value

            results.append({
                "Laptop": laptop,
                "Scenario": scenario,
                "Workload": workload.name,

                "Instances": active_instances,

                "CPU Avg (%)": round(cpu_avg, 2),
                "CPU Max (%)": round(cpu_max, 2),

                "Mem Avg (%)": round(mem_avg, 2),
                "Mem Max (%)": round(mem_max, 2),

                "Total Request": total_request,
                "Success": success,
                "Failed": failed,

                "Latency (s)": latency,
                "Throughput (req/s)": throughput
            })

summary = pd.DataFrame(results)

summary.to_csv(
    "summary.csv",
    index=False
)

print(summary)