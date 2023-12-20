from testing.color_palette import Color_Palette as cp
from testing.manage_color_palette import create_new_palette, edit_palette
from testing.menu import *


def change_draw_color(color: str, current_color: StringVar):
    current_color.set(color)


def open_menu(ws, project_name, canvas, scale_factors):
    use_menu(ws, project_name, canvas, scale_factors)


class SideBarGUI:
    def __init__(self, canvas, ws, columnFrame):
        self.current_palette_idx = 0
        self.palettes_idxs = ["1"]
        self.color_palettes = [cp(["black"])]
        self.palette_buttons_array = []

    def display_line(self, nr_of_colors: int, colors, start_idx: int, ypadding: int, columnFrame,
                     current_color: StringVar):

        if nr_of_colors == 1:
            color_button = CanvasWidget(columnFrame, width=50, height=50)
            color_button.configure(bg=self.color_palettes[self.current_palette_idx].colors[start_idx])
            color_button.grid(row=7 + ypadding, column=0)
            color_button.bind("<Button-1>"
                              , lambda event, color=colors[start_idx]: change_draw_color(color, current_color))
            self.palette_buttons_array.append(color_button)
        elif nr_of_colors == 2:
            color_button = CanvasWidget(columnFrame, width=50, height=50)
            color_button.configure(bg=self.color_palettes[self.current_palette_idx].colors[start_idx])
            color_button.grid(row=7 + ypadding, column=0, padx=(0, 65))
            color_button.bind("<Button-1>"
                              , lambda event, color=colors[start_idx]: change_draw_color(color, current_color))
            self.palette_buttons_array.append(color_button)

            color_button = CanvasWidget(columnFrame, width=50, height=50)
            color_button.configure(bg=self.color_palettes[self.current_palette_idx].colors[start_idx + 1])
            color_button.grid(row=7 + ypadding, column=0, padx=(65, 0))
            color_button.bind("<Button-1>"
                              , lambda event, color=colors[start_idx + 1]: change_draw_color(color, current_color))
            self.palette_buttons_array.append(color_button)
        elif nr_of_colors == 3:
            color_button = CanvasWidget(columnFrame, width=50, height=50)
            color_button.configure(bg=self.color_palettes[self.current_palette_idx].colors[start_idx])
            color_button.grid(row=7 + ypadding, column=0, padx=(0, 115))
            color_button.bind("<Button-1>"
                              , lambda event, color=colors[start_idx]: change_draw_color(color, current_color))
            self.palette_buttons_array.append(color_button)

            color_button = CanvasWidget(columnFrame, width=50, height=50)
            color_button.configure(bg=self.color_palettes[self.current_palette_idx].colors[start_idx + 1])
            color_button.grid(row=7 + ypadding, column=0)
            color_button.bind("<Button-1>"
                              , lambda event, color=colors[start_idx + 1]: change_draw_color(color, current_color))
            self.palette_buttons_array.append(color_button)

            color_button = CanvasWidget(columnFrame, width=50, height=50)
            color_button.configure(bg=self.color_palettes[self.current_palette_idx].colors[start_idx + 2])
            color_button.grid(row=7 + ypadding, column=0, padx=(115, 0))
            color_button.bind("<Button-1>"
                              , lambda event, color=colors[start_idx + 2]: change_draw_color(color, current_color))
            self.palette_buttons_array.append(color_button)

    def update_palette_colors_display(self, columnFrame, current_color):
        if len(self.palette_buttons_array) > 0:
            for i in self.palette_buttons_array:
                i.destroy()

        cnt = 0
        self.palette_buttons_array = []

        for i in range(len(self.color_palettes[self.current_palette_idx].colors)):
            if i % 3 == 0:
                if i + 2 < len(self.color_palettes[self.current_palette_idx].colors):
                    self.display_line(3, self.color_palettes[self.current_palette_idx].colors, i, cnt,
                                      columnFrame, current_color)
                elif i + 1 < len(self.color_palettes[self.current_palette_idx].colors):
                    self.display_line(2, self.color_palettes[self.current_palette_idx].colors, i, cnt,
                                      columnFrame, current_color)
                else:
                    self.display_line(1, self.color_palettes[self.current_palette_idx].colors, i, cnt,
                                      columnFrame, current_color)

            if (i + 1) % 3 == 0:
                cnt += 1

        change_draw_color(self.color_palettes[self.current_palette_idx].colors[0], current_color)

    def palette_on_option_change(self, value, columnFrame, current_color: StringVar):
        self.current_palette_idx = self.palettes_idxs.index(value)
        self.update_palette_colors_display(columnFrame, current_color)

    # define a function to create a new color palette
    def create_palette(self, ws, select_field, select, columnFrame, current_color):

        # new color palette object reference
        new_cp = cp([])
        # palette name stored as a str list to pass it by reference, so it is mutable
        palette_name = [""]

        create_new_palette(ws, new_cp, palette_name, self.color_palettes)

        if not new_cp.colors:
            return

        self.color_palettes.append(new_cp)

        self.current_palette_idx = len(self.color_palettes) - 1

        if palette_name[0] == "":
            idx = len(self.color_palettes)

            # find the first available index
            while str(idx) in self.palettes_idxs or str(idx + 1) in self.palettes_idxs:
                idx += 1
                if str(idx) not in self.palettes_idxs and str(idx + 1) not in self.palettes_idxs:
                    break

            self.palettes_idxs.append(str(idx))
            new_cp.name = str(idx)
        else:
            self.palettes_idxs.append(palette_name[0])
        select_field.set(self.palettes_idxs[self.current_palette_idx])

        select.destroy()
        select = OptionMenu(columnFrame, select_field, *self.palettes_idxs
                            , command=lambda v: self.palette_on_option_change(select_field.get(), columnFrame,
                                                                              current_color))
        select.grid(row=4, column=0)

        self.update_palette_colors_display(columnFrame, current_color)

    def edit_existing_palette(self, ws, select_field, select, columnFrame, current_color):

        # save the current_palette_idx in a list to pass it by reference, so it is mutable
        current_idx = [self.current_palette_idx]
        # memorize the old length of the color palettes array
        old_cps_len = len(self.color_palettes)
        # palette name stored as a str list to pass it by reference, so it is mutable
        palette_name = [self.palettes_idxs[self.current_palette_idx]]

        edit_palette(ws, self.color_palettes, current_idx, palette_name)
        # in case a change occurred, reflect it on the palette index
        if len(self.color_palettes) != old_cps_len:
            # make an array of the remaining palette names
            palettes_names = []
            for i in range(len(self.color_palettes)):
                palettes_names.append(self.color_palettes[i].name)
            print(self.palettes_idxs)
            print(palettes_names)

            # find the deleted palette index
            deleted_idx = -1
            for i in range(len(self.palettes_idxs)):
                if self.palettes_idxs[i] not in palettes_names:
                    deleted_idx = i
                    break

            print(deleted_idx)
            print(self.palettes_idxs[deleted_idx])

            # remove the deleted palette index from the palettes_idxs array
            self.palettes_idxs.remove(self.palettes_idxs[deleted_idx])
            select_field.set(self.palettes_idxs[current_idx[0]])

            # destroy the option menu then rebuild it updated
            select.destroy()
            select = OptionMenu(columnFrame, select_field, *self.palettes_idxs
                                , command=lambda v: self.palette_on_option_change(select_field.get(), columnFrame,
                                                                                  current_color))
            select.grid(row=4, column=0)
            select_field.trace("w", lambda *args: self.palette_on_option_change(select_field.get(), columnFrame,
                                                                                current_color))

            # if a change occurred, update the current_palette_idx
            self.current_palette_idx = current_idx[0]
        else:
            # if no change occurred, update the palette name
            self.palettes_idxs[current_idx[0]] = palette_name[0]
            select_field.set(self.palettes_idxs[current_idx[0]])

            # destroy the option menu then rebuild it updated
            select.destroy()
            select = OptionMenu(columnFrame, select_field, *self.palettes_idxs
                                , command=lambda v: self.palette_on_option_change(select_field.get(), columnFrame,
                                                                                  current_color))
            select.grid(row=4, column=0)
            select_field.trace("w", lambda *args: self.palette_on_option_change(select_field.get(), columnFrame,
                                                                                current_color))

        # if there are no colors in the palette, exit
        if not self.color_palettes[self.current_palette_idx].colors:
            return

        self.update_palette_colors_display(columnFrame, current_color)
