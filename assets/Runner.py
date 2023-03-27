from assets.Simulation import Simulation

class RoundRobin(Simulation):
    def __init__(self, quantum: int) -> None:
        super().__init__()
        self.quantum : int = quantum

    def run(self, run_time: float):
        i = 0
        num_model = len(self.models)
        print(self.models)
        while self.global_time < run_time:
            next = self.models[i]
            self.run_model(next)
            i = (i + 1) % num_model
        
        for line in self.logger:
            print(line)



