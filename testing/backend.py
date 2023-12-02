from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool, BrushType
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool
from core.tools.buckettool import BucketTool
import time

size = (200, 200)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, fill_color=(255, 255, 255, 255))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(0)

BrushTool().set_brush_size(5)
BrushTool().paint(canvas, 50, 50, (227, 11, 93, 255))

BrushTool().set_brush_size(1)
BrushTool().paint(canvas, 52, 52, (0, 255, 0, 255))

# canvas.set_active_layer(1)
RectangleTool().set_fill(False)
RectangleTool().set_stroke_color((0, 128, 128, 255))
RectangleTool().set_stroke_weight(2)
RectangleTool().draw_rectangle(canvas, (60, 10), (90, 40))
LineTool().draw_line(canvas, (60, 10), (90, 40), (0, 0, 0, 255))
BucketTool().fill(canvas, 70, 16, (255, 0, 0, 255))

# LineTool().set_line_width(1)
# LineTool().draw_line(canvas, (20, 20), (40, 80), (0, 0, 0, 255))

# canvas.set_active_layer(2)
# RectangleTool().set_fill(False)
# RectangleTool().set_stroke_color((0, 0, 255, 255))
# RectangleTool().set_stroke_weight(1)
# RectangleTool().draw_rectangle(canvas, (60, 63), (90, 90))

# BrushTool().set_brush_size(10)
# BrushTool().paint(canvas, 80, 60, (255, 200, 0, 255))

# EraserTool().set_eraser_size(5)
# EraserTool().erase(80, 60, canvas)

# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as CanvasWidget
from PIL import ImageTk, Image

def use_brush(event):
    x, y = event.x, event.y
    # print(f"Mouse clicked at pixel coordinates ({x // 1}, {y // 1})")
    BrushTool().set_brush_size(5)
    BrushTool().set_brush_type(BrushType.ROUND)
    BrushTool().paint(canvas, x // scale_factor_x, y // scale_factor_y, (0, 255, 0, 255)) 

def use_fill(event):
    x, y = event.x, event.y
    BucketTool().fill(canvas, x // scale_factor_x, y // scale_factor_y, (255, 0, 0, 255))
    # print(f"Mouse clicked at pixel coordinates ({x // 8}, {y // 8})")

ws = Tk()
ws.title('Canvas Preview')
ws.geometry('800x800')

canvas_size = (800, 800)

scale_factor_x = canvas_size[0] // size[0]
scale_factor_y = canvas_size[1] // size[1]

c_w = CanvasWidget(ws, width=canvas_size[0], height=canvas_size[1])
c_w.bind("<B1-Motion>", use_brush)
c_w.bind("<Button-1>", use_brush)
c_w.bind("<Button-3>", use_fill)
c_w.pack()

img = ImageTk.PhotoImage(canvas.top_texture.resize(canvas_size, resample=Image.NEAREST))
c_w.create_image(0, 0, anchor=NW, image=img)  

def draw_frame():
    global img, c_w, ws
    c_w.delete("all")
    img = ImageTk.PhotoImage(canvas.top_texture.resize(canvas_size, resample=Image.NEAREST))
    c_w.create_image(0, 0, anchor=NW, image=img)
    ws.after(33, draw_frame)  # 30fps = ~33ms delay, 60fps = ~16ms delay

draw_frame()
ws.mainloop()
