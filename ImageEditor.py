import tkinter as tk, time, os
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import colorchooser
from PIL import ImageTk, Image
import image_processing, byuimage

import shutil


class Application:
    def __init__(self):
        self.filters = [
            "darken",
            "sepia",
            "grayscale",
            "make border",
            "flip",
            "mirror",
            "composite",
            "greenscreen",
        ]
        self.filepath = [None]

        try:
            os.mkdir(os.path.join(os.getcwd(), "cached_images"))
        except OSError:
            pass

        self.init_window()

    def init_window(self):
        # fmt: off
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.selected_filter = tk.StringVar()
        self.selected_filter.set("display")
        self.filter_settings = tk.DoubleVar()

        # create application frames
        self.info_frame = tk.Frame(master=self.window)
        top_spacer_frame = tk.Frame(master=self.window, height=1, background="black")
        self.images_frame = tk.Frame(master=self.window)
        self.bottom_frame = tk.Frame(master=self.window)

        # create widgets that go into above frames
        self.in_image_lbl = tk.Label(master=self.images_frame, width=50, height=17, background="grey", text="No Image")
        middle_spacer_frame = tk.Frame(master=self.images_frame, width=1, background="black")
        self.out_img_lbl = tk.Label(master=self.images_frame, width=50, height=17, background="grey", text="No Image")
        load_img_button = tk.Button(master=self.info_frame, text="Load New Image", command=self.handle_load_image)
        filter_apply_button = tk.Button(master=self.info_frame, text="Apply", command=self.handle_apply_filter)
        filter_dropdown = tk.OptionMenu(self.info_frame, self.selected_filter, "display", *self.filters, command=self.handle_filter_change)
        self.info_label = tk.Label(master=self.info_frame, text='')
        self.filter_settings_entry = tk.Entry(master=self.info_frame, textvariable=self.filter_settings, width = 5)
        self.filter_settings_label = tk.Label(master=self.info_frame, pady=4)
        self.color_picker_button = tk.Button(master=self.info_frame, text="Choose border color", command=self.color_picker, padx=4, pady=4)
        self.save_button = tk.Button(master=self.bottom_frame, text="Save Image", command=self.handle_save_image, padx=4, pady=4)

        # grid application frames
        self.info_frame.grid(row=0, sticky="nsew")
        top_spacer_frame.grid(row=1, sticky="nsew")
        self.images_frame.grid(row=2, sticky="nsew")
        self.bottom_frame.grid(row=3, sticky='ew')

        # grid the frame widgets
        self.in_image_lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        middle_spacer_frame.grid(row=0, column=1, sticky="ns")
        self.out_img_lbl.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        load_img_button.pack(side=tk.LEFT, padx=4, pady=4)
        filter_apply_button.pack(side=tk.RIGHT, padx=4, pady=4)
        filter_dropdown.pack(side=tk.RIGHT, padx=4, pady=4)
        self.info_label.pack(side=tk.LEFT, padx=4, pady=4)

        # set the close_window function to be run when the user closes the window
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # begin window main loop
        self.window.mainloop()
        # fmt: on

    def close_window(self):
        # remove the image_cache file
        shutil.rmtree("./cached_images")
        self.window.destroy()

    def handle_load_image(self):
        # uses the file dialogue to get input for and process an image file
        filepath = askopenfilename(
            filetypes=[
                ("Image Files", "*.png .jpg .jpeg .ico .bmp"),
                ("All Files", "*.*"),
            ]
        )
        if not filepath:
            self.info_label.config(text="Invalid file path. Please try again.")
            return

        self.filepath[0] = filepath
        self.open_file(filepath)
        self.save_button.pack_forget()
        self.bottom_frame.config(height=1)

        self.out_img_lbl.config(
            image="",
            width=40,
            height=17,
            background="grey",
            text="No Image",
        )

    def handle_save_image(self):
        destination_path = asksaveasfilename(
            defaultextension=".png", filetypes=[(".png", "*.png")], initialfile="output"
        )
        if not destination_path:
            self.info_label.config(text="Invalid file path. Please try again.")
            return

        # copies the image from cache to the save location
        src = "./cached_images/image_cache.png"
        shutil.copy(src, destination_path)

    def handle_filter_change(self, option):
        if option == "darken":
            self.filter_settings_label.config(text="darken percent:")

            self.filter_settings_entry.pack(side=tk.RIGHT)
            self.filter_settings_label.pack(side=tk.RIGHT)
        elif option == "make border":
            self.filter_settings_label.config(text="border width:")

            self.filter_settings_entry.pack(side=tk.RIGHT)
            self.filter_settings_label.pack(side=tk.RIGHT)
            self.color_picker_button.pack(side=tk.RIGHT)
        else:
            self.filter_settings_entry.pack_forget()
            self.filter_settings_label.pack_forget()
            self.color_picker_button.pack_forget()

        self.save_button.pack_forget()
        self.bottom_frame.config(height=1)

    def handle_apply_filter(self):
        option = self.selected_filter.get()
        img_filepath = "cached_images/image_cache.png"

        # check if there is an input file yet or not
        if not self.filepath[0]:
            self.info_label.config(text="Cannot Apply. No input file.")
            return

        # call the image_processing library function depending on the options chosen by the user
        if option == "display":
            image_processing.display([self.filepath[0]])
        elif option == "darken":
            try:
                # code that allows the input box to accept percent values and decimal values
                darken_percent = float(self.filter_settings.get())
                if darken_percent >= 1:
                    darken_percent /= 100

                image_processing.darken([self.filepath[0], darken_percent])
            except tk.TclError:
                self.info_label.config(text="Invalid darken percent value")
                return
        elif option == "sepia":
            image_processing.sepia([self.filepath[0]])
        elif option == "grayscale":
            image_processing.grayscale([self.filepath[0]])
        elif option == "make border":
            try:
                border_thickness = float(self.filter_settings.get())

                image_processing.make_borders(
                    [self.filepath[0], border_thickness] + self.color_code
                )
            except tk.TclError:
                self.info_label.config("Invalid border thickness")
                return
        elif option == "flip":
            image_processing.flip([self.filepath[0]])
        elif option == "mirror":
            image_processing.mirror([self.filepath[0]])

        # opens the modified image and displays it in the output section
        # this is necessary because the image_processing library and the
        # PIL library which has TKinter image support have two slightly
        # different image formats
        try:
            img = Image.open(img_filepath)
            self.output_img, img_width, img_height = Application.scale_image(img)
        except:
            self.info_label.config(text="Error importing filtered image.")
            return

        self.out_img_lbl.config(
            image=self.output_img,
            background="light grey",
            text="",
            width=img_width,
            height=img_height,
        )

        # clean info_label output if no errors
        self.info_label.config(text="")
        self.save_button.pack(side=tk.RIGHT, padx=4, pady=4)

    def open_file(self, filepath):
        try:
            img = Image.open(filepath)

            self.input_img, img_width, img_height = Application.scale_image(img)
        except:
            self.info_label.config(text="Invalid image type or contents")

        self.in_image_lbl.config(
            image=self.input_img,
            background="light grey",
            text="",
            width=img_width,
            height=img_height,
        )

    def color_picker(self):
        try:
            self.color_code = list(colorchooser.askcolor(initialcolor="grey")[0])
        except TypeError:
            self.info_label.config(text="No color received. Operation cancelled.")
            return
        self.info_label.config(text="")

    @staticmethod
    def scale_image(img, max_x=500, max_y=400):
        img_width = img.width
        img_height = img.height

        scalarx = max_x / img_width
        scalary = max_y / img_height
        if scalarx > scalary:
            img_width *= scalary
            img_height *= scalary
        else:
            img_width *= scalarx
            img_height *= scalarx

        img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img, size=(img_width, img_height))
        return img, img_width, img_height


if __name__ == "__main__":
    app = Application()
