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

TIME = 3
FPS = 30
FREQUENCY = 5

def get_random_schedule(num_tasks = 10, time_period = 30):
    schedule = []
    models = [model1, model2, model3, model4]
    for i in range(num_tasks):
        random_model = random.randint(0, len(models)-1)
        random_arrival_time = random.randint(0, time_period)
        task = [i, random_model, random_arrival_time]
        schedule += [task]
    print(schedule)
    return schedule


def get_schedule(time):
    schedule = []
    task = 0
    temp = 1
    for arrival_time in np.linspace(0, TIME, FPS * TIME + 1):
        if temp % FREQUENCY == 0: 
            schedule.append([task, 1, arrival_time])
        else:
            schedule.append([task, 0, arrival_time])
        temp = (temp + 1) % FREQUENCY
        task += 1
    
    return schedule

schedule = get_random_schedule(200, 15)
server = LoadBalancer(models, schedule.copy())
server.run_basic() 
print("Server 1 information")
for clus in server.cluster_list:
    print(clus.global_time)
    print(clus.get_stats())


schedule = get_schedule(2)
server1 = LoadBalancer(models, schedule.copy())
server1.run_greedy() 
print("Server 2 information")
for clus in server1.cluster_list:
    print(clus.global_time)
    print(clus.get_stats())
