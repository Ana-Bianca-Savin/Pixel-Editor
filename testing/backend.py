from core.layer import BlendingMode
from core.canvas import Canvas

size = (100, 100)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, background_color=(255, 255, 255, 255))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(0)
canvas.set_pixel((50, 50), (255, 0, 0, 255))

canvas.set_active_layer(1)
canvas.set_pixel((20, 20), (255, 0, 0, 255))

canvas.set_active_layer(2)
canvas.set_pixel((60, 60), (255, 0, 0, 255))

image = canvas.top_texture
image.show()