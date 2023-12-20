from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool, BrushType
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool
from core.tools.buckettool import BucketTool
from core.tools.eyedropper import Eyedropper
from core.utilties import *
from core.transform import *
from core.mouseutil import *

size = (200, 200)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, fill_color=(31, 29, 42))
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(1)

pizza_texture = import_texture("./testing/pizza.png")

# rotated_pizza = Transform.rotate(pizza_texture, 40)
# canvas.place_texture(rotated_pizza, (40, 100))

canvas.place_texture(Transform.scale(pizza_texture, (80, 80)), (40, 100))
# canvas.place_texture(Transform.rotate(Transform.scale(pizza_texture, (30, 30)), 45), (150, 120))

# canvas.place_texture(Transform.rotate(Transform.scale(pizza_texture, (100, 100)), 195), (150, 30))

canvas.set_active_layer(0)

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

def use_line_tool(event):
    x, y = event.x, event.y
    LineTool().set_line_width(2)
    LineTool().draw_line(canvas, (40, 40), (x // scale_factor_x, y // scale_factor_y), (0, 0, 0, 255))


def on_motion(event):
    x, y = event.x, event.y
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)

    # Do stuff depending on the current context (active tool, previously pressed buttons, etc.)

def on_m1_press(event):
    MouseUtil().update_m1_button(True)

    # Do stuff when pressing m1 button
    # For example, use the brush:

    mouse_x = MouseUtil().mouse_x
    mouse_y = MouseUtil().mouse_y

    BrushTool().set_brush_size(5)
    BrushTool().set_brush_type(BrushType.ROUND)
    BrushTool().paint(canvas, mouse_x, mouse_y, (146, 14, 13, 255))

    # Or use the eyedropper
    #print(Eyedropper().sample(canvas, mouse_x, mouse_y))


def on_m1_motion(event):
    x, y = event.x, event.y
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)
    MouseUtil().update_m1_button(True)

    # Do stuff while holding down m1 button
    # For example, use the brush:

    mouse_x = MouseUtil().mouse_x
    mouse_y = MouseUtil().mouse_y
    prev_x = MouseUtil().prev_x
    prev_y = MouseUtil().prev_y


    EraserTool().set_eraser_size(10)
    EraserTool().erase(mouse_x, mouse_y, canvas)

    # BrushTool().set_brush_size(5)
    # BrushTool().set_brush_type(BrushType.ROUND)
    # BrushTool().paint(canvas, mouse_x, mouse_y, (146, 14, 13, 255))

    # # But hold on, if the previous frame we were still holding down the m1 button,
    # # depending of the speed of the mouse, we might have missed some spots to draw.
    # # So interpolate the mouse position between the previous mouse position and the current one
    # if MouseUtil().m1_down is True and MouseUtil().prev_m1_down is True:
    #     distance = ((mouse_x - prev_x)**2 + (mouse_y - prev_y)**2)**0.5
    #     if distance < 0.75 * BrushTool().get_brush_size():
    #         return
    #     num_steps = 10

    #     step_x = (mouse_x - prev_x) / num_steps
    #     step_y = (mouse_y - prev_y) / num_steps
    #     for i in range(num_steps):
    #         x = int(prev_x + i * step_x)
    #         y = int(prev_y + i * step_y)
    #         BrushTool().paint(canvas, x, y, (146, 14, 13, 255))


def on_m1_release(event):
    MouseUtil().update_m1_button(False)

    # Do stuff on release of m1 button

ws = Tk()
ws.title('Canvas Preview')
ws.geometry('800x800')

canvas_size = (800, 800)

scale_factor_x = canvas_size[0] // size[0]
scale_factor_y = canvas_size[1] // size[1]

c_w = CanvasWidget(ws, width=canvas_size[0], height=canvas_size[1])
c_w.bind("<Motion>", on_motion)
c_w.bind("<Button-1>", on_m1_press)
c_w.bind("<B1-Motion>", on_m1_motion)
c_w.bind("<ButtonRelease-1>", on_m1_release)
c_w.pack()

img = ImageTk.PhotoImage(canvas.top_texture.resize(canvas_size, resample=Image.NEAREST))
c_w.create_image(0, 0, anchor=NW, image=img)

def draw_frame():
    global img, c_w, ws
    c_w.delete("all")

    canvas.update_top_texture()
    img = ImageTk.PhotoImage(canvas.top_texture.resize(canvas_size, resample=Image.NEAREST))
    canvas.preview_layer.clear()

    c_w.create_image(0, 0, anchor=NW, image=img)
    ws.after(33, draw_frame)  # 30fps = ~33ms delay, 60fps = ~16ms delay

draw_frame()
ws.mainloop()

# Save to disk
# export(canvas.top_texture, 'PNG', size, Image.NEAREST, 'output.png')
