from core.tools.tool import Tool

class Eyedropper(Tool):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def sample(self, canvas, x, y):
        return canvas.get_pixel((x, y))