from assets.MLModel import MLModel
from typing import List

class MemoryManager:
    def __init__(self, max_memory: int = 16_000):
        self.MAX_MEMORY : float = max_memory # mb
        self.loaded : set[MLModel] = set()
        self.last_seen : List[MLModel] = []
        self.curr_memory : float = 0
    
    def can_load(self, model: MLModel) -> bool:
        if model in self.loaded:
            return True
        return self.curr_memory + model.space < self.MAX_MEMORY
    
    def load(self, model: MLModel) -> float:
        CACHE_HIT_TIME = 0.0
        self.most_recently_use_helper(model)

        if model in self.loaded:
            return CACHE_HIT_TIME

        while not self.can_load(model):
            self.evict()
        
        self.loaded.add(model)
        self.curr_memory += model.space
        return model.load_time

    def evict(self) -> None:
        for model in self.last_seen:
            try:
                self.loaded.remove(model)
                self.curr_memory -= model.space
            except:
                continue


    def most_recently_use_helper(self, model: MLModel):
        if model in self.last_seen:
            self.last_seen.remove(model)
        
        self.last_seen.append(model)

