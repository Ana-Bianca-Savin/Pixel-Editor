from core.tools.tool import Tool

class LineTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.stroke_weight = 1
            cls._instance.fill = False
        return cls._instance
    
    def draw_line(self, canvas):
        pass