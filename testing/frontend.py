from core.layer import BlendingMode
from core.canvas import Canvas
from core.tools.brushtool import BrushTool
from core.tools.erasertool import EraserTool
from core.tools.linetool import LineTool
from core.tools.rectangletool import RectangleTool
from core.tools.buckettool import BucketTool
from core.tools.eyedropper import Eyedropper
from core.mouseutil import MouseUtil
from core.undoredo import UndoRedoManager
from core.utilties import export

# Canvas set-up
undo_manager = UndoRedoManager()
size = (200, 200)
real_size = (800, 800)
scale_factor_x = real_size[0] / size[0]
scale_factor_y = real_size[1] / size[1]

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, fill_color=(255, 255, 255, 255))
canvas.add_layer(BlendingMode.NORMAL)
canvas.add_layer(BlendingMode.NORMAL)

canvas.set_active_layer(0)
undo_manager.push_canvas(canvas)


# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as CanvasWidget
from tkinter import colorchooser
from PIL import ImageTk, Image

def undo_handler(event):
    global canvas
    new_canvas = undo_manager.undo()
    if new_canvas is not None:
        print('undone')
        canvas = new_canvas

def redo_handler(event):
    global canvas
    new_canvas = undo_manager.redo()
    if new_canvas is not None:
        print('redone')
        canvas = new_canvas

def handle_preview():
    global selected_tool

    if selected_tool == 4 and LineTool().get_drawing_state() is True:
        # Draw the preview
        origin = LineTool().get_origin()
        end = (MouseUtil().mouse_x, MouseUtil().mouse_y)

        def distance(p0, p1):
            return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2
        
        if (distance(origin, end) > 9):
            canvas.preview_layer.draw_line(origin, end, current_color, BrushTool().get_brush_size())
            canvas.update_top_texture()

    if selected_tool == 6 and RectangleTool().get_drawing_state() is True:
        # Draw the preview
        origin = RectangleTool().get_origin()
        end = (MouseUtil().mouse_x, MouseUtil().mouse_y)

        def distance(p0, p1):
            return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2
        
        if (distance(origin, end) > 9):
            canvas.preview_layer.draw_rectangle(origin, end, (0, 0, 0, 0), current_color, BrushTool().get_brush_size())
            canvas.update_top_texture()

def release_m1(event):
    global selected_tool
    x, y = event.x, event.y
    MouseUtil().update_m1_button(False)
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)

    if selected_tool == 1 or selected_tool == 3:
        undo_manager.push_canvas(canvas)

    if selected_tool == 4 and LineTool().get_drawing_state() is True:
        LineTool().set_drawing_state(False)
        origin = LineTool().get_origin()
        end = (MouseUtil().mouse_x, MouseUtil().mouse_y)
        def distance(p0, p1):
            return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2
        
        if (distance(origin, end) > 9):
            LineTool().set_line_width(BrushTool().get_brush_size())
            LineTool().draw_line(canvas, origin, end, current_color)

        undo_manager.push_canvas(canvas)

    if selected_tool == 6 and RectangleTool().get_drawing_state() is True:
        RectangleTool().set_drawing_state(False)
        origin = RectangleTool().get_origin()
        end = (MouseUtil().mouse_x, MouseUtil().mouse_y)
        def distance(p0, p1):
            return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2
        
        if (distance(origin, end) > 9):
            RectangleTool().set_stroke_weight(BrushTool().get_brush_size())
            RectangleTool().set_stroke_color(current_color)
            RectangleTool().draw_rectangle(canvas, origin, end)

        undo_manager.push_canvas(canvas)

