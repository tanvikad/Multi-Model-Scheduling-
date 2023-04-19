from abc import abstractmethod
from assets.MLModel import MLModel
from assets.MemoryManager import MemoryManager
from typing import List
import matplotlib.pyplot as plt 

class Simulation:
    def __init__(self, schedule) -> None:
        self.global_time : float = 0
        self.models : List[MLModel] = []
        self.memory_manger : MemoryManager = MemoryManager()
        self.logger : List[List] = []           # for logging
        self.schedule : List[List] = schedule

    def __str__(self) -> str:
        model_str = [str(model) for model in self.models]
        return f"time: {self.global_time}\n" + model_str + "\n"

    def time(self) -> float:
        return self.global_time

    def add_model(self, model: MLModel) -> None:
        self.models.append(model)

    def run_model(self, model: MLModel, task_no) -> None:
        load_cost = self.memory_manger.load(model)
        self.log_event(model, "Load")
        self.global_time += load_cost
        self.log_event(model, "Run", task_no=task_no)
        self.global_time += model.latency
        

    @abstractmethod
    def run(self, run_time : float) -> None:
        pass

    # Logging information to look at event history
    def log_event(self, model: MLModel, event: str, task_no=None) -> None:
        self.logger.append([self.global_time, model.name, event, task_no])

    def store_log_information(self, file: str) -> None:
        f = open(file, "w")
        for event, time in self.logger:
            f.write(f"{event}: {time}\n")
        f.close()

    def print_events(self) -> None:
        for time, model, event, task_no in self.logger:
            print(time, ":", model, ":", event, ":", task_no)

    def gantt_chart(self) -> None:   
        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()
        
        # Setting Y-axis limits
        gnt.set_ylim(0, 50)
        
        # Setting X-axis limits
        gnt.set_xlim(0, self.logger[-1][0])
        print("Last time is ", self.logger[-1][0])
        
        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Seconds')
        gnt.set_ylabel('Events')
        
        # Setting ticks on y-axis
        gnt.set_yticks([15, 25, 35])
        # Labelling tickes of y-axis
        gnt.set_yticklabels(['1', '2', '3'])
        
        # Setting graph attribute
        gnt.grid(True)
        
        # Declaring a bar in 

        run_arr = []
        done_arr = []
        load_arr = []

        prev_time = 0
        prev_event = "Load"
        for time, model, event, task_no in self.logger:
            if(prev_event == "Run"):
                run_arr += [(prev_time, (time-prev_time))]
            elif(prev_event == "Load"):
                load_arr += [(prev_time, (time-prev_time))]
            elif(prev_event == "Done"):
                done_arr += [(time, 0.5)]
            prev_time = time
            prev_event = event

        print(run_arr)
        print(load_arr)
        print(done_arr)

        gnt.broken_barh(run_arr, (30, 9), facecolors =('tab:orange'), label="Run")
        
        # Declaring multiple bars in at same level and same width
        gnt.broken_barh(load_arr, (10, 9),
                                facecolors ='tab:blue', label="Load")
        
        gnt.broken_barh(done_arr, (20, 9),
                                        facecolors =('tab:red'), label="Done Flag"), 
        
        plt.legend()
        plt.title("Gantt Chart")
        
        plt.savefig("gantt1.png")


    def status() -> None:
        pass

    def get_stats(self) -> None:
        print("The number of loads is ", str(self.get_number_loads()))
        print("The average wait time is: ", str(self.get_average_wait_time()))
        print("The average response time is: ", str(self.get_average_response_time()))
    
    
    def get_average_response_time(self):
        total_wait_time = 0
        wait_times = []
        for task_no, model_idx, arrival_time in self.schedule:
            first_occurance_of_job = 0
            wait_time_for_this_job = 0
            for time, model, event, task_no2 in self.logger:
                if(event == "Run" and task_no == task_no2):
                    first_occurance_of_job = time
                    break
            
            wait_time_for_this_job = first_occurance_of_job - arrival_time
            wait_times += [wait_time_for_this_job]
            total_wait_time += wait_time_for_this_job
    
        return (total_wait_time/len(self.schedule))


    def get_average_wait_time(self):
        #we will avoid the load times of own model
        total_wait_time = 0
        wait_time_arr = []
        for task_no, model_idx, arrival_time in self.schedule:
            wait_time_for_this_job = 0
            prev_event = "Load"
            prev_time = 0
            for time, model, event, task_no2 in self.logger:
                if(time == 0): continue
                if(task_no2 == task_no):
                    prev_time = time
                    prev_event = event
                    continue
                if(model == model_idx and prev_event == "Load"): 
                    prev_time = time
                    prev_event = event
                    continue
                wait_time_for_this_job+= (time-prev_time)
                prev_time = time
                prev_event = event
        
            total_wait_time += wait_time_for_this_job
            wait_time_arr += [wait_time_for_this_job]
        
        return total_wait_time/len(self.schedule)



    def get_number_loads(self) -> int:
        num_loads = 0
        for time, model, event, task_no in self.logger:
            if(event == "Load"):
                num_loads += 1
        return num_loads