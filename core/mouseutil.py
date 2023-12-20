# A util class that handles mouse input
# It should also implement mouse interpolation
# TODO
class MouseUtil():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.mouse_x = 0
            cls._instance.mouse_y = 0
            cls._instance.prev_x = 0
            cls._instance.prev_y = 0

            cls._instance.m1_down = False
            cls._instance.prev_m1_down = False
        return cls._instance
    
    def update_mouse_coords(self, x : float, y : float):
        self.prev_x = self.mouse_x
        self.prev_y = self.mouse_y

        self.mouse_x = x
        self.mouse_y = y

    def update_m1_button(self, m1_down : bool):
        self.prev_m1_down = self.m1_down
        self.m1_down = m1_down

    def interpolate(self, num_steps: int):
        step_x = (self.mouse_x - self.prev_x) / num_steps
        step_y = (self.mouse_y - self.prev_y) / num_steps
        points = []
        for i in range(num_steps):
            x = int(self.prev_x + i * step_x)
            y = int(self.prev_y + i * step_y)
            points.append((x, y))
        return points