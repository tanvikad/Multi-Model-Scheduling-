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
    def run_next(self, active_pool: List, next_arrival_time: float):
        next = active_pool.pop(0)
        model, task = self.models[next[1]], next[3]
        self.run_model(model, next[0], task)
        self.log_event(self.models[next[1]], "Done", next[0])


class SFS(Simulation):
    """
    Shortest job first
    """
    def run_next(self, active_pool: List, next_arrival_time: float):
        active_pool.sort(key = lambda x: x[3])
        next = active_pool.pop(0)
        model, task = self.models[next[1]], next[3]
        self.run_model(model, next[0], task)
        self.log_event(self.models[next[1]], "Done", next[0])


class SRTF(Simulation):
    """
    Shortest Remaining Time first
    """
    def run_next(self, active_pool: List, next_arrival_time: float):
        active_pool.sort(key = lambda x: x[3])
        next = active_pool.pop(0)
        model, task = self.models[next[1]], next[3]

        step = min(task, next_arrival_time)
        self.run_model(model, next[0], step)

        next[3] -= step
        if next[3] > 0:
            active_pool.append(next)
        else:
            self.log_event(self.models[next[1]], "Done", next[0])

# elements in active_pool: [task_num, model_num, arrival_time, burst_time]
class HRRF(Simulation):
    """
    Highest Response Ratio (waiting time + burst time)/burst time first
    """
    def run_next(self, active_pool: List, next_arrival_time: float):
        active_pool.sort(key = lambda x: (self.global_time - x[3]) / x[3], reverse=True)
        next = active_pool.pop(0)
        model, task = self.models[next[1]], next[3]
        self.run_model(model, next[0], task)
        self.log_event(self.models[next[1]], "Done", next[0])