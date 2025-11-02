import requests
import csv
from datetime import datetime, timedelta

PROM_URL = "PROM_URL"
JOB_NAME = "JOB_NAME"
STEP = "15s"

# 対象IP
TARGET_IPS = [
    "192.168.X.X",
    "192.168.X.X",
    "192.168.X.X",
    "192.168.X.X"
]

# === 現在時刻を基準に「1分前の区間」を取得 ===
now = datetime.utcnow()
# 例: 17:00:00に実行 → start=16:59:00, end=17:00:00
end = now.replace(second=0, microsecond=0) - timedelta(seconds=1)
start = end - timedelta(minutes=1) + timedelta(seconds=1)

output_path = "./status_code_metrics.csv"

data_by_time = {}

for ip in TARGET_IPS:
    instance_url = f"http://{ip}/"
    query = f'probe_http_status_code{{job="{JOB_NAME}", instance="{instance_url}"}}'

    params = {
        "query": query,
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z",
        "step": STEP,  # ← 15秒ごと（00,15,30,45秒）
    }

    response = requests.get(PROM_URL, params=params).json()
    results = response.get("data", {}).get("result", [])

    for series in results:
        for timestamp, val in series["values"]:
            ts = datetime.utcfromtimestamp(float(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
            if ts not in data_by_time:
                data_by_time[ts] = {}
            data_by_time[ts][ip] = val

# 時間でソートして書き出し
sorted_times = sorted(data_by_time.keys())

with open(output_path, "a", newline="") as f:
    writer = csv.writer(f)
    # 新規ファイルならヘッダを書く
    if f.tell() == 0:
        writer.writerow(["timestamp"] + TARGET_IPS)

    for ts in sorted_times:
        row = [ts] + [data_by_time[ts].get(ip, "") for ip in TARGET_IPS]
        writer.writerow(row)

print(f"Metrics exported to {output_path}")
print(f"Time range: {start.strftime('%H:%M:%S')} ～ {end.strftime('%H:%M:%S')} (UTC)")
