from abc import abstractmethod
from assets.MLModel import MLModel
from assets.MemoryManger import MemoryManger
from typing import List

class Simulation:
    def __init__(self) -> None:
        self.global_time : float = 0
        self.models : List[MLModel] = []
        self.memory_manger : MemoryManger = MemoryManger()
        # for logging
        self.logger : List[List] = []

    def __str__(self) -> str:
        model_str = [str(model) for model in self.models]
        return f"time: {self.global_time}\n" + model_str + "\n"

    def time(self) -> float:
        return self.global_time

    def add_model(self, model: MLModel) -> None:
        self.models.append(model)

    def run_model(self, model: MLModel) -> None:
        self.global_time += self.memory_manger.load(model)
        self.log_event(f"Load model: {model.name}")
        self.global_time += model.latency
        self.log_event(f"Run")
        

    @abstractmethod
    def run(self, run_time : float) -> None:
        pass

    # Logging information to look at event history
    def log_event(self, event: str) -> None:
        self.logger.append([event, self.global_time])

    def store_log_information(self, file: str) -> None:
        f = open(file, "w")
        for event, time in self.logger:
            f.write(f"{event}: {time}\n")
        f.close()

