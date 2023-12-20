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
scale_factors = [scale_factor_x, scale_factor_y]

canvas = Canvas(size)
canvas.add_layer(BlendingMode.NORMAL, fill_color=(255, 255, 255, 255))

canvas.set_active_layer(0)
undo_manager.push_canvas(canvas)


# ---- PREVIEW IMAGE ----
from tkinter import *
from tkinter import Canvas as CanvasWidget
from tkinter import colorchooser
from tkinter import ttk
from PIL import ImageTk, Image

def undo_handler(event):
    global canvas
    new_canvas = undo_manager.undo()
    if new_canvas is not None:
        canvas = new_canvas

def redo_handler(event):
    global canvas
    new_canvas = undo_manager.redo()
    if new_canvas is not None:
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
            canvas.preview_layer.draw_line(origin, end, current_color.get(), BrushTool().get_brush_size())
            canvas.update_top_texture()

    if selected_tool == 6 and RectangleTool().get_drawing_state() is True:
        # Draw the preview
        origin = RectangleTool().get_origin()
        end = (MouseUtil().mouse_x, MouseUtil().mouse_y)

        def distance(p0, p1):
            return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2
        
        if (distance(origin, end) > 9):
            canvas.preview_layer.draw_rectangle(origin, end, (0, 0, 0, 0), current_color.get(), BrushTool().get_brush_size())
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
            LineTool().draw_line(canvas, origin, end, current_color.get())

        undo_manager.push_canvas(canvas)

    if selected_tool == 6 and RectangleTool().get_drawing_state() is True:
        RectangleTool().set_drawing_state(False)
        origin = RectangleTool().get_origin()
        end = (MouseUtil().mouse_x, MouseUtil().mouse_y)
        def distance(p0, p1):
            return (p0[0] - p1[0])**2 + (p0[1] - p1[1])**2
        
        if (distance(origin, end) > 9):
            RectangleTool().set_stroke_weight(BrushTool().get_brush_size())
            RectangleTool().set_stroke_color(current_color.get())
            RectangleTool().draw_rectangle(canvas, origin, end)

        undo_manager.push_canvas(canvas)

