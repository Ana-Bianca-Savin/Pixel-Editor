# consider the color palette an array of buttons
# that when clicked, change the current color

class Color_Palette:

    def __init__(self, colors):
        self.name = "1"
        self.colors = colors

    def set_colors(self, _new_colors):
        self.colors = _new_colors

    def return_color_at_idx(self, idx: int) -> str:
        return self.colors[idx]

    def get_colors(self):
        return self.colors
