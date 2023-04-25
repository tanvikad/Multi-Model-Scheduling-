from assets.scheduling_algorithm import RoundRobin, FCFS, SFS, SRTF
from assets.MLModel import MLModel
from assets.MemoryManager import Eviction
import matplotlib.pyplot as plt
import numpy as np

QUANTUM = .1
HARDWARE_SPEED_UP = 1
FREQUENCY = 3
TIME = 3

fps = list(range(1,45, 3))
wait_time = {}
finish_time = {}
load = {}


for FPS in fps:
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

    model1 = MLModel("ResNet18", 0.000928401947, 1.959828854/HARDWARE_SPEED_UP, 1508)
    model2 = MLModel("ResNet50", 3, 2.226957321/HARDWARE_SPEED_UP, 5474)
    schedule = get_schedule(3)

    RR_sim = RoundRobin(schedule, QUANTUM)
    FCFS_sim = FCFS(schedule)
    SFS_sim = SFS(schedule)
    SRTF_sim = SRTF(schedule)
    for model in [model1, model2]:
        for simulation in [RR_sim, FCFS_sim, SFS_sim, SRTF_sim]:
            simulation.add_model(model)

    # Change this line to change which model you want to run
    for idx, sim in enumerate([RR_sim, FCFS_sim, SFS_sim, SRTF_sim]):
        sim.run(100)
        if idx not in wait_time:
            wait_time[idx] = []
            finish_time[idx] = []
            load[idx] = []
             
        wait_time[idx].append(sim.get_average_wait_time())
        finish_time[idx].append(sim.global_time)
        load[idx].append(sim.get_number_loads())
        # sim.print_events()
        # sim.get_stats()
        # sim.gantt_chart()


plt.plot(fps, load[0])
plt.plot(fps, load[1])
plt.plot(fps, load[2])
plt.plot(fps, load[3])
plt.show()
