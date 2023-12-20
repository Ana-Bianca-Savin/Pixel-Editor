from core.tools.tool import Tool

class BucketTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def fill(self, canvas, x, y, color):
        canvas.flood_fill((x, y), color)