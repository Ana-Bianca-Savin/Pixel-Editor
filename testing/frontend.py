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

# denis' great (copium) code
from testing.color_palette import Color_Palette as cp
from testing.manage_color_palette import *

current_palette_idx = 0
palettes_idxs = ["1"]
color_palettes = [cp(["black"])]
palette_buttons_array = []


def change_draw_color(color: str):
    global current_color
    current_color = color


def palette_on_option_change(value):
    global current_palette_idx
    current_palette_idx = palettes_idxs.index(value)
    update_palette_colors_display()


def display_line(nr_of_colors: int, colors, start_idx: int, ypadding: int):
    if nr_of_colors == 1:
        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_palettes[current_palette_idx].colors[start_idx])
        color_button.grid(row=0, column=2, pady=(625 + 115 * ypadding, 0))
        color_button.bind("<Button-1>"
                          , lambda event, color=colors[start_idx]: change_draw_color(color))
        palette_buttons_array.append(color_button)
    elif nr_of_colors == 2:
        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_palettes[current_palette_idx].colors[start_idx])
        color_button.grid(row=0, column=2, pady=(625 + 115 * ypadding, 0), padx=(0, 65))
        color_button.bind("<Button-1>"
                          , lambda event, color=colors[start_idx]: change_draw_color(color))
        palette_buttons_array.append(color_button)

        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_palettes[current_palette_idx].colors[start_idx + 1])
        color_button.grid(row=0, column=2, pady=(625 + 115 * ypadding, 0), padx=(65, 0))
        color_button.bind("<Button-1>"
                          , lambda event, color=colors[start_idx + 1]: change_draw_color(color))
        palette_buttons_array.append(color_button)
    elif nr_of_colors == 3:
        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_palettes[current_palette_idx].colors[start_idx])
        color_button.grid(row=0, column=2, pady=(625 + 115 * ypadding, 0), padx=(0, 115))
        color_button.bind("<Button-1>"
                          , lambda event, color=colors[start_idx]: change_draw_color(color))
        palette_buttons_array.append(color_button)

        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_palettes[current_palette_idx].colors[start_idx + 1])
        color_button.grid(row=0, column=2, pady=(625 + 115 * ypadding, 0))
        color_button.bind("<Button-1>"
                          , lambda event, color=colors[start_idx + 1]: change_draw_color(color))
        palette_buttons_array.append(color_button)

        color_button = CanvasWidget(applicationFrame, width=50, height=50)
        color_button.configure(bg=color_palettes[current_palette_idx].colors[start_idx + 2])
        color_button.grid(row=0, column=2, pady=(625 + 115 * ypadding, 0), padx=(115, 0))
        color_button.bind("<Button-1>"
                          , lambda event, color=colors[start_idx + 2]: change_draw_color(color))
        palette_buttons_array.append(color_button)


def update_palette_colors_display():
    global palette_buttons_array, current_color
    if len(palette_buttons_array) > 0:
        for i in palette_buttons_array:
            i.destroy()

    cnt = 0
    palette_buttons_array = []

    for i in range(len(color_palettes[current_palette_idx].colors)):
        if i % 3 == 0:
            if i + 2 < len(color_palettes[current_palette_idx].colors):
                display_line(3, color_palettes[current_palette_idx].colors, i, cnt)
            elif i + 1 < len(color_palettes[current_palette_idx].colors):
                display_line(2, color_palettes[current_palette_idx].colors, i, cnt)
            else:
                display_line(1, color_palettes[current_palette_idx].colors, i, cnt)

        if (i + 1) % 3 == 0:
            cnt += 1

    change_draw_color(color_palettes[current_palette_idx].colors[0])


