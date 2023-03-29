# Multi-Model-Scheduling-

This folder contains the simulation code for loading and running models on the GPU. 

## assets 

File name  | purpose/contain
------------- | -------------
\_\_init__.py | Makes the file a module 
MLModel.py       | Contains the class definition of a model. Every model pass into the simulation should be of this type.
MemoryManager.py | Contains the logic and parameter of the GPU model. Use this class to manage GPU memory. 
Simulation.py | Contains the logic of the simulation. Every simulation will have a memoryManager and models. 
Scheduling_algoirthm.py | This class contains the different type of scheduling algoirthm. The scheduling algoirthm should inherit from Simulation and implement the abstract method run(run_time: float).
