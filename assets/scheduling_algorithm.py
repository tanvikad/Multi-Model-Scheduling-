from typing import List
from assets.Simulation import Simulation

class RoundRobin(Simulation):
    def __init__(self, quantum: int) -> None:
        super().__init__()
        self.quantum : int = quantum

    def run(self, run_time: float):
        i = 0
        q = 0
        num_model = len(self.models)
        print(self.models)
        while self.global_time < run_time:
            next = self.models[i]
            self.run_model(next)

            q += 1
            if q == self.quantum:
                i = (i + 1) % num_model
                q = 0
        
        self.print_events()

class FCFS(Simulation):
    """
    First Come First Serve schedule
    """
    def __init__(self) -> None:
        super().__init__()
    
    def run(self, queue: List) -> None:
        queue.sort(key = lambda x: x[1])
        for model_idx, arrival_time in queue:
            next = self.models[model_idx]
            if self.global_time <= arrival_time:
                self.global_time = arrival_time
                self.run_model(next)
            else:
                self.run_model(next)
        
        self.print_events()

