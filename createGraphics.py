# import required libraries for memory stats, plotting, and timing
# here i use psutil to get the values in a more simple way, since
# the subprocess lib works fine but i chose psutil for simplicity here after running the
#console commands on the memoryTestConsole
import psutil
import matplotlib.pyplot as plt
import time
from collections import deque

# create a fixed-size queue to store the last 5 memory percentage readings
history = deque([0.0] * 5, maxlen=5)

# turn on interactive mode for live plotting
plt.ion()

# set up the figure and axis with dark theme colors
fig, ax = plt.subplots(figsize=(7, 4), facecolor="#0a0a0a")
ax.set_facecolor("#0a0a0a")

# color the borders dark grey
for spine in ax.spines.values():
    spine.set_color("#222")


# define the function to generate the dashboard
def generateDash():
    # loop runs until it is forced to stop
    # begin the continuous update loop
    while True:
        # fetch current ram percentage and append it to our queue
        history.append(psutil.virtual_memory().percent)
        data = list(history)

        # clear the plot for the new frame
        ax.clear()

        # reapply the dark background and border colors after clearing
        ax.set_facecolor("#0a0a0a")
        for spine in ax.spines.values():
            spine.set_color("#222")

        # set up colors: green for past data, blue for the current reading
        colors = ["#00cc66"] * 4 + ["#00aaff"]
        ax.bar(range(5), data, color=colors, width=0.6)

        # configure the y-axis to scale from 0 to 100 percent
        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 25))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)}%"))

        # configure the x-axis labels to show relative time
        ax.set_xticks(range(5))
        ax.set_xticklabels(["-4s", "-3s", "-2s", "-1s", "now"], color="#aaa")

        # style the axis ticks and draw background grid lines
        ax.tick_params(colors="#aaa")
        ax.yaxis.grid(True, color="#1a1a1a", linewidth=0.8)
        ax.set_axisbelow(True)

        # grab full virtual memory statistics for the dynamic title
        vm = psutil.virtual_memory()
        ax.set_title(
            f"RAM  {vm.percent:.1f}%   used {vm.used / 1e9:.1f}GB / {vm.total / 1e9:.1f}GB   free {vm.available / 1e9:.1f}GB",
            color="#00aaff", fontsize=10, fontfamily="monospace", loc="left", pad=10
        )

        # draw the updated canvas and process gui events
        fig.canvas.draw()
        fig.canvas.flush_events()

        # wait one second before repeating
        time.sleep(1)