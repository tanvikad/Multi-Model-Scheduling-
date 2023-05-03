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
model1_copy2 = MLModel("ResNet152 Copy1", 0.4305839539, 4.763916254, 11586)
model1_copy3 = MLModel("ResNet152 Copy2", 0.4305839539, 4.763916254, 11586)



SCHEDULE1 = [[0, 1, 0], [1, 0, 10], [2, 0, 20], [3, 1, 20], [4, 2, 20], [5, 3, 20]]
SCHEDULE2 = [[0, 1, 0], [1, 0, 0], [2, 0, 0], [3, 1, 0], [4, 2, 0], [5, 3, 0]]
THRASH_SCHEDULE = [[0, 0, 0], [1, 1, 0], [2, 0, 14], [3, 3, 7], [4, 3, 9], [5, 1, 2], [6, 3, 19], [7, 2, 10], [8, 2, 20], [9, 1, 19]] 

models = [model1, model2, model3, model4, model5]
large_models = [model1_copy, model1, model1_copy2, model1_copy3]
def get_random_schedule(num_tasks = 10, time_period = 20, models_used = models):
    schedule = []
    for i in range(num_tasks):
        random_model = random.randint(0, len(models_used)-1)
        random_arrival_time = random.randint(0, time_period)
        if(i == 0): random_arrival_time = 0
        task = [i, random_model, random_arrival_time]
        schedule += [task]
    return schedule


QUANTUM = 2

schedule = THRASH_SCHEDULE

RR_sim = RoundRobin(schedule, QUANTUM, evict_policy = Eviction.LRU)
FCFS_sim = FCFS(schedule)
SFS_sim = SFS(schedule)
SRTF_sim = SRTF(schedule,evict_policy=Eviction.MRU)
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



def get_eviction_policy_comparison(num_trials = 10000, models_used = large_models):

    num_times_MRU = 0
    avg_times_MRU_took= 0
    equal_time = 0
    for i in range(num_trials):
        random_schedule = get_random_schedule(models_used=large_models)
        RR_sim_LRU = RoundRobin(random_schedule, QUANTUM, evict_policy = Eviction.LRU)
        RR_sim_MRU = RoundRobin(random_schedule, QUANTUM, evict_policy = Eviction.MRU)

        for model in models_used:
            for simulation in [RR_sim_LRU, RR_sim_MRU]:
                simulation.add_model(model)

        RR_sim_LRU.run(100)
        RR_sim_MRU.run(100)

        LRU_time = RR_sim_LRU.get_time()
        MRU_time = RR_sim_MRU.get_time()
        if(MRU_time < LRU_time): 
            num_times_MRU +=1
        avg_times_MRU_took += ((LRU_time - MRU_time)/max(LRU_time,MRU_time))
        if(MRU_time == LRU_time):
            equal_time += 1
    
    return (num_times_MRU/num_trials)*100, (avg_times_MRU_took/num_trials)*100, (equal_time/num_trials)*100
print("Eviction Comparison", get_eviction_policy_comparison())


