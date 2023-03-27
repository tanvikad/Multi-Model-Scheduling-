"""
This is a class representation of a machine learning model. We use information from this class
to calculate name, load time, and latency.
"""
class MLModel:
    def __init__(self, name: str, load_time: float, latency: float, space : float) -> None:
        self.name : str = name
        self.load_time : float = load_time
        self.latency : float = latency
        self.space : float = space
    
    def __str__(self) -> str:
        return f"name: {self.name} \nload time: {self.load_time}\nlatency: {self.latency}\nspace: {self.space}\n"
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    