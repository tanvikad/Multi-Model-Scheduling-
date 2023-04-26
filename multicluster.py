from ./
from assets.LoadBalancer import LoadBalancer
from assets.MLModel import MLModel
import numpy as np
import random

random.seed(42)

NETWORK_DELAY = 0

model1 = MLModel("ResNet152", 0.4305839539 + NETWORK_DELAY, 4.763916254, 11586)
model2 = MLModel("ResNet50", 0.03879141808 + NETWORK_DELAY, 2.226957321, 5474)
model3 = MLModel("VGG16", 0.03628611565 + NETWORK_DELAY, 4.252752304, 9540)
model4 = MLModel("VGG19", 0.03628611565 + NETWORK_DELAY, 4.252752304, 5708)
model5 = MLModel("Resnet18", 0.000928401947 + NETWORK_DELAY, 1.959828854, 1508)

models = [model1, model2, model3, model4]

def get_random_schedule(num_tasks = 10, time_period = 30):
    schedule = []
    models = [model1, model2, model3, model4]
    for i in range(num_tasks):
        random_model = random.randint(0, len(models)-1)
        random_arrival_time = random.uniform(0, time_period)
        task = [i, random_model, random_arrival_time]
        schedule += [task]
    return schedule

schedule = get_random_schedule(200, 3)
MAX_CLUSTER = 8
file = open("multicluster.txt", "w")
file.write(str(MAX_CLUSTER) + "\n")
for num_cluster in range(1, MAX_CLUSTER + 1):
    server = LoadBalancer(models, schedule.copy(), num_cluster)
    server.run_basic() 
    file.write(str(len(server.cluster_list)) + "\n")
    file.write("Memory Based approach" + "\n")
    for clus in server.cluster_list:
        file.write(str(clus.global_time) + "\n")
        # print(clus.get_stats())

    server1 = LoadBalancer(models, schedule.copy(), num_cluster)
    server1.run_greedy() 
    file.write("Greedy approach" + "\n")
    for clus in server1.cluster_list:
        file.write(str(clus.global_time) + "\n")
        # print(clus.get_stats())

    server2 = LoadBalancer(models, schedule.copy(), num_cluster)
    server2.run_random() 
    file.write("Random approach" + "\n")
    for clus in server2.cluster_list:
        file.write(str(clus.global_time) + "\n")
        # print(clus.get_stats())

file.close()