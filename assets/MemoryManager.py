from assets.MLModel import MLModel
from typing import List
from enum import Enum
import random

class Eviction(Enum):
    MRU = 1
    LRU = 2
    RAND = 3


class MemoryManager:
    def __init__(self, max_memory: int = 16000, evict_policy= Eviction.MRU):
        self.MAX_MEMORY : float = max_memory # mb
        self.loaded : set[MLModel] = set()
        self.last_seen : List[MLModel] = []
        self.curr_memory : float = 0
        self.evict_policy = evict_policy
    
    def can_load(self, model: MLModel) -> bool:
        if model in self.loaded:
            return True
        return self.curr_memory + model.space < self.MAX_MEMORY
    
    def load(self, model: MLModel) -> float:
        CACHE_HIT_TIME = 0.0
        if model in self.loaded:
            return CACHE_HIT_TIME

        while not self.can_load(model):
            self.evict()

        self.most_recently_use_helper(model)
        self.loaded.add(model)
        self.curr_memory += model.space
        return model.load_time

    def evict(self) -> None:
        if (self.evict_policy == Eviction.LRU): evicted_model = self.last_seen.pop(0)   # Remove the least recently used
        elif (self.evict_policy == Eviction.MRU): evicted_model = self.last_seen.pop(-1)  # Remove the most recently used
        else:
            random_index = random.randint(0, len(self.last_seen)-1)
            evicted_model = self.last_seen[random_index]
        self.loaded.remove(evicted_model)
        self.curr_memory -= evicted_model.space

    def most_recently_use_helper(self, model: MLModel):
        if model in self.last_seen:
            self.last_seen.remove(model)
        
        self.last_seen.append(model)

