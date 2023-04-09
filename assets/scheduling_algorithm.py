from typing import List
from assets.Simulation import Simulation

class RoundRobin(Simulation):
    def __init__(self, schedule, quantum: int) -> None:
        super().__init__(schedule)
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
    def __init__(self, schedule) -> None:
        super().__init__(schedule)
    
    def run(self, queue: List) -> None:
        queue.sort(key = lambda x: x[2])
        for task_no, model_idx, arrival_time in queue:
            next = self.models[model_idx]
            if self.global_time <= arrival_time:
                self.global_time = arrival_time
                self.run_model(next, task_no)
            else:
                self.run_model(next, task_no)
            self.log_event(self.models[model_idx], "Done", task_no=task_no)
        self.print_events()

