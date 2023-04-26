import matplotlib.pyplot as plt
import numpy as np

KEYS = ["memory runtime", "greedy runtime", "random runtime"]
LINES = ["cluster 1", "cluster 2"]

file = open("twoCluster.txt")
file.readline()
data = {key: () for key in LINES}
print(data)
num_cluster = int(file.readline())
for _ in KEYS:
    file.readline()
    for key in LINES:
        x = file.readline()
        print(x, key)
        data[key] = data[key] + (float(x), )

number_cluster = np.arange(len(KEYS))
x = np.arange(len(KEYS))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
print(data)
fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Model Type')
ax.set_ylabel('Completion Time (s)')
ax.set_title('Completion Time Over Number of Clusters')
ax.set_xticks(x + width, KEYS)
ax.legend(loc='upper right')
# ax.set_ylim(0, 900)

plt.show()

