from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool

size = (100, 100)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, background_color=(255, 255, 255, 255))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(0)
BrushTool().set_brush_size(5)
BrushTool().paint(50, 50, (255, 0, 0, 255), canvas)

BrushTool().set_brush_size(1)
BrushTool().paint(52, 52, (0, 255, 0, 255) , canvas)

LineTool().set_line_width(2)
LineTool().draw_line(canvas, (20, 20), (40, 60), (0, 0, 0, 255))

canvas.set_active_layer(2)
RectangleTool().set_fill(False)
RectangleTool().set_stroke_color((0, 0, 255, 255))
RectangleTool().set_stroke_weight(1)
RectangleTool().draw_rectangle(canvas, (60, 63), (90, 90))

BrushTool().set_brush_size(10)
BrushTool().paint(80, 60, (255, 200, 0, 255), canvas)

EraserTool().set_eraser_size(5)
EraserTool().erase(80, 60, canvas)

image = canvas.top_texture
image.show()
image.save('test.png')