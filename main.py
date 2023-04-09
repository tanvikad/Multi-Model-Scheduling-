from assets.scheduling_algorithm import RoundRobin, FCFS
from assets.MLModel import MLModel

model1 = MLModel("model 1", 5, 2.5, 5000)
model2 = MLModel("model 2", 10, 2.5, 5000)
model3 = MLModel("model 3", 15, 5, 5000)
model4 = MLModel("model 4", 2, 1, 5000)

QUANTUM = 3
sim = RoundRobin([], QUANTUM)
for model in [model1, model2, model3, model4]:
    sim.add_model(model)
# eviction MRR
# sim.run(100)


schedule = [[0, 1, 0], [1, 0, 10], [2, 0, 20], [3, 1, 20], [4, 2, 20], [5, 3, 20]]
sim2 = FCFS(schedule)
for model in [model1, model2, model3, model4]:
    sim2.add_model(model)
sim2.run(schedule)
sim2.get_stats()