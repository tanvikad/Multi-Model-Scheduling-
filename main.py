from assets.scheduling_algorithm import RoundRobin, FCFS, SFS, SRTF, HRRF
from assets.MLModel import MLModel
from assets.MemoryManager import Eviction 
import random


model1 = MLModel("ResNet152", 0.4305839539, 4.763916254, 11586)
model2 = MLModel("ResNet50", 0.03879141808, 2.226957321, 5474)
model3 = MLModel("VGG16", 0.03628611565, 4.252752304, 9540)
model4 = MLModel("VGG19", 0.03628611565, 4.252752304, 5708)
model5 = MLModel("Resnet18", 0.000928401947, 1.959828854, 1508)
model1_copy = MLModel("ResNet152 Copy", 0.4305839539, 4.763916254, 11586)


SCHEDULE1 = [[0, 1, 0], [1, 0, 10], [2, 0, 20], [3, 1, 20], [4, 2, 20], [5, 3, 20]]
SCHEDULE2 = [[0, 1, 0], [1, 0, 0], [2, 0, 0], [3, 1, 0], [4, 2, 0], [5, 3, 0]]
SCHEDULE3 = [[0, 0, 0], [1, 0, 10], [2, 4, 21], [3, 4, 29], [4, 5, 18], [5, 5, 23], [6, 0, 16], [7, 5, 10], [8, 4, 5], [9, 3, 2]]     


models = [model1, model2, model3, model4, model5]
def get_random_schedule(num_tasks = 10, time_period = 20):
    schedule = []
    for i in range(num_tasks):
        random_model = random.randint(0, len(models)-1)
        random_arrival_time = random.randint(0, time_period)
        if(i == 0): random_arrival_time = 0
        task = [i, random_model, random_arrival_time]
        schedule += [task]
    print(schedule)
    return schedule


QUANTUM = 2

schedule = SCHEDULE2

RR_sim = RoundRobin(schedule, QUANTUM, evict_policy = Eviction.LRU)
FCFS_sim = FCFS(schedule)
SFS_sim = SFS(schedule)
SRTF_sim = SRTF(schedule,evict_policy=Eviction.LRU)
HRRF_sim = HRRF(schedule)
for model in models:
    for simulation in [RR_sim, FCFS_sim, SFS_sim, SRTF_sim, HRRF_sim]:
        simulation.add_model(model)

# Change this line to change which model you want to run
sim = RR_sim

sim.run(100)
sim.print_events()
sim.get_stats()
sim.gantt_chart()
