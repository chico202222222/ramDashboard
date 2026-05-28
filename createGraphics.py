import psutil
import matplotlib.pyplot as plt
import time
import json
import os
from datetime import datetime
from collections import deque

HISTORY_FILE = "history.json"

# Load existing history or start fresh
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except:
        return []

# Append a timestamped RAM reading to history.json
def save_reading(ram_percent):
    records = load_history()
    records.append({
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "ram_percent": ram_percent
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(records, f, indent=2)

history = deque([0.0] * 5, maxlen=5)

plt.ion()
fig, ax = plt.subplots(figsize=(7, 4), facecolor="#0a0a0a")
ax.set_facecolor("#0a0a0a")
for spine in ax.spines.values():
    spine.set_color("#222")

def generateDash():
    while True:
        vm = psutil.virtual_memory()
        history.append(vm.percent)
        save_reading(vm.percent)  # save timestamp + ram_percent to history.json

        ax.clear()
        ax.set_facecolor("#0a0a0a")
        for spine in ax.spines.values():
            spine.set_color("#222")

        ax.bar(range(5), list(history), color=["#00cc66"] * 4 + ["#00aaff"], width=0.6)
        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 25))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)}%"))
        ax.set_xticks(range(5))
        ax.set_xticklabels(["-4s", "-3s", "-2s", "-1s", "now"], color="#aaa")
        ax.tick_params(colors="#aaa")
        ax.yaxis.grid(True, color="#1a1a1a", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_title(
            f"RAM {vm.percent:.1f}% used {vm.used/1e9:.1f}GB / {vm.total/1e9:.1f}GB free {vm.available/1e9:.1f}GB",
            color="#00aaff", fontsize=10, fontfamily="monospace", loc="left", pad=10
        )
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1)