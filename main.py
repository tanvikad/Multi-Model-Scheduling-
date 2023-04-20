from assets.scheduling_algorithm import RoundRobin, FCFS, SFS, SRTF
from assets.MLModel import MLModel

model1 = MLModel("model 0", 5, 2.5, 5000)
model2 = MLModel("model 1", 10, 2.5, 5000)
model3 = MLModel("model 2", 15, 5, 5000)
model4 = MLModel("model 3", 2, 1, 5000)

schedule = [[0, 1, 0], [1, 0, 10], [2, 0, 20], [3, 1, 20], [4, 2, 20], [5, 3, 20]]
QUANTUM = 2
RR_sim = RoundRobin(schedule, QUANTUM)
FCFS_sim = FCFS(schedule)
SFS_sim = SFS(schedule)
SRTF_sim = SRTF(schedule)
for model in [model1, model2, model3, model4]:
    for simulation in [RR_sim, FCFS_sim, SFS_sim, SRTF_sim]:
        simulation.add_model(model)

# Change this line to change which model you want to run
sim = SRTF_sim

sim.run(100)
sim.print_events()
sim.gantt_chart()
