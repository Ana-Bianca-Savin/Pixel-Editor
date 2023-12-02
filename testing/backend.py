from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool, BrushType
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool
from core.tools.buckettool import BucketTool
from core.utilties import *
from core.transform import *

size = (200, 200)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, fill_color=(31, 29, 42))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(1)

pizza_texture = import_texture("./testing/pizza.png")

canvas.place_texture(Transform.scale(pizza_texture, (80, 80)), (40, 100))
canvas.place_texture(Transform.rotate(Transform.scale(pizza_texture, (30, 30)), 45), (150, 120))

canvas.place_texture(Transform.rotate(Transform.scale(pizza_texture, (100, 100)), 195), (150, 30))

canvas.set_active_layer(2)

# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as CanvasWidget
from PIL import ImageTk, Image

def use_brush(event):
    x, y = event.x, event.y
    BrushTool().set_brush_size(5)
    BrushTool().set_brush_type(BrushType.ROUND)
    BrushTool().paint(canvas, x // scale_factor_x, y // scale_factor_y, (146, 14, 13, 255)) 

def use_eraser(event):
    x, y = event.x, event.y
    BrushTool().set_brush_size(9)
    BrushTool().set_brush_type(BrushType.ROUND)
    BrushTool().paint(canvas, x // scale_factor_x, y // scale_factor_y, (0, 0, 0, 0)) 

ws = Tk()
ws.title('Canvas Preview')
ws.geometry('800x800')

canvas_size = (800, 800)

scale_factor_x = canvas_size[0] // size[0]
scale_factor_y = canvas_size[1] // size[1]

c_w = CanvasWidget(ws, width=canvas_size[0], height=canvas_size[1])
c_w.bind("<B1-Motion>", use_brush)
c_w.bind("<Button-1>", use_brush)
c_w.bind("<Button-3>", use_eraser)
c_w.bind("<B3-Motion>", use_eraser)
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

# Save to disk
export(canvas.top_texture, 'PNG', size, Image.NEAREST, 'output.png')
