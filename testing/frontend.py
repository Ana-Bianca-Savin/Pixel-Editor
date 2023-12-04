from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool
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

# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as CanvasWidget
from tkinter import colorchooser
from PIL import ImageTk, Image


def use_brush(event):
    x, y = event.x, event.y
    BrushTool().set_brush_size(2)
    BrushTool().paint(canvas, x // 8, y // 8, current_color)
    # print(f"Mouse clicked at pixel coordinates ({x // 8}, {y // 8})")


def use_fill(event):
    x, y = event.x, event.y
    BucketTool().fill(canvas, x // 8, y // 8, current_color)
    # print(f"Mouse clicked at pixel coordinates ({x // 8}, {y // 8})")


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

# This frame contains all the tools buttons, placed in the first column
buttonFrame = Frame(applicationFrame)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.grid(row=0, column=0, sticky='nw', padx=(0, 20))

#  Icons for buttons
brush_tool_img = ImageTk.PhotoImage(Image.open('./assets/paint-brush.png'))

btn_color1 = '#0a0b0c'
btn_color2 = '#606266'
btn_color3 = '#72757a'
btn_color4 = 'BLACK'

btn1 = Button(buttonFrame, text='1', font=('Arial', 18))
# btn1 = Button(
#     buttonFrame,
#     background=btn_color2,
#     foreground=btn_color4,
#     width=150,
#     height=50,
#     highlightthickness=2,
#     highlightbackground=btn_color2,
#     highlightcolor='WHITE',
#     activebackground=btn_color3,
#     activeforeground=btn_color4,
#     cursor='hand1',
#     border=0,
#     image=brush_tool_img,
#     compound=LEFT,
#     text='1',
#     font=('Arial', 18)
# )
btn1.grid(row=0, column=0)

btn2 = Button(buttonFrame, text='2', font=('Arial', 18))
btn2.grid(row=0, column=1)

btn3 = Button(buttonFrame, text='3', font=('Arial', 18))
btn3.grid(row=1, column=0)

btn4 = Button(buttonFrame, text='4', font=('Arial', 18))
btn4.grid(row=1, column=1)

btn5 = Button(buttonFrame, text='5', font=('Arial', 18))
btn5.grid(row=2, column=0)

btn6 = Button(buttonFrame, text='6', font=('Arial', 18))
btn6.grid(row=2, column=1)

# COLUMN 2

#  To print the canvas
c_w = CanvasWidget(applicationFrame, width=800, height=800)
c_w.bind("<B1-Motion>", use_brush)
c_w.bind("<Button-1>", use_brush)
c_w.bind("<Button-3>", use_fill)
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

# denis' great (copium) code
from testing.color_pallette import Color_Pallette as cp
from testing.manage_color_pallette import *

current_pallette_idx = 0
pallettes_idxs = ["1"]
color_pallettes = [cp(["black"])]
pallette_buttons_array = []



def change_draw_color(color: str):
    global current_color
    current_color = color


def pallette_on_option_change(value):
    global current_pallette_idx
    print(value)
    current_pallette_idx = int(value) - 1
    update_pallette_colors_display()


def update_pallette_colors_display():
    global pallette_buttons_array, current_color
    if len(pallette_buttons_array) > 0:
        for i in pallette_buttons_array:
            i.destroy()

    pallette_buttons_array = []
    for i in range(len(color_pallettes[current_pallette_idx].colors)):
        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_pallettes[current_pallette_idx].colors[i])
        color_button.grid(row=0, column=2, pady=(400, 0)
                          , padx=(115, 50 + 110 * (len(color_pallettes[current_pallette_idx].colors) - i)))
        color_button.bind("<Button-1>", lambda event,
                                               color=color_pallettes[current_pallette_idx].colors[
                                                   i]: change_draw_color(color))
        pallette_buttons_array.append(color_button)

    change_draw_color(color_pallettes[current_pallette_idx].colors[0])
    print(len(pallette_buttons_array))


# define a function to create a new color pallette
def create_pallette():
    global pallettes_idxs, current_pallette_idx, color_pallettes, pallette_buttons_array
    global select_field, select

    # select.destroy()
    # select = OptionMenu(applicationFrame, select_field, *pallettes_idxs, command=pallette_on_option_change)
    # select.grid(row=0, column=2, pady=(300, 0), padx=(0, 200))

    new_cp = cp([])

    create_new_pallette(ws, new_cp)

    color_pallettes.append(new_cp)

    current_pallette_idx = len(color_pallettes) - 1
    print(f'current_pallette_idx: {current_pallette_idx}')

    pallettes_idxs.append(str(len(color_pallettes)))
    select_field.set(pallettes_idxs[current_pallette_idx])

    select.destroy()
    select = OptionMenu(applicationFrame, select_field, *pallettes_idxs, command=pallette_on_option_change)
    select.grid(row=0, column=2, pady=(300, 0), padx=(0, 200))

    update_pallette_colors_display()


# Display current palette colors
update_pallette_colors_display()

# define a select_field to switch between color pallettes
select_field = StringVar(value="1")
select = OptionMenu(applicationFrame, select_field, *pallettes_idxs, command=pallette_on_option_change)
select.grid(row=0, column=2, pady=(300, 0), padx=(0, 200))

select_field.trace("w", lambda *args: pallette_on_option_change(select_field.get()))

# define 'create new color pallette' button
create_cp_button = Button(applicationFrame, text="Create new color pallette", font=('Arial', 18),
                          command=create_pallette)
create_cp_button.grid(row=0, column=2, pady=(300, 0), padx=(100, 0))

ws.mainloop()
