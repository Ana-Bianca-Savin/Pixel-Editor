from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool, BrushType
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool
from core.tools.buckettool import BucketTool
import time

# Canvas set-up

size = (100, 100)

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, fill_color=(255, 255, 255, 255))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(0)

# Tools set-up

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

brush_size = 1

# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as CanvasWidget
from tkinter import colorchooser
from PIL import ImageTk, Image

def use_brush(event):
    x, y = event.x, event.y
    BrushTool().set_brush_size(brush_size)
    BrushTool().set_brush_type(BrushType.SQUARE)
    BrushTool().paint(canvas, x // 8, y // 8, current_color) 
    # print(f"Mouse clicked at pixel coordinates ({x // 8}, {y // 8})")

def use_fill(event):
    x, y = event.x, event.y
    BucketTool().fill(canvas, x // 8, y // 8, current_color)
    # print(f"Mouse clicked at pixel coordinates ({x // 8}, {y // 8})")

def use_eraser(event):
    x, y = event.x, event.y
    BrushTool().set_brush_size(brush_size)
    BrushTool().set_brush_type(BrushType.SQUARE)
    BrushTool().paint(canvas, x // 8, y // 8, (255, 255, 255, 255))

def use_line_tool(event):
    x, y = event.x, event.y
    #BrushTool().set_brush_size(2)
    #BrushTool().set_brush_type(BrushType.ROUND)
    LineTool().set_line_width(2)
    LineTool().draw_line(canvas, x // 8, y // 8, current_color)

def use_eyedropper_tool(event):
    print("wow eyedropper sau cv")

def use_rectangle_tool(event):
    print("wow rectangle")

def update_current_tool():
    global selected_tool
    c_w.unbind("<Button-1>")
    c_w.unbind("<B1-Motion>")

    if selected_tool == 1:
        c_w.bind("<B1-Motion>", use_brush)
        c_w.bind("<Button-1>", use_brush)
    elif selected_tool == 2:
        c_w.bind("<Button-1>", use_fill)
    elif selected_tool == 3:
        c_w.bind("<B1-Motion>", use_eraser)
        c_w.bind("<Button-1>", use_eraser)
    elif selected_tool == 4:
        c_w.bind("<B1-Motion>", use_line_tool)
        c_w.bind("<Button-1>", use_line_tool)
    elif selected_tool == 5:
        c_w.bind("<B1-Motion>", use_eyedropper_tool)
        c_w.bind("<Button-1>", use_eyedropper_tool)
    elif selected_tool == 6:
        c_w.bind("<B1-Motion>", use_rectangle_tool)
        c_w.bind("<Button-1>", use_rectangle_tool)


# Initialize screen
ws = Tk()
ws.title('Canvas Preview')
ws.geometry('800x800')

# This label should be the name of the project
label = Label(ws, text="incerc", font=('Arial', 18))
label.pack()

# This frame contains the three main columns of the application
applicationFrame = Frame(ws)
applicationFrame.columnconfigure(0, weight=1)
applicationFrame.columnconfigure(1, weight=1)
applicationFrame.columnconfigure(2, weight=1)
applicationFrame.pack()


# COLUMN 1

#  Field for selecting the brush size
# input_brush_size = Text(applicationFrame, height = 20, width = 20) 
# input_brush_size.grid(row=0, column=0, sticky='nw', padx=(0, 20))
# brush_size = input_brush_size.get(1.0, "end-1c")
# print(brush_size)

def test_func(arg):
    global brush_size
    brush_size = int(arg)
    print(brush_size)


label = Label(applicationFrame, text="Brush size", font=('Arial', 12))
label.grid(row=0, column=0, sticky='nwe', padx=(0, 20))

slider = Scale(
    applicationFrame,
    from_=1,
    to=10,
    orient='horizontal',
    command=test_func,
)
slider.grid(row=0, column=0, sticky='nwe', padx=(0, 20), pady=(20, 0))

# This frame contains all the tools buttons, placed in the first column
buttonFrame = Frame(applicationFrame)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.grid(row=0, column=0, sticky='nw', padx=(0, 20), pady=(200, 0))

#  Icons for buttons
brush_tool_img = ImageTk.PhotoImage(Image.open('./assets/icons8-brush-48.png'))
fill_tool_img = ImageTk.PhotoImage(Image.open('./assets/icons8-fill-drip-48.png'))
eraser_tool_img = ImageTk.PhotoImage(Image.open('./assets/icons8-eraser-48.png'))
line_tool_img = ImageTk.PhotoImage(Image.open('./assets/icons8-line-48.png'))
eyedropper_img = ImageTk.PhotoImage(Image.open('./assets/icons8-eye-dropper-48.png'))
rectangle_tool_img = ImageTk.PhotoImage(Image.open('./assets/icons8-rectangle-48.png'))

# Colors for buttons
btn_color1 = '#0a0b0c'
btn_color2 = '#606266'
btn_color3 = '#72757a'
btn_color4 = 'BLACK'

# Padding for buttons
buttons_padding_x = 5
buttons_padding_y = 5

#  Index of the selected tool
selected_tool = 1

def set_selected_tool(index):
    global selected_tool
    selected_tool = index
    update_current_tool()

btn_brush_tool = Button(
    buttonFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=50,
    height=50,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=brush_tool_img,
    font=('Arial', 18),
    command=lambda: set_selected_tool(1)
)
btn_brush_tool.grid(row=0, column=0, padx=buttons_padding_x, pady = buttons_padding_y)

btn_fill_tool = Button(
    buttonFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=50,
    height=50,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=fill_tool_img,
    font=('Arial', 18),
    command=lambda: set_selected_tool(2)
)
btn_fill_tool.grid(row=0, column=1, padx=buttons_padding_x, pady = buttons_padding_y)

btn_eraser_tool = Button(
    buttonFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=50,
    height=50,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=eraser_tool_img,
    font=('Arial', 18),
    command=lambda: set_selected_tool(3)
)
btn_eraser_tool.grid(row=1, column=0, padx=buttons_padding_x, pady = buttons_padding_y)

btn_line_tool = Button(
    buttonFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=50,
    height=50,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=line_tool_img,
    font=('Arial', 18),
    command=lambda: set_selected_tool(4)
)
btn_line_tool.grid(row=1, column=1, padx=buttons_padding_x, pady = buttons_padding_y)

btn_eyedropper_tool = Button(
    buttonFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=50,
    height=50,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=eyedropper_img,
    font=('Arial', 18),
    command=lambda: set_selected_tool(5)
)
btn_eyedropper_tool.grid(row=2, column=0, padx=buttons_padding_x, pady = buttons_padding_y)

btn_rectangle_tool = Button(
    buttonFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=50,
    height=50,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=rectangle_tool_img,
    font=('Arial', 18),
    command=lambda: set_selected_tool(6)
)
btn_rectangle_tool.grid(row=2, column=1, padx=buttons_padding_x, pady = buttons_padding_y)

# Undo and redo buttons
undo_img = ImageTk.PhotoImage(Image.open('./assets/icons8-undo-24.png'))
redo_img = ImageTk.PhotoImage(Image.open('./assets/icons8-redo-24.png'))

btn_undo = Button(
    applicationFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=30,
    height=30,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=undo_img,
)
btn_undo.grid(row=0, column=0, sticky='w', padx=(buttons_padding_x, 20), pady = (300, 0))

btn_redo = Button(
    applicationFrame,
    background=btn_color2,
    foreground=btn_color4,
    width=30,
    height=30,
    highlightthickness=2,
    highlightbackground=btn_color2,
    highlightcolor='WHITE',
    activebackground=btn_color3,
    activeforeground=btn_color4,
    cursor='hand1',
    border=0,
    image=redo_img,
)
btn_redo.grid(row=0, column=0, sticky='w', padx=(40 + buttons_padding_x, 20), pady = (300, 0))



# COLUMN 2

#  To print the canvas
c_w = CanvasWidget(applicationFrame, width=800, height=800)
c_w.bind("<B1-Motion>", use_brush)
c_w.bind("<Button-1>", use_brush)
# c_w.bind("<Button-3>", use_fill)
c_w.grid(row=0, column=1)

img = ImageTk.PhotoImage(canvas.top_texture.resize((800, 800), resample=Image.NEAREST))
c_w.create_image(0, 0, anchor=NW, image=img)

def draw_frame():
    global img, c_w, ws
    c_w.delete("all")
    img = ImageTk.PhotoImage(canvas.top_texture.resize((800, 800), resample=Image.NEAREST))
    c_w.create_image(0, 0, anchor=NW, image=img)
    ws.after(33, draw_frame)  # 30fps = ~33ms delay
draw_frame()


# COLUMN 3

# Color chooser
current_color = "black"
def choose_color():
    global current_color
    current_color = colorchooser.askcolor()[1]
btn_color = Button(applicationFrame, text="Pick a color", font=('Arial', 18), command=choose_color)
btn_color.grid(row=0, column=2)

# Color preview
square = CanvasWidget(applicationFrame, width=50, height=50)
square.configure(bg=current_color)
square.grid(row=0, column=2, pady=(200, 0))

def draw_current_color():
    global square
    square.delete("all")
    square.configure(bg=current_color)
    ws.after(33, draw_current_color)
draw_current_color()

ws.mainloop()
