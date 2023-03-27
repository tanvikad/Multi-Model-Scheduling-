from assets.Runner import RoundRobin
from assets.MLModel import MLModel

model1 = MLModel("model 1", 5, 2.5, 500)
model2 = MLModel("model 2", 10, 2.5, 500)
model3 = MLModel("model 3", 15, 5, 500)
model4 = MLModel("model 4", 2, 1, 500)

sim = RoundRobin(1)
sim.add_model(model1)
sim.add_model(model2)
sim.add_model(model3)
sim.add_model(model4)

sim.run(100)
