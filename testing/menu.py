from tkinter import *
from tkinter import filedialog
from tkinter import Canvas as CanvasWidget
from PIL import ImageTk, Image
from core import utilties as utils
from core.canvas import Canvas
from core.layer import Layer, BlendingMode


def use_menu(_parent_window: Tk, project_name: Label, canvas: Canvas, draw_scale: list[float]) -> None:
    # open the menu window
    menu_window = Toplevel(_parent_window)
    menu_window.title("Pixel Editor Menu")
    menu_window.geometry("500x500")

    # grab the input focus
    menu_window.grab_set()

    _menu_window_frame = Frame(menu_window)
    _menu_window_frame.columnconfigure(0, weight=1)
    _menu_window_frame.pack()

    information_label = Label(_menu_window_frame, text="Current Project Information")
    information_label.grid(row=0, column=0)

    def change_project_name() -> None:
        initial_project_name = project_name.cget("text")
        # open the change project name window
        change_project_name_window = Toplevel(menu_window)
        change_project_name_window.title("Change Project Name")
        change_project_name_window.geometry("200x100")

        def cancel_changes() -> None:
            project_name.config(text=initial_project_name)
            change_project_name_window.grab_release()
            change_project_name_window.destroy()
            menu_window.grab_set()

        def save_changes() -> None:
            if len(project_name_entry.get()) == 0:
                project_name.config(text=initial_project_name)
            else:
                project_name.config(text=project_name_entry.get())

            change_project_name_window.grab_release()
            change_project_name_window.destroy()
            menu_window.grab_set()
            project_name_label.configure(text=f'Project Name: {project_name.cget("text")}')

        _change_project_name_frame = Frame(change_project_name_window)
        _change_project_name_frame.columnconfigure(0, weight=1)
        _change_project_name_frame.pack()

        # grab the input focus
        menu_window.grab_release()
        change_project_name_window.grab_set()

        edit_project_name_label = Label(_change_project_name_frame, text="Edit Project Name")
        edit_project_name_label.grid(row=0, column=0)

        project_name_entry = Entry(_change_project_name_frame)
        project_name_entry.grid(row=1, column=0)
        project_name_entry.bind("<Return>", lambda event: save_changes())
        project_name_entry.focus_set()

        change_project_name_window.protocol("WM_DELETE_WINDOW", lambda: cancel_changes())
        change_project_name_window.wait_window(change_project_name_window)

    def export_current_texture() -> None:
        file_path = filedialog.asksaveasfilename(initialfile=f'{project_name.cget("text")}.png'
                                                 , defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if len(file_path) == 0:
            return
        else:
            img_to_save = canvas.top_texture.copy()
            img_to_save = img_to_save.resize((img_to_save.size[0]
                                              , img_to_save.size[1]))
            img_to_save.save(file_path)

    def import_texture() -> None:
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if len(file_path) == 0:
            return
        else:
            texture = utils.import_texture(file_path)
            texture.resize((texture.size[0], texture.size[1]))
            canvas.place_texture(texture, (canvas.size[0] // 2, canvas.size[1] // 2))

    def change_canvas_size() -> None:

        # open the change canvas size window
        change_canvas_size_window = Toplevel(menu_window)
        change_canvas_size_window.title("Change Canvas Size")
        change_canvas_size_window.geometry("200x200")

        def cancel_changes() -> None:
            change_canvas_size_window.grab_release()
            change_canvas_size_window.destroy()
            menu_window.grab_set()

        def save_changes() -> None:
            old_width = canvas.size[0]
            old_height = canvas.size[1]

            if len(width_entry.get()) == 0:
                width = canvas.size[0]
            else:
                width = int(width_entry.get())

            if len(height_entry.get()) == 0:
                height = canvas.size[1]
            else:
                height = int(height_entry.get())

            canvas.size = (width, height)

            # resize all the layers
            for i in range(len(canvas.layers)):
                new_layer_texture = Image.new("RGBA", canvas.size, canvas.layers[i].texture.getpixel((0, 0)))
                new_layer_texture.paste(canvas.layers[i].texture, (width // 2 - old_width // 2
                                                                   , height // 2 - old_height // 2))
                canvas.layers[i] = Layer(canvas.size, canvas.layers[i].blending_mode, new_layer_texture)

            # update the top texture
            canvas.update_top_texture()

            draw_scale[0] = 800.0 / canvas.size[0]

            change_canvas_size_window.grab_release()
            change_canvas_size_window.destroy()
            menu_window.grab_set()

        _change_canvas_size_frame = Frame(change_canvas_size_window)
        _change_canvas_size_frame.columnconfigure(0, weight=1)
        _change_canvas_size_frame.pack()

        # grab the input focus
        menu_window.grab_release()
        change_canvas_size_window.grab_set()

        edit_canvas_size_label = Label(_change_canvas_size_frame, text="Edit Canvas Size")
        edit_canvas_size_label.grid(row=0, column=0)

        width_label = Label(_change_canvas_size_frame, text="Width")
        width_label.grid(row=1, column=0)

        width_entry = Entry(_change_canvas_size_frame)
        width_entry.grid(row=2, column=0)
        width_entry.bind("<Return>", lambda event: save_changes())
        width_entry.focus_set()

        height_label = Label(_change_canvas_size_frame, text="Height")
        height_label.grid(row=3, column=0)

        height_entry = Entry(_change_canvas_size_frame)
        height_entry.grid(row=4, column=0)
        height_entry.bind("<Return>", lambda event: save_changes())

        change_canvas_size_window.protocol("WM_DELETE_WINDOW", lambda: cancel_changes())
        change_canvas_size_window.wait_window(change_canvas_size_window)

    # project name
    project_name_label = Label(_menu_window_frame, text=f'Project Name: {project_name.cget("text")}')
    project_name_label.grid(row=1, column=0)
    project_name_label.bind("<Button-1>", lambda event: change_project_name())

    # export current texture
    export_texture_button = Button(_menu_window_frame, text="Export Current Texture", command=export_current_texture)
    export_texture_button.grid(row=2, column=0)

    # import a texture
    import_texture_button = Button(_menu_window_frame, text="Import Texture", command=import_texture)
    import_texture_button.grid(row=3, column=0)

    # change canvas size
    change_canvas_size_button = Button(_menu_window_frame, text="Change Canvas Size", command=change_canvas_size)
    change_canvas_size_button.grid(row=4, column=0)

    def release_grab():
        menu_window.grab_release()
        menu_window.destroy()

    menu_window.protocol("WM_DELETE_WINDOW", lambda: release_grab())
    menu_window.wait_window(menu_window)
