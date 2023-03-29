from assets.scheduling_algorithm.Runner import RoundRobin
from assets.MLModel import MLModel

model1 = MLModel("model 1", 5, 2.5, 5000)
model2 = MLModel("model 2", 10, 2.5, 5000)
model3 = MLModel("model 3", 15, 5, 5000)
model4 = MLModel("model 4", 2, 1, 5000)

QUANTUM = 3
sim = RoundRobin(QUANTUM)
sim.add_model(model1)
sim.add_model(model2)
sim.add_model(model3)
sim.add_model(model4)

sim.run(100)