def use_brush(event):
    x, y = event.x, event.y
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)
    BrushTool().paint(canvas, x // scale_factor_x, y // scale_factor_y, current_color)

def use_brush_hold(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)

    mouse_x = MouseUtil().mouse_x
    mouse_y = MouseUtil().mouse_y
    prev_x = MouseUtil().prev_x
    prev_y = MouseUtil().prev_y

    BrushTool().paint(canvas, mouse_x, mouse_y, current_color)
    # But hold on, if the previous frame we were still holding down the m1 button,
    # depending of the speed of the mouse, we might have missed some spots to draw.
    # So interpolate the mouse position between the previous mouse position and the current one
    if MouseUtil().m1_down is True and MouseUtil().prev_m1_down is True:
        distance = ((mouse_x - prev_x)**2 + (mouse_y - prev_y)**2)**0.5
        if distance < 0.75 * BrushTool().get_brush_size():
            return
        num_steps = 10

        step_x = (mouse_x - prev_x) / num_steps
        step_y = (mouse_y - prev_y) / num_steps
        for i in range(num_steps):
            x = int(prev_x + i * step_x)
            y = int(prev_y + i * step_y)
            BrushTool().paint(canvas, x, y, current_color)


def use_fill(event):
    x, y = event.x, event.y
    BucketTool().fill(canvas, x // scale_factor_x, y // scale_factor_y, current_color)
    undo_manager.push_canvas(canvas)

def use_eraser(event):
    x, y = event.x, event.y
    EraserTool().set_eraser_size(BrushTool().get_brush_size())
    EraserTool().erase(x // scale_factor_x, y // scale_factor_y, canvas)

def use_line_tool(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)
    if LineTool().get_drawing_state() is False:
        # Mark the start of the preview and save the origin
        LineTool().set_drawing_state(True)
        LineTool().set_origin((MouseUtil().mouse_x, MouseUtil().mouse_y))

def use_line_tool_hold(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)


def use_eyedropper_tool(event):
    global current_color
    x, y = event.x, event.y
    # Get the pixel color, slicing the alpha channel off
    pixel_color = Eyedropper().sample(canvas, x // scale_factor_x, y // scale_factor_y)[:3]
    # Convert it to hex then set it as the current color
    hex_color = "#{:02X}{:02X}{:02X}".format(*pixel_color)    
    current_color = hex_color

def use_rectangle_tool(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)
    if RectangleTool().get_drawing_state() is False:
        # Mark the start of the preview and save the origin
        RectangleTool().set_drawing_state(True)
        RectangleTool().set_origin((MouseUtil().mouse_x, MouseUtil().mouse_y))

def use_rectangle_tool_hold(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factor_x, y // scale_factor_y)

def highlight_button():
    global btn_brush_tool, btn_fill_tool, btn_eraser_tool, btn_line_tool, btn_eyedropper_tool, btn_rectangle_tool
    global selected_tool, btn_color2, btn_color3
    buttons = [btn_brush_tool, btn_fill_tool, btn_eraser_tool, btn_line_tool, btn_eyedropper_tool, btn_rectangle_tool]
    buttons[selected_tool - 1].config(background="#373738", activebackground="#373738")

    for i, button in enumerate(buttons):
        if i != selected_tool - 1:
            button.config(background=btn_color2, activebackground=btn_color3)
        

def update_current_tool():
    global selected_tool
    c_w.unbind("<Button-1>")
    c_w.unbind("<B1-Motion>")

    highlight_button()

    if selected_tool == 1:
        c_w.bind("<B1-Motion>", use_brush_hold)
        c_w.bind("<Button-1>", use_brush)
    elif selected_tool == 2:
        c_w.bind("<Button-1>", use_fill)
    elif selected_tool == 3:
        c_w.bind("<B1-Motion>", use_eraser)
        c_w.bind("<Button-1>", use_eraser)
    elif selected_tool == 4:
        c_w.bind("<B1-Motion>", use_line_tool_hold)
        c_w.bind("<Button-1>", use_line_tool)
    elif selected_tool == 5:
        c_w.bind("<B1-Motion>", use_eyedropper_tool)
        c_w.bind("<Button-1>", use_eyedropper_tool)
    elif selected_tool == 6:
        c_w.bind("<B1-Motion>", use_rectangle_tool_hold)
        c_w.bind("<Button-1>", use_rectangle_tool)


# Initialize screen
ws = Tk()
ws.title('Pixel Editor')
# ws.geometry('800x800')

# This label should be the name of the project
label = Label(ws, text="Pixel Editor", font=('Arial', 18))
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

def change_brush_size(arg):
    BrushTool().set_brush_size(int(arg))

#brush_size = int(DoubleVar().get())
slider = Scale(
    applicationFrame,
    from_=1,
    to=10,
    orient='horizontal',
    command=change_brush_size,
)
slider.grid(row=0, column=0, sticky='nwe', padx=(0, 20))

# This frame contains all the tools buttons, placed in the first column
buttonFrame = Frame(applicationFrame)
buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.grid(row=0, column=0, sticky='nw', padx=(0, 20), pady=(100, 0))

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


# COLUMN 2

#  To print the canvas
c_w = CanvasWidget(applicationFrame, width=real_size[0], height=real_size[1])
selected_tool = 1
highlight_button()
c_w.bind("<B1-Motion>", use_brush_hold)
c_w.bind("<Button-1>", use_brush)
c_w.bind("<ButtonRelease-1>", release_m1)
c_w.bind_all("<Control-z>", undo_handler)
c_w.bind_all("<Control-y>", redo_handler)
c_w.grid(row=0, column=1)

def draw_frame():
    global img, c_w, ws
    c_w.delete("all")

    handle_preview()

    img = ImageTk.PhotoImage(canvas.top_texture.resize(real_size, resample=Image.NEAREST))
    c_w.create_image(0, 0, anchor=NW, image=img)
    canvas.preview_layer.clear()
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
