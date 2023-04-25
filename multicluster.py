from assets.LoadBalancer import LoadBalancer
from assets.MLModel import MLModel
import numpy as np
import random


model1 = MLModel("ResNet152", 0.4305839539, 4.763916254, 11586)
model2 = MLModel("ResNet50", 0.03879141808, 2.226957321, 5474)
model3 = MLModel("VGG16", 0.03628611565, 4.252752304, 9540)
model4 = MLModel("VGG19", 0.03628611565, 4.252752304, 5708)
model5 = MLModel("Resnet18", 0.000928401947, 1.959828854, 1508)

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

schedule = get_random_schedule(300, 15)
server = LoadBalancer(models, schedule.copy())
server.run_basic() 
print(len(server.cluster_list))
print("Memory Based approach")
for clus in server.cluster_list:
    print(clus.global_time)
    # print(clus.get_stats())

server1 = LoadBalancer(models, schedule.copy())
server1.run_greedy() 
print("Greedy approach")
for clus in server1.cluster_list:
    print(clus.global_time)
    # print(clus.get_stats())

server2 = LoadBalancer(models, schedule.copy())
server2.run_random() 
print("Random approach")
for clus in server2.cluster_list:
    print(clus.global_time)
    # print(clus.get_stats())