def use_brush(event):
    x, y = event.x, event.y
    MouseUtil().update_mouse_coords(x // scale_factors[0], y // scale_factors[1])
    BrushTool().paint(canvas, x // scale_factors[0], y // scale_factors[1], current_color.get())

def use_brush_hold(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factors[0], y // scale_factors[1])

    mouse_x = MouseUtil().mouse_x
    mouse_y = MouseUtil().mouse_y
    prev_x = MouseUtil().prev_x
    prev_y = MouseUtil().prev_y

    BrushTool().paint(canvas, mouse_x, mouse_y, current_color.get())
    # But hold on, if the previous frame we were still holding down the m1 button,
    # depending of the speed of the mouse, we might have missed some spots to draw.
    # So interpolate the mouse position between the previous mouse position and the current one
    if MouseUtil().m1_down is True and MouseUtil().prev_m1_down is True:
        distance = ((mouse_x - prev_x)**2 + (mouse_y - prev_y)**2)**0.5
        if distance < 0.75 * BrushTool().get_brush_size():
            return

        points = MouseUtil().interpolate(num_steps=10)
        for p in points:
            BrushTool().paint(canvas, p[0], p[1], current_color.get())


def use_fill(event):
    x, y = event.x, event.y
    BucketTool().fill(canvas, x // scale_factors[0], y // scale_factors[1], current_color.get())
    undo_manager.push_canvas(canvas)

def use_eraser(event):
    x, y = event.x, event.y
    EraserTool().set_eraser_size(BrushTool().get_brush_size())
    EraserTool().erase(x // scale_factors[0], y // scale_factors[1], canvas)

def use_line_tool(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factors[0], y // scale_factors[1])
    if LineTool().get_drawing_state() is False:
        # Mark the start of the preview and save the origin
        LineTool().set_drawing_state(True)
        LineTool().set_origin((MouseUtil().mouse_x, MouseUtil().mouse_y))

def use_line_tool_hold(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factors[0], y // scale_factors[1])


def use_eyedropper_tool(event):
    global current_color
    x, y = event.x, event.y
    # Get the pixel color, slicing the alpha channel off
    pixel_color = Eyedropper().sample(canvas, x // scale_factors[0], y // scale_factors[1])[:3]
    # Convert it to hex then set it as the current color
    hex_color = "#{:02X}{:02X}{:02X}".format(*pixel_color)    
    current_color.set(hex_color)

def use_rectangle_tool(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factors[0], y // scale_factors[1])
    if RectangleTool().get_drawing_state() is False:
        # Mark the start of the preview and save the origin
        RectangleTool().set_drawing_state(True)
        RectangleTool().set_origin((MouseUtil().mouse_x, MouseUtil().mouse_y))

def use_rectangle_tool_hold(event):
    x, y = event.x, event.y
    MouseUtil().update_m1_button(True)
    MouseUtil().update_mouse_coords(x // scale_factors[0], y // scale_factors[1])

def highlight_button():
    global btn_brush_tool, btn_fill_tool, btn_eraser_tool, btn_line_tool, btn_eyedropper_tool, btn_rectangle_tool
    global selected_tool, btn_color2, btn_color3
    buttons = [btn_brush_tool, btn_fill_tool, btn_eraser_tool, btn_line_tool, btn_eyedropper_tool, btn_rectangle_tool]
    buttons[selected_tool - 1].config(background=btn_highlight1, foreground=btn_highlight3, highlightbackground=btn_highlight1, activebackground=btn_highlight2, activeforeground=btn_highlight3)

    for i, button in enumerate(buttons):
        if i != selected_tool - 1:
            button.config(background=btn_color1, foreground=btn_color3, highlightbackground=btn_color1, activebackground=btn_color2, activeforeground=btn_color3)
        

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

# Create a button with an image
def create_button_img(_parent_frame, tool_index, size, c1, c2, c3, image) -> Button:
    btn = Button(
        _parent_frame,
        background=c1,
        foreground=c3,
        width=size,
        height=size,
        highlightthickness=2,
        highlightbackground=c1,
        highlightcolor='WHITE',
        activebackground=c2,
        activeforeground=c3,
        cursor='hand1',
        border=0,
        image=image
    )

    if tool_index != 0:
        btn.configure(command=lambda: set_selected_tool(tool_index))

    return btn

# Initialize screen
ws = Tk()
ws.title('Pixel Editor')

# This label should be the name of the project
project_name = Label(ws, text="Pixel Editor", font=('Arial', 18))
project_name.pack()

# This frame contains the three main columns of the application
applicationFrame = Frame(ws)
applicationFrame.columnconfigure(0, weight=1)
applicationFrame.columnconfigure(1, weight=1)
applicationFrame.columnconfigure(2, weight=1)
applicationFrame.pack()


# COLUMN 1

#  Select the brush size
def change_brush_size(arg):
    BrushTool().set_brush_size(int(arg))

label = Label(applicationFrame, text="Brush size", font=('Arial', 12))
label.grid(row=0, column=0, sticky='nwe', padx=(0, 20))

slider = Scale(
    applicationFrame,
    from_=1,
    to=10,
    orient='horizontal',
    command=change_brush_size,
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
btn_color1 = '#606266'
btn_color2 = '#72757a'
btn_color3 = 'BLACK'

btn_highlight1 = "#81848a"
btn_highlight2 = "#7a7e85"
btn_highlight3 = "WHITE"

# Padding for buttons
buttons_padding_x = 5
buttons_padding_y = 5

#  Index of the selected tool
selected_tool = 1

def set_selected_tool(index):
    global selected_tool
    selected_tool = index
    update_current_tool()

# Create all the buttons for tools
btn_brush_tool = create_button_img(buttonFrame, 1, 50, btn_color1, btn_color2, btn_color3, brush_tool_img)
btn_brush_tool.grid(row=0, column=0, padx=buttons_padding_x, pady = buttons_padding_y)

btn_fill_tool = create_button_img(buttonFrame, 2, 50, btn_color1, btn_color2, btn_color3, fill_tool_img)
btn_fill_tool.grid(row=0, column=1, padx=buttons_padding_x, pady = buttons_padding_y)

btn_eraser_tool = create_button_img(buttonFrame, 3, 50, btn_color1, btn_color2, btn_color3, eraser_tool_img)
btn_eraser_tool.grid(row=1, column=0, padx=buttons_padding_x, pady = buttons_padding_y)

btn_line_tool = create_button_img(buttonFrame, 4, 50, btn_color1, btn_color2, btn_color3, line_tool_img)
btn_line_tool.grid(row=1, column=1, padx=buttons_padding_x, pady = buttons_padding_y)

btn_eyedropper_tool = create_button_img(buttonFrame, 5, 50, btn_color1, btn_color2, btn_color3, eyedropper_img)
btn_eyedropper_tool.grid(row=2, column=0, padx=buttons_padding_x, pady = buttons_padding_y)

btn_rectangle_tool = create_button_img(buttonFrame, 6, 50, btn_color1, btn_color2, btn_color3, rectangle_tool_img)
btn_rectangle_tool.grid(row=2, column=1, padx=buttons_padding_x, pady = buttons_padding_y)

# Undo and redo buttons
undo_img = ImageTk.PhotoImage(Image.open('./assets/icons8-undo-24.png'))
redo_img = ImageTk.PhotoImage(Image.open('./assets/icons8-redo-24.png'))

btn_undo = create_button_img(applicationFrame, 0, 30, btn_color1, btn_color2, btn_color3, undo_img)
btn_undo.configure(command=lambda event="<Control-z>": undo_handler(event))
btn_undo.grid(row=0, column=0, sticky='w', padx=(buttons_padding_x, 20), pady = (300, 0))

btn_redo = create_button_img(applicationFrame, 0, 30, btn_color1, btn_color2, btn_color3, redo_img)
btn_redo.configure(command=lambda event="<Control-y>": redo_handler(event))
btn_redo.grid(row=0, column=0, sticky='w', padx=(40 + buttons_padding_x, 20), pady = (300, 0))

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

column3Frame = Frame(applicationFrame)
column3Frame.columnconfigure(0, weight=1)
column3Frame.columnconfigure(1, weight=1)
column3Frame.columnconfigure(2, weight=1)
column3Frame.grid(row=0, column=2, sticky="n")

invis_canvas = CanvasWidget(column3Frame, width=200, height=200)
invis_canvas.grid(row=0, column=0, sticky="nw")

# Layer frame
from testing.layers_editor import *
create_layer_scroller(applicationFrame, canvas)

# Color chooser
current_color = StringVar(value="black")
def choose_color():
    global current_color
    clr = colorchooser.askcolor()[1]
    current_color.set(clr)
# btn_color = Button(applicationFrame, text="Pick a color", font=('Arial', 18), command=choose_color)


# Color preview
square = CanvasWidget(applicationFrame, width=50, height=50)
square.configure(bg=current_color.get())
square.grid(row=0, column=0, sticky='w', padx=(buttons_padding_x - 5, 20), pady=(450, 0))
square.bind("<Button-1>", lambda event: choose_color())

def draw_current_color():
    global square
    square.delete("all")
    square.configure(bg=current_color.get())
    ws.after(33, draw_current_color)


draw_current_color()

# denis' great (copium) code
from testing.manage_color_palette import *
from testing.SideBarGUI import *

sidebargui = SideBarGUI(canvas, ws, column3Frame)

# create canvas preview
preview_canvas = CanvasWidget(column3Frame, width=250, height=250)
preview_canvas.grid(row=1, column=0)

preview_image = ImageTk.PhotoImage(canvas.top_texture.resize((250, 250), resample=Image.NEAREST))
preview_canvas.create_image(0, 0, anchor=NW, image=preview_image)


def draw_preview_frame():
    global preview_image, preview_canvas, ws
    preview_canvas.delete("all")

    preview_canvas = CanvasWidget(column3Frame, width=250, height=250)
    preview_canvas.grid(row=1, column=0)

    preview_image = ImageTk.PhotoImage(canvas.top_texture.resize((250, 250), resample=Image.NEAREST))
    preview_canvas.create_image(0, 0, anchor=NW, image=preview_image)

    ws.after(33, lambda: draw_preview_frame())  # 30fps = ~33ms delay


draw_preview_frame()
# Display current palette colors
sidebargui.update_palette_colors_display(column3Frame, current_color)

# define menu button
menu_button = Button(column3Frame, text="Menu", font=('Arial', 11)
                     , command=lambda: open_menu(ws, project_name, canvas, scale_factors))
menu_button.grid(row=2, column=0)

# label for message 'Current palette'
current_palette_label = Label(column3Frame, text="Current palette", font=('Arial', 18))
current_palette_label.grid(row=3, column=0)

# define a select_field to switch between color palettes
select_field = StringVar(value="1")
select = OptionMenu(column3Frame, select_field, *sidebargui.palettes_idxs
                    , command=lambda: sidebargui.palette_on_option_change(select_field.get(), column3Frame,
                                                                          current_color))
select.grid(row=4, column=0)
select_field.trace("w",
                   lambda *args: sidebargui.palette_on_option_change(select_field.get(), column3Frame, current_color))

# define 'create new color palette' button
create_cp_button = Button(column3Frame, text="Create new color palette", font=('Arial', 11)
                          , command=lambda: sidebargui.create_palette(ws, select_field, select, column3Frame,
                                                                      current_color))
create_cp_button.grid(row=5, column=0, pady=(5, 0))

# define 'edit palette' button
edit_cp_button = Button(column3Frame, text="Edit palette", font=('Arial', 11)
                        , command=lambda: sidebargui.edit_existing_palette(ws, select_field, select, column3Frame,
                                                                           current_color))
edit_cp_button.grid(row=6, column=0, pady=(5, 0))

ws.mainloop()