# define a function to create a new color palette
def create_palette():
    global palettes_idxs, current_palette_idx, color_palettes, palette_buttons_array
    global select_field, select

    # new color palette object reference
    new_cp = cp([])
    # palette name stored as a str list to pass it by reference so it is mutable
    palette_name = [""]

    create_new_palette(ws, new_cp, palette_name, color_palettes)

    if not new_cp.colors:
        return

    color_palettes.append(new_cp)

    current_palette_idx = len(color_palettes) - 1

    if palette_name[0] == "":
        idx = len(color_palettes)

        # find the first available index
        while str(idx) in palettes_idxs or str(idx + 1) in palettes_idxs:
            idx += 1
            if str(idx) not in palettes_idxs and str(idx + 1) not in palettes_idxs:
                break

        palettes_idxs.append(str(idx))
        new_cp.name = str(idx)
    else:
        palettes_idxs.append(palette_name[0])
    select_field.set(palettes_idxs[current_palette_idx])

    select.destroy()
    select = OptionMenu(applicationFrame, select_field, *palettes_idxs, command=palette_on_option_change)
    select.grid(row=0, column=2, pady=(350, 0))

    update_palette_colors_display()


# define a function to edit an existing color palette
def edit_existing_palette():
    global palettes_idxs, current_palette_idx, color_palettes, palette_buttons_array
    global select_field, select

    # save the current_palette_idx in a list to pass it by reference, so it is mutable
    current_idx = [current_palette_idx]
    # memorize the old length of the color palettes array
    old_cps_len = len(color_palettes)
    # palette name stored as a str list to pass it by reference, so it is mutable
    palette_name = [palettes_idxs[current_palette_idx]]

    edit_palette(ws, color_palettes, current_idx, palette_name)
    # in case a change occurred, reflect it on the palette index
    if len(color_palettes) != old_cps_len:
        # make an array of the remaining palette names
        palettes_names = []
        for i in range(len(color_palettes)):
            palettes_names.append(color_palettes[i].name)
        print(palettes_idxs)
        print(palettes_names)

        # find the deleted palette index
        deleted_idx = -1
        for i in range(len(palettes_idxs)):
            if palettes_idxs[i] not in palettes_names:
                deleted_idx = i
                break

        print(deleted_idx)
        print(palettes_idxs[deleted_idx])

        # remove the deleted palette index from the palettes_idxs array
        palettes_idxs.remove(palettes_idxs[deleted_idx])
        select_field.set(palettes_idxs[current_idx[0]])

        # destroy the option menu then rebuild it updated
        select.destroy()
        select = OptionMenu(applicationFrame, select_field, *palettes_idxs, command=palette_on_option_change)
        select.grid(row=0, column=2, pady=(350, 0))
        select_field.trace("w", lambda *args: palette_on_option_change(select_field.get()))

        # if a change occurred, update the current_palette_idx
        current_palette_idx = current_idx[0]
    else:
        # if no change occurred, update the palette name
        palettes_idxs[current_idx[0]] = palette_name[0]
        select_field.set(palettes_idxs[current_idx[0]])

        # destroy the option menu then rebuild it updated
        select.destroy()
        select = OptionMenu(applicationFrame, select_field, *palettes_idxs, command=palette_on_option_change)
        select.grid(row=0, column=2, pady=(350, 0))
        select_field.trace("w", lambda *args: palette_on_option_change(select_field.get()))

    # if there are no colors in the palette, exit
    if not color_palettes[current_palette_idx].colors:
        return

    update_palette_colors_display()


# Display current palette colors
update_palette_colors_display()

# label for message 'Current palette'
current_palette_label = Label(applicationFrame, text="Current palette", font=('Arial', 18))
current_palette_label.grid(row=0, column=2, pady=(300, 0))

# define a select_field to switch between color palettes
select_field = StringVar(value="1")
select = OptionMenu(applicationFrame, select_field, *palettes_idxs, command=palette_on_option_change)
select.grid(row=0, column=2, pady=(350, 0))
select_field.trace("w", lambda *args: palette_on_option_change(select_field.get()))

# define 'create new color palette' button
create_cp_button = Button(applicationFrame, text="Create new color palette", font=('Arial', 18),
                          command=create_palette)
create_cp_button.grid(row=0, column=2, pady=(425, 0))

# define 'edit palette' button
edit_cp_button = Button(applicationFrame, text="Edit palette", font=('Arial', 18),
                        command=lambda: edit_existing_palette())
edit_cp_button.grid(row=0, column=2, pady=(500, 0))

ws.mainloop()
