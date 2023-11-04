from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool
from core.tools.buckettool import BucketTool

size = (100, 100)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, background_color=(255, 255, 255, 255))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(0)

BrushTool().set_brush_size(5)
BrushTool().paint(canvas, 50, 50, (227, 11, 93, 255))

BrushTool().set_brush_size(1)
BrushTool().paint(canvas, 52, 52, (0, 255, 0, 255))

canvas.set_active_layer(1)
RectangleTool().set_fill(False)
RectangleTool().set_stroke_color((0, 128, 128, 255))
RectangleTool().set_stroke_weight(2)
RectangleTool().draw_rectangle(canvas, (60, 10), (90, 40))
LineTool().draw_line(canvas, (60, 10), (90, 40), (0, 0, 0, 255))
BucketTool().fill(canvas, 70, 16, (255, 0, 0, 255))

LineTool().set_line_width(1)
LineTool().draw_line(canvas, (20, 20), (40, 80), (0, 0, 0, 255))

canvas.set_active_layer(2)
RectangleTool().set_fill(False)
RectangleTool().set_stroke_color((0, 0, 255, 255))
RectangleTool().set_stroke_weight(1)
RectangleTool().draw_rectangle(canvas, (60, 63), (90, 90))

BrushTool().set_brush_size(10)
BrushTool().paint(canvas, 80, 60, (255, 200, 0, 255))

EraserTool().set_eraser_size(5)
EraserTool().erase(80, 60, canvas)

# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as canvas_widget
from PIL import ImageTk, Image

ws = Tk()
ws.title('Canvas Preview')
ws.geometry('500x500')

c_w = canvas_widget(ws, width=500, height=500)
c_w.pack()
img = ImageTk.PhotoImage(canvas.top_texture.resize((500, 500), resample=Image.NEAREST))
c_w.create_image(0, 0, anchor=NW, image=img)
ws.mainloop()
