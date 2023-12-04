from tkinter import *
from tkinter import Canvas as CanvasWidget
from tkinter import colorchooser
from PIL import ImageTk, Image

from testing.color_pallette import Color_Pallette

_new_pallette_colors = []


def create_new_pallette(_parent_window, new_cp: Color_Pallette):
    # open a new window
    create_pallette_window = Toplevel(_parent_window)
    create_pallette_window.title('Create new pallette')
    create_pallette_window.geometry('300x300')

    # Grab the input focus to disable interaction with the main window
    create_pallette_window.grab_set()

    # create a frame for the window
    _window_pallette_frame = Frame(create_pallette_window)
    _window_pallette_frame.columnconfigure(0, weight=1)
    _window_pallette_frame.pack()

    def return_pallette():
        global _new_pallette_colors
        new_cp.set_colors(_new_pallette_colors)
        update_colors_display()
        _new_pallette_colors = []
        # Release the grab to allow interaction with the main window
        create_pallette_window.grab_release()
        create_pallette_window.destroy()

    def get_color():
        global _new_pallette_colors
        _new_pallette_colors.append(colorchooser.askcolor()[1])
        update_colors_display()

    new_color_button = Button(_window_pallette_frame, text="Add new color", command=get_color)
    new_color_button.grid(row=0, column=0)

    # display colors added so far
    colors_so_far_label = Label(_window_pallette_frame, text="Colors so far:")
    colors_so_far_label.grid(row=1, column=0)

    return_pallette_button = Button(_window_pallette_frame, text="Create pallette", command=return_pallette)
    return_pallette_button.grid(row=len(_new_pallette_colors) + 3, column=0)

    new_color_button.grid(row=0, column=0)

    def update_colors_display():
        for i in _window_pallette_frame.winfo_children():
            i.destroy()

        new_color_button = Button(_window_pallette_frame, text="Add new color", command=get_color)
        new_color_button.grid(row=0, column=0)

        # display colors added so far
        colors_so_far_label = Label(_window_pallette_frame, text="Colors so far:")
        colors_so_far_label.grid(row=1, column=0)

        for i in range(len(_new_pallette_colors)):
            color_button = CanvasWidget(_window_pallette_frame, width=50, height=50)
            color_button.configure(bg=_new_pallette_colors[i])
            color_button.grid(row=i + 2, column=0, pady=5, padx=5)

        return_pallette_button = Button(_window_pallette_frame, text="Create pallette", command=return_pallette)
        return_pallette_button.grid(row=len(_new_pallette_colors) + 3, column=0)

    # Release the grab when the new window is closed
    create_pallette_window.protocol("WM_DELETE_WINDOW", lambda: release_grab(create_pallette_window))
    create_pallette_window.wait_window(create_pallette_window)

def release_grab(window):
    global _new_pallette_colors
    _new_pallette_colors = []
    # Release the grab to allow interaction with the main window
    window.grab_release()
    window.destroy()


