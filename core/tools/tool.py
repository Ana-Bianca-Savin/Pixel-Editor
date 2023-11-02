from abc import ABC

class Tool(ABC):
    def __init__(self):
        self.active = False
        self.position = [0, 0]