from PIL import Image
from core.layer import Layer

class Canvas:
    def __init__(self, size):
        # When creating a new canvas, add the first default layer, transparent
        self.layers = []
        self.size = size
        self.top_texture = Image.new("RGBA", size, (0, 0, 0, 0))

        default_layer = Layer(size)
        self.add_layer(default_layer)

    def add_layer(self, layer):
        self.layers.append(layer)

    def set_top_texture(self, texture):
        self.top_texture = texture

    def merge_layers(self):
        merged = Image.new("RGBA", self.size, (0, 0, 0, 0))
        for layer in self.layers:
            merged = Image.alpha_composite(merged, layer.texture)
        return merged