from assets.MLModel import MLModel

class MemoryManger:
    def __init__(self, max_memory: int = 16_000):
        self.MAX_MEMORY : float = max_memory # mb
        self.loaded : set[MLModel] = set()
        self.curr_memory : float = 0
    
    def can_load(self, model: MLModel) -> bool:
        if model in self.loaded:
            return True
        return self.curr_memory + model.space < self.MAX_MEMORY
    
    def load(self, model: MLModel) -> float:
        load_time = 0
        if model in self.loaded:
            return load_time

        while not self.can_load(model):
            load_time += self.evict()
        
        self.loaded.add(model)
        self.curr_memory += model.space
        load_time += model.load_time
        return load_time

    # TODO: implement an eviction policy atm it is random
    def evict(self) -> int:
        eviction_time = 0
        evicted_model = self.loaded.pop()
        self.curr_memory -= evicted_model.space
        return eviction_time
