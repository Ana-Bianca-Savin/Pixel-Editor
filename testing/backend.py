from core.layer import Layer, BlendingMode
from core.canvas import Canvas

size = (100, 100)

canvas = Canvas(size)

layer1 = Layer(size, BlendingMode.NORMAL, background_color=(255, 255, 255, 255))
layer2 = Layer(size, BlendingMode.NORMAL)
layer3 = Layer(size, BlendingMode.NORMAL)

canvas.add_layer(layer1)
canvas.add_layer(layer2)
canvas.add_layer(layer3)

layer1.set_pixel((50, 50), (255, 0, 0, 255))
layer2.set_pixel((20, 20), (255, 0, 0, 255))
layer3.set_pixel((60, 60), (255, 0, 0, 255))

image = canvas.merge_layers()
image.show()