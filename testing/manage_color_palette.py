from tkinter import *
from tkinter import Canvas as CanvasWidget
from tkinter import colorchooser

from testing.color_palette import Color_Palette

_new_palette_colors = []
_editable_palette = []


def create_new_palette(_parent_window, new_cp: Color_Palette, palette_name: list[str], color_palettes):
    global _new_palette_colors
    # open a new window
    create_palette_window = Toplevel(_parent_window)
    create_palette_window.title('Create new palette')
    create_palette_window.geometry('400x400')

    # Grab the input focus to disable interaction with the main window
    create_palette_window.grab_set()

    # create a frame for the window
    _window_palette_frame = Frame(create_palette_window)
    _window_palette_frame.columnconfigure(0, weight=1)
    _window_palette_frame.pack()

    def return_palette():
        global _new_palette_colors
        new_cp.set_colors(_new_palette_colors)
        update_colors_display()
        _new_palette_colors = []

        # set the palette nam, so it is identifiable without the need of the palette_idx array
        if new_cp.name == "1":
            new_cp.name = str(len(color_palettes) + 1)

        # Release the grab to allow interaction with the main window
        create_palette_window.grab_release()
        create_palette_window.destroy()

    def add_new_color() -> None:
        global _new_palette_colors
        color = colorchooser.askcolor()[1]
        if color:
            _new_palette_colors.append(color)
        update_colors_display()

    def get_input() -> None:
        palette_name[0] = palette_name_entry.get()
        if palette_name[0] != "":
            new_cp.name = palette_name[0]

    def update_color(_selected_color) -> None:
        def update_color_display():
            _current_color_canvas.configure(bg=_selected_color.cget('bg'))
            _current_color_hex_label.configure(text=_selected_color.cget('bg'))

        # allow the user to modify the color : update or remove it
        old_bg = _selected_color.cget('bg')
        # open a new window
        _edit_color_window = Toplevel(create_palette_window)
        _edit_color_window.title('Edit color')
        _edit_color_window.geometry('300x300')

        # Grab the input focus to disable interaction with the palette creation window
        _edit_color_window.grab_set()

        def modify_color(event):
            new_color = colorchooser.askcolor()[1]
            _selected_color.configure(bg=new_color)
            update_color_display()

        # create a frame for the window
        _edit_color_frame = Frame(_edit_color_window)
        _edit_color_frame.columnconfigure(0, weight=1)
        _edit_color_frame.pack()

        # display a label, the color and its hex code
        _current_color_label = Label(_edit_color_frame, text="Current color:")
        _current_color_label.grid(row=1, column=0)

        _current_color_canvas = CanvasWidget(_edit_color_frame, width=50, height=50)
        _current_color_canvas.configure(bg=_selected_color.cget('bg'))
        _current_color_canvas.grid(row=2, column=0, padx=(0, 75))
        _current_color_canvas.bind("<Button-1>", modify_color)

        _current_color_hex_label = Label(_edit_color_frame, text=_selected_color.cget('bg'))
        _current_color_hex_label.grid(row=2, column=0, padx=(45, 0))

        def save_changes():
            global _new_palette_colors
            _new_palette_colors[_new_palette_colors.index(old_bg)] = _current_color_canvas.cget(
                'bg')
            update_colors_display()
            _edit_color_window.grab_release()
            _edit_color_window.destroy()

        # save changes button
        save_changes_button = Button(_edit_color_frame, text="Save changes", command=lambda: save_changes())
        save_changes_button.grid(row=0, column=0, padx=(0, 140))

        def delete_color():
            global _new_palette_colors
            _new_palette_colors.remove(old_bg)
            update_colors_display()
            _edit_color_window.grab_release()
            _edit_color_window.destroy()

        # delete color button
        delete_color_button = Button(_edit_color_frame, text="Delete color", command=lambda: delete_color())
        delete_color_button.grid(row=0, column=0, padx=(100, 0))

        def cancel_changes():
            global _new_palette_colors
            _new_palette_colors[_new_palette_colors.index(old_bg)] = old_bg
            update_colors_display()
            _edit_color_window.grab_release()
            _edit_color_window.destroy()

        _edit_color_window.protocol("WM_DELETE_WINDOW", lambda: cancel_changes())
        _edit_color_window.wait_window(_edit_color_window)

    palette_name_entry = Entry(_window_palette_frame)
    palette_name_entry.grid(row=0, column=0, pady=(3, 0))
    palette_name_entry.bind("<Return>", lambda event: get_input())

    # set_palette_name_button = Button(_window_palette_frame, text="Set palette name", command=get_input)
    # set_palette_name_button.grid(row=0, column=0, padx=(120, 0))

    add_color_button = Button(_window_palette_frame, text="Add new color", command=add_new_color)
    add_color_button.grid(row=1, column=0)

    # display colors added so far
    colors_so_far_label = Label(_window_palette_frame, text="Colors so far:")
    colors_so_far_label.grid(row=2, column=0)

    return_palette_button = Button(_window_palette_frame, text="Create palette", command=return_palette)
    return_palette_button.grid(row=len(_new_palette_colors) + 4, column=0)

    def display_line(nr_of_colors: int, colors, start_idx: int, ypadding: int):
        if nr_of_colors == 1:
            color_button = CanvasWidget(_window_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx])
            color_button.grid(row=3 + ypadding, column=0)
            color_button.bind("<Button-1>"
                              , lambda event, color=color_button: update_color(color))
        elif nr_of_colors == 2:
            color_button = CanvasWidget(_window_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx])
            color_button.grid(row=3 + ypadding, column=0, padx=(0, 65))
            color_button.bind("<Button-1>"
                              , lambda event, color=color_button: update_color(color))

            color_button = CanvasWidget(_window_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx + 1])
            color_button.grid(row=3 + ypadding, column=0, padx=(65, 0))
            color_button.bind("<Button-1>"
                              , lambda event, color=color_button: update_color(color))
        elif nr_of_colors == 3:
            color_button = CanvasWidget(_window_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx])
            color_button.grid(row=3 + ypadding, column=0, padx=(0, 115))
            color_button.bind("<Button-1>"
                              , lambda event, color=color_button: update_color(color))

            color_button = CanvasWidget(_window_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx + 1])
            color_button.grid(row=3 + ypadding, column=0)
            color_button.bind("<Button-1>"
                              , lambda event, color=color_button: update_color(color))

            color_button = CanvasWidget(_window_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx + 2])
            color_button.grid(row=3 + ypadding, column=0, padx=(115, 0))
            color_button.bind("<Button-1>"
                              , lambda event, color=color_button: update_color(color))

    def release_grab(window) -> None:
        global _new_palette_colors
        _new_palette_colors = []
        # Release the grab to allow interaction with the main window
        window.grab_release()
        window.destroy()

    def update_colors_display() -> None:
        for i in _window_palette_frame.winfo_children():
            if i.winfo_class() != 'Entry':
                i.destroy()

        palette_name_entry.delete(0, END)
        palette_name_entry.insert(0, palette_name[0])

        add_color_button = Button(_window_palette_frame, text="Add new color", command=add_new_color)
        add_color_button.grid(row=1, column=0)

        # display colors added so far
        colors_so_far_label = Label(_window_palette_frame, text="Colors so far:")
        colors_so_far_label.grid(row=2, column=0)

        cnt = 0

        for i in range(len(_new_palette_colors)):
            if i % 3 == 0:
                if i + 2 < len(_new_palette_colors):
                    display_line(3, _new_palette_colors, i, cnt)
                elif i + 1 < len(_new_palette_colors):
                    display_line(2, _new_palette_colors, i, cnt)
                else:
                    display_line(1, _new_palette_colors, i, cnt)

            if (i + 1) % 3 == 0:
                cnt += 1

        return_palette_button = Button(_window_palette_frame, text="Create palette", command=return_palette)
        return_palette_button.grid(row=len(_new_palette_colors) + 4, column=0)

    # Release the grab when the new window is closed
    create_palette_window.protocol("WM_DELETE_WINDOW", lambda: release_grab(create_palette_window))
    create_palette_window.wait_window(create_palette_window)


def edit_palette(_parent_window: Tk, palettes_array, current_idx: list[int], palette_name: list[str]):
    current_palette_idx = current_idx[0]

    global _editable_palette
    _editable_palette = palettes_array[current_palette_idx].colors

    # open a new window
    edit_palette_window = Toplevel(_parent_window)
    edit_palette_window.title('Edit palette')
    edit_palette_window.geometry('400x400')

    # save the initial palette
    old_palette = palettes_array[current_palette_idx].colors.copy()
    # Grab the input focus to disable interaction with the main window
    edit_palette_window.grab_set()

    # create a frame for the window
    _edit_palette_frame = Frame(edit_palette_window)
    _edit_palette_frame.columnconfigure(0, weight=1)
    _edit_palette_frame.pack()

    def edit_palette_save_changes() -> None:
        global _editable_palette
        palettes_array[current_palette_idx].set_colors(_editable_palette)
        palettes_array[current_palette_idx].name = palette_name[0]
        _editable_palette = []
        # Release the grab to allow interaction with the main window
        edit_palette_window.grab_release()
        edit_palette_window.destroy()

    def edit_palette_add_new_color() -> None:
        global _editable_palette
        color = colorchooser.askcolor()[1]
        if color:
            _editable_palette.append(color)
        update_colors_display()

    def edit_palette_cancel_changes() -> None:
        global _editable_palette
        _editable_palette = []

        palettes_array[current_palette_idx].set_colors(old_palette)
        # Release the grab to allow interaction with the main window
        edit_palette_window.grab_release()
        edit_palette_window.destroy()

    def edit_palette_delete_palette() -> None:
        # check if the palette can be deleted
        # as in check if it's the only palette, if so do not delete it
        if len(palettes_array) == 1:
            error_cannot_delete_only_palette = Toplevel(edit_palette_window)
            error_cannot_delete_only_palette.geometry('300x75')
            error_cannot_delete_only_palette.title('Error')

            error_label = Label(error_cannot_delete_only_palette, text="Can't delete the only palette")
            error_label.pack()

            print("can't delete the only palette")

            palettes_array[current_palette_idx].set_colors(old_palette)
            # check if the index is 0, if so remove the palette and move at ex-index 1
        else:
            if current_palette_idx == 0:
                palettes_array.pop(current_palette_idx)
            # check if the index is len(palettes_array) - 1, if so, move at ex-index len(palettes_array) - 2
            elif current_palette_idx == len(palettes_array) - 1:
                current_idx[0] -= 1
                palettes_array.pop(current_palette_idx)
            else:
                palettes_array.pop(current_palette_idx)

            edit_palette_window.grab_release()
            edit_palette_window.destroy()

    def get_input():
        palette_name[0] = update_palette_name_entry.get()

    # color_idx is the index of the _selected_color background in the _editable_palette array
    def edit_palette_update_color(_selected_color, color_idx: int) -> None:
        def update_color_display():
            _current_color_canvas.configure(bg=_selected_color.cget('bg'))
            _current_color_hex_label.configure(text=_selected_color.cget('bg'))

        # allow the user to modify the color : update or remove it
        old_bg = _selected_color.cget('bg')
        # open a new window
        _edit_color_window = Toplevel(edit_palette_window)
        _edit_color_window.title('Edit color')
        _edit_color_window.geometry('300x300')

        # Grab the input focus to disable interaction with the palette creation window
        edit_palette_window.grab_release()
        _edit_color_window.grab_set()

        def update_color_modify_color(event):
            new_color = colorchooser.askcolor()[1]
            if new_color:
                _selected_color.configure(bg=new_color)
            update_color_display()

        # create a frame for the window
        _edit_color_frame = Frame(_edit_color_window)
        _edit_color_frame.columnconfigure(0, weight=1)
        _edit_color_frame.pack()

        # display a label, the color and its hex code
        _current_color_label = Label(_edit_color_frame, text="Current color:")
        _current_color_label.grid(row=1, column=0)

        _current_color_canvas = CanvasWidget(_edit_color_frame, width=50, height=50)
        _current_color_canvas.configure(bg=_selected_color.cget('bg'))
        _current_color_canvas.grid(row=2, column=0, padx=(0, 75))
        _current_color_canvas.bind("<Button-1>", update_color_modify_color)

        _current_color_hex_label = Label(_edit_color_frame, text=_selected_color.cget('bg'))
        _current_color_hex_label.grid(row=2, column=0, padx=(45, 0))

        def update_color_save_changes():
            global _editable_palette
            _editable_palette[color_idx] = _selected_color.cget('bg')

            update_colors_display()
            _edit_color_window.grab_release()
            edit_palette_window.grab_set()
            _edit_color_window.destroy()

        # save changes button
        save_changes_button = Button(_edit_color_frame, text="Save changes",
                                     command=lambda: update_color_save_changes())
        save_changes_button.grid(row=0, column=0, padx=(0, 140))

        def update_color_delete_color():
            global _editable_palette
            _editable_palette.pop(color_idx)

            update_colors_display()
            _edit_color_window.grab_release()
            edit_palette_window.grab_set()
            _edit_color_window.destroy()

        # delete color button
        delete_color_button = Button(_edit_color_frame, text="Delete color",
                                     command=lambda: update_color_delete_color())
        delete_color_button.grid(row=0, column=0, padx=(100, 0))

        def update_color_cancel_changes():
            _selected_color.configure(bg=old_bg)
            update_colors_display()
            _edit_color_window.grab_release()
            edit_palette_window.grab_set()
            _edit_color_window.destroy()

        _edit_color_window.protocol("WM_DELETE_WINDOW", lambda: update_color_cancel_changes())
        _edit_color_window.wait_window(_edit_color_window)

    update_palette_name_entry = Entry(_edit_palette_frame)
    update_palette_name_entry.grid(row=0, column=0, pady=(3, 0))
    update_palette_name_entry.bind("<Return>", lambda event: get_input())

    add_color_button = Button(_edit_palette_frame, text="Add new color", command=edit_palette_add_new_color)
    add_color_button.grid(row=1, column=0, padx=(0, 100))

    delete_palette_button = Button(_edit_palette_frame, text="Delete palette", command=edit_palette_delete_palette)
    delete_palette_button.grid(row=1, column=0, padx=(100, 0))

    # display colors added so far
    colors_so_far_label = Label(_edit_palette_frame, text="Colors so far:")
    colors_so_far_label.grid(row=2, column=0)

    def display_line(nr_of_colors: int, colors, start_idx: int, ypadding: int):
        if nr_of_colors == 1:
            color_button = CanvasWidget(_edit_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx])
            color_button.grid(row=3 + ypadding, column=0)
            color_button.bind("<Button-1>"
                              , lambda event, color_idx=start_idx, color=color_button: edit_palette_update_color(
                                color, color_idx))
        elif nr_of_colors == 2:
            color_button = CanvasWidget(_edit_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx])
            color_button.grid(row=3 + ypadding, column=0, padx=(0, 65))
            color_button.bind("<Button-1>"
                              , lambda event, color_idx=start_idx, color=color_button: edit_palette_update_color(
                                color, color_idx))

            color_button = CanvasWidget(_edit_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx + 1])
            color_button.grid(row=3 + ypadding, column=0, padx=(65, 0))
            color_button.bind("<Button-1>"
                              , lambda event, color_idx=start_idx + 1, color=color_button: edit_palette_update_color(
                                color, color_idx))
        elif nr_of_colors == 3:
            color_button = CanvasWidget(_edit_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx])
            color_button.grid(row=3 + ypadding, column=0, padx=(0, 115))
            color_button.bind("<Button-1>"
                              , lambda event, color_idx=start_idx, color=color_button: edit_palette_update_color(
                                color, color_idx))

            color_button = CanvasWidget(_edit_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx + 1])
            color_button.grid(row=3 + ypadding, column=0)
            color_button.bind("<Button-1>"
                              , lambda event, color_idx=start_idx + 1, color=color_button: edit_palette_update_color(
                                color, color_idx))

            color_button = CanvasWidget(_edit_palette_frame, width=50, height=50)
            color_button.configure(bg=colors[start_idx + 2])
            color_button.grid(row=3 + ypadding, column=0, padx=(115, 0))
            color_button.bind("<Button-1>"
                              , lambda event, color_idx=start_idx + 2, color=color_button: edit_palette_update_color(
                                color, color_idx))

    cnt = 0

    for i in range(len(_editable_palette)):
        if i % 3 == 0:
            if i + 2 < len(_editable_palette):
                display_line(3, _editable_palette, i, cnt)
            elif i + 1 < len(_editable_palette):
                display_line(2, _editable_palette, i, cnt)
            else:
                display_line(1, _editable_palette, i, cnt)

        if (i + 1) % 3 == 0:
            cnt += 1

    return_palette_button = Button(_edit_palette_frame, text="Save palette", command=edit_palette_save_changes)
    return_palette_button.grid(row=len(_editable_palette) + 4, column=0)

    def update_colors_display() -> None:
        global _editable_palette
        for i in _edit_palette_frame.winfo_children():
            if i.winfo_class() != 'Entry':
                i.destroy()

        new_color_button = Button(_edit_palette_frame, text="Add new color", command=edit_palette_add_new_color)
        new_color_button.grid(row=1, column=0, padx=(0, 100))

        delete_palette_button = Button(_edit_palette_frame, text="Delete palette", command=edit_palette_delete_palette)
        delete_palette_button.grid(row=1, column=0, padx=(100, 0))

        # display colors added so far
        colors_so_far_label = Label(_edit_palette_frame, text="Colors so far:")
        colors_so_far_label.grid(row=2, column=0)

        cnt = 0
        for i in range(len(_editable_palette)):
            if i % 3 == 0:
                if i + 2 < len(_editable_palette):
                    display_line(3, _editable_palette, i, cnt)
                elif i + 1 < len(_editable_palette):
                    display_line(2, _editable_palette, i, cnt)
                else:
                    display_line(1, _editable_palette, i, cnt)

            if (i + 1) % 3 == 0:
                cnt += 1

        return_palette_button = Button(_edit_palette_frame, text="Save palette", command=edit_palette_save_changes)
        return_palette_button.grid(row=len(_editable_palette) + 4, column=0)

    # Release the grab when the new window is closed
    edit_palette_window.protocol("WM_DELETE_WINDOW", lambda: edit_palette_cancel_changes())
    edit_palette_window.wait_window(edit_palette_window)
