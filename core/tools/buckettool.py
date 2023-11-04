from core.tools.tool import Tool


class BucketTool(Tool):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def fill(self, canvas, x, y, color):
        target_color = canvas.get_pixel((x, y))

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()
            if canvas.get_pixel((x, y)) == target_color:
                canvas.set_pixel((x, y), color)

                # Check neighboring pixels
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_x, new_y = x + dx, y + dy

                    if 0 <= new_x < canvas.size[0] and 0 <= new_y < canvas.size[1]:
                        stack.append((new_x, new_y))
