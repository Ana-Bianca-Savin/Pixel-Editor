from backend.canvas import Canvas
from backend.layer import BlendingMode

from tkinter import *
from tkinter import Canvas
from tkinter import ttk
from PIL import ImageTk, Image

# Colors for buttons
btn_color1 = '#606266'
btn_color2 = '#72757a'
btn_color3 = 'BLACK'

btn_highlight1 = "#81848a"
btn_highlight2 = "#7a7e85"
btn_highlight3 = "WHITE"

# List of all buttons for layer
btn_layers_list = []

# Index of the last highlighted button
last_btn_highlighted = 0

# How many buttons there are, used for naming the buttons, after some have been deleted
btn_count = 1

# Create a button for a layer
def create_button_layer(_parent_frame, c1, c2, c3, index, text_index, canvas: Canvas) -> Button:
    return Button(
        _parent_frame,
        background=c1,
        foreground=c3,
        highlightthickness=2,
        highlightbackground=c1,
        highlightcolor='WHITE',
        activebackground=c2,
        activeforeground=c3,
        cursor='hand1',
        borderwidth=1,
        text="Layer " + str(text_index),
        command=lambda var=index, canvas=canvas: change_active_layer(var, canvas)
    )

def create_button_img(_parent_frame, size, c1, c2, c3, image) -> Button:
    return Button(
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

def change_active_layer(index, canvas: Canvas):
    global btn_layers_list, last_btn_highlighted
    print(f'index : {index}, last_btn_high : {last_btn_highlighted}')
    # Set the new active layer
    canvas.set_active_layer(index)
    print(index)

    # Highlight the active layer's button
    btn_layers_list[index].configure(
        background=btn_highlight1,
        foreground=btn_highlight3,
        highlightbackground=btn_highlight1,
        activebackground=btn_highlight2,
        activeforeground=btn_highlight3
        )

    # Return the old highlighted button to normal
    if last_btn_highlighted != index:
        btn_layers_list[last_btn_highlighted].configure(
            background=btn_color1,
            foreground=btn_color3,
            highlightbackground=btn_color1,
            activebackground=btn_color2,
            activeforeground=btn_color3
        )
        last_btn_highlighted = index

def add_layer_btn(canvas: Canvas, layers_canvas, layers_frame):
    global btn_layers_list, btn_dummy, btn_count

    # Add new layer to canvas layer list and new button to button list
    canvas.add_layer(BlendingMode.NORMAL)
    btn_count += 1
    btn_layers_list.append(create_button_layer(layers_frame, btn_color1, btn_color2, btn_color3, len(canvas.layers)-1, btn_count-1, canvas))

    btn_dummy.grid_forget()

    # Permute all buttons a row down from their initial position, to make room for the new button
    for i in range(0, len(btn_layers_list)):
        btn_layers_list[i].grid_forget()
        btn_layers_list[i].grid(row=len(btn_layers_list) - i - 1, column=0, sticky='ew')
    btn_layers_list[len(btn_layers_list) - 1].grid(row=0, column=0, sticky='ew')
    change_active_layer(len(btn_layers_list) - 1, canvas)

    if len(btn_layers_list) >= 4:
        btn_dummy.grid(row=len(btn_layers_list), column=0, sticky='ew')

    # Reconfigure canvas for the new size
    layers_canvas.configure(scrollregion = layers_canvas.bbox('all'))

def delete_layer_button(canvas: Canvas, layers_canvas):
    global btn_layers_list, last_btn_highlighted

    # If there if only one layer left, it can NOT be deleted
    if len(canvas.layers) == 1:
        return
    
    # Get the index of the layer that needs to be deleted
    index = canvas.get_active_layer_index()
    canvas.delete_layer(index)

    btn_dummy.grid_forget()
    
    # Refactor the buttons' rows
    for i in range(index, -1, -1):
        btn_layers_list[i].grid_forget()
        if len(btn_layers_list) - i - 2 < 0:
            continue
        else:
            btn_layers_list[i].grid(row=len(btn_layers_list) - i - 2, column=0, sticky='ew')
    btn_layers_list[index].destroy()
    btn_layers_list.pop(index)

    # Rebind the buttons
    for i in range(len(btn_layers_list)):
        btn_layers_list[i].configure(command=lambda var=i, canvas=canvas: change_active_layer(var, canvas))
    if (index != 0):
        last_btn_highlighted = index - 1
        change_active_layer(index - 1, canvas)
    else:
        change_active_layer(0, canvas)

    if len(btn_layers_list) >= 4:
        btn_dummy.grid(row=len(btn_layers_list), column=0, sticky='ew')

    # Reconfigure canvas for the new size
    layers_canvas.configure(scrollregion = layers_canvas.bbox('all'))

def switch_up(canvas: Canvas, layers_canvas):
    global btn_layers_list

    # Get the index of the layer that needs to be moved
    index = canvas.get_active_layer_index()
    if index == len(canvas.layers) - 1:
        return

    aux_text = btn_layers_list[index].cget("text")
    btn_layers_list[index].configure(text = btn_layers_list[index + 1].cget("text"), command=lambda var=index, canvas=canvas: change_active_layer(var, canvas))
    btn_layers_list[index + 1].configure(text = aux_text, command=lambda var=index+1, canvas=canvas: change_active_layer(var, canvas))

    canvas.layers[index], canvas.layers[index + 1] = canvas.layers[index + 1], canvas.layers[index]
    canvas.update_top_texture()

    change_active_layer(index + 1, canvas)

    # Reconfigure canvas for the new size
    layers_canvas.configure(scrollregion = layers_canvas.bbox('all'))

def switch_down(canvas: Canvas, layers_canvas):
    global btn_layers_list

    # Get the index of the layer that needs to be moved
    index = canvas.get_active_layer_index()
    if index == 0:
        return

    aux_text = btn_layers_list[index].cget("text")
    btn_layers_list[index].configure(text = btn_layers_list[index - 1].cget("text"), command=lambda var=index, canvas=canvas: change_active_layer(var, canvas))
    btn_layers_list[index - 1].configure(text = aux_text, command=lambda var=index-1, canvas=canvas: change_active_layer(var, canvas))

    canvas.layers[index], canvas.layers[index - 1] = canvas.layers[index - 1], canvas.layers[index]
    canvas.update_top_texture()

    change_active_layer(index - 1, canvas)

    # Reconfigure canvas for the new size
    layers_canvas.configure(scrollregion = layers_canvas.bbox('all'))


def create_layer_scroller(_parent_frame, canvas: Canvas):
    global add_img, delete_img, up_img, down_img
    layers_wrapper = LabelFrame(_parent_frame)

    layers_canvas = Canvas(layers_wrapper, width=200, height=120)
    layers_canvas.pack(side=LEFT, fill='both', expand='yes')

    yscrollbar = ttk.Scrollbar(layers_wrapper, orient='vertical', command=layers_canvas.yview)
    yscrollbar.pack(side=RIGHT, fill='y')

    layers_canvas.config(yscrollcommand=yscrollbar.set)

    layers_canvas.bind('<Configure>', lambda e: layers_canvas.configure(scrollregion = layers_canvas.bbox('all')))

    layers_frame = Frame(layers_canvas)
    layers_frame.columnconfigure(0, weight=1)
    layers_canvas.create_window((0,0), width=240, window=layers_frame, anchor='nw')

    layers_wrapper.grid(row=0, column=2, sticky='nwe', padx=10, pady=(45, 10))

    # Add an invisible object as the last one
    # This fixes a bug where the last layer was not visible when scrolling
    global btn_dummy
    btn_dummy = (Button(
        layers_frame,
        background='WHITE',
        borderwidth=1,
    ))

    # Initially, there is only one layer which is highlighted
    btn_layers_list.append(create_button_layer(layers_frame, btn_highlight1, btn_highlight2, btn_highlight3, 0, 0, canvas))
    btn_layers_list[0].grid(row=0, column=0, sticky='ew')

    # Buttons for layers
    add_img = ImageTk.PhotoImage(Image.open('./assets/icons8-plus-24.png'))
    delete_img = ImageTk.PhotoImage(Image.open('./assets/icons8-minus-24.png'))
    up_img = ImageTk.PhotoImage(Image.open('./assets/icons8-up-24.png'))
    down_img = ImageTk.PhotoImage(Image.open('./assets/icons8-down-24.png'))

    # Create, configure and display the 4 buttons for editing layers
    btn_add = create_button_img(_parent_frame, 30, btn_color1, btn_color2, btn_color3, add_img)
    btn_add.configure(command=lambda canvas=canvas, l1=layers_canvas, l2=layers_frame: add_layer_btn(canvas, l1, l2))
    btn_add.grid(row=0, column=2, sticky='nw', pady=(10, 0), padx=10)

    btn_delete = create_button_img(_parent_frame, 30, btn_color1, btn_color2, btn_color3, delete_img)
    btn_delete.configure(command=lambda canvas=canvas, l1=layers_canvas:delete_layer_button(canvas, l1))
    btn_delete.grid(row=0, column=2, sticky='nw', pady=(10, 0), padx=(45, 10))

    btn_up = create_button_img(_parent_frame, 30, btn_color1, btn_color2, btn_color3, up_img)
    btn_up.configure(command=lambda canvas=canvas, l1=layers_canvas: switch_up(canvas, l1))
    btn_up.grid(row=0, column=2, sticky='nw', pady=(10, 0), padx=(80, 10))

    btn_down = create_button_img(_parent_frame, 30, btn_color1, btn_color2, btn_color3, down_img)
    btn_down.configure(command=lambda canvas=canvas, l1=layers_canvas: switch_down(canvas, l1))
    btn_down.grid(row=0, column=2, sticky='nw', pady=(10, 0), padx=(115, 10))