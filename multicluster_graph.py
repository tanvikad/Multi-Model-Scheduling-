import matplotlib.pyplot as plt
import numpy as np



NUM_RUN = 8
KEYS = ["memory runtime", "greedy runtime", "random runtime"]


file = open("multicluster.txt")
file.readline()
data = {key: () for key in KEYS}

for _ in range(NUM_RUN):
    num_cluster = int(file.readline())
    for key in KEYS:
        file.readline()
        max_time = 0
        for _ in range(num_cluster):
            max_time = max(max_time, float(file.readline()))
        data[key] = data[key] + (max_time, )


# Build the graph
number_cluster = list(range(1, NUM_RUN + 1))
x = np.arange(len(number_cluster))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Number of Clusters')
ax.set_ylabel('Completion Time (s)')
ax.set_title('Completion Time Over Number of Clusters')
ax.set_xticks(x + width, number_cluster)
ax.legend(loc='upper right')
# ax.set_ylim(0, 900)

plt.show()

