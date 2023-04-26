from assets.Simulation import Simulation
from assets.scheduling_algorithm import SRTF, FCFS
from assets.MLModel import MLModel
from typing import List
import random

class LoadBalancer():
    def __init__(self, models, schedule, num_cluster = 2, cluster_type = None) -> None:
        self.models = models
        if cluster_type == None:
            self.cluster_list : List[Simulation] = [FCFS([]) for _ in range(num_cluster)]
        else:
            self.cluster_list : List[Simulation] = cluster_type
            
        for cluster in self.cluster_list:
            for m in models:
                cluster.add_model(m)

        self.cluster_active_pool : List[List[tuple]] = [[] for _ in range(len(self.cluster_list))]
        self.schedule : List[tuple] = schedule
    
    def run_to_finish(self):
      for active_pool, clust in zip(self.cluster_active_pool, self.cluster_list):
            while active_pool != []:
                clust.run_next(active_pool, float('inf'))
            
    def run_cluster(self, cluster_selection, next, model):
        self.cluster_active_pool[cluster_selection].append(next + [model.latency])
        self.cluster_list[cluster_selection].run_next(self.cluster_active_pool[cluster_selection], float('inf'))
        self.cluster_list[cluster_selection].schedule.append(next)


    def run_basic(self):
        while self.schedule != []:
            next = self.schedule.pop(0)
            model : MLModel = self.models[next[1]]
            flag = False

            for idx, cluster in enumerate(self.cluster_list):
                if model in cluster.memory_manger.loaded:
                    self.run_cluster(idx, next, model)
                    flag = True
                    break
            
            if flag:
                continue
            
            # we need to select a cluster to load the model
            cluster_selection = 0
            for idx, clust in enumerate(self.cluster_list):
                if clust.memory_manger.curr_memory < self.cluster_list[cluster_selection].memory_manger.curr_memory:
                    cluster_selection = idx
            
            self.run_cluster(cluster_selection, next, model)
        
        self.run_to_finish()

    def run_greedy(self):
        while self.schedule != []:
            next = self.schedule.pop(0)
            model : MLModel = self.models[next[1]]

            cluster_selection = 0
            for idx, clust in enumerate(self.cluster_list):
                if clust.global_time < self.cluster_list[cluster_selection].global_time:
                    cluster_selection = idx
            
            self.run_cluster(cluster_selection, next, model)
        
        self.run_to_finish()
    
    def run_random(self):
        while self.schedule != []:
            next = self.schedule.pop(0)
            model : MLModel = self.models[next[1]]

            cluster_section = random.randint(0, len(self.cluster_list) - 1)
            self.cluster_list[cluster_section].schedule.append(next)
        
        for clus in self.cluster_list:
            clus.run(1)
