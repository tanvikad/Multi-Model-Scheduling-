from typing import List
from assets.Simulation import Simulation

class RoundRobin(Simulation):
    def __init__(self, schedule, quantum: int) -> None:
        super().__init__(schedule)
        self.quantum : int = quantum

    def run_next(self, active_pool: List, next_arrival_time: float):
        next = active_pool.pop(0)
        model, task = self.models[next[1]], next[3]
        
        # Find the step size of the run.
        time_run = min(task, self.quantum)
        self.run_model(model, next[0], time_run)

        # update the job and put it back into the queue if needed
        next[3] -= time_run
        if next[3] > 0:
            active_pool.append(next)
        else:
            self.log_event(self.models[next[1]], "Done", next[0])

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

