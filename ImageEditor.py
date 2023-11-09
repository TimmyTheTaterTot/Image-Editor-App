import tkinter as tk, time, os
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
import image_processing, byuimage


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
        self.filepath = None

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
        self.filter_settings = tk.StringVar()

        # create application frames
        self.info_frame = tk.Frame(master=self.window, height=20)
        top_spacer_frame = tk.Frame(master=self.window, height=1, background="black")
        self.images_frame = tk.Frame(master=self.window)

        # create widgets that go into above frames
        self.in_image_lbl = tk.Label(master=self.images_frame, width=40, height=17, background="grey", text="placeholder")
        middle_spacer_frame = tk.Frame(master=self.images_frame, width=1, background="black")
        self.out_img_lbl = tk.Label(master=self.images_frame, width=40, height=17, background="grey", text="placeholder")
        load_img_button = tk.Button(master=self.info_frame, text="Load New Image", command=self.handle_load_image)
        filter_apply_button = tk.Button(master=self.info_frame, text="Apply", command=self.handle_apply_filter)
        filter_dropdown = tk.OptionMenu(self.info_frame, self.selected_filter, "display", *self.filters, command=self.handle_filter_change)
        self.info_label = tk.Label(master=self.info_frame, text='')
        self.filter_settings_entry = tk.Entry(master=self.info_frame, textvariable=self.filter_settings, width = 5)
        self.filter_settings_label = tk.Label(master=self.info_frame, pady=4)

        # grid application frames
        self.info_frame.grid(row=0, sticky="ew")
        top_spacer_frame.grid(row=1, sticky="nsew")
        self.images_frame.grid(row=2, sticky="nsew")

        # grid the frame widgets
        self.in_image_lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        middle_spacer_frame.grid(row=0, column=1, sticky="ns")
        self.out_img_lbl.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        load_img_button.pack(side=tk.LEFT, padx=4, pady=4)
        filter_apply_button.pack(side=tk.RIGHT, padx=4, pady=4)
        filter_dropdown.pack(side=tk.RIGHT, padx=4, pady=4)
        self.info_label.pack(side=tk.LEFT, padx=4, pady=4)

        # begin window main loop
        self.window.mainloop()
        # fmt: on

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

        self.filepath = filepath
        print(self.filepath)
        self.open_file(filepath)

    def handle_filter_change(self, option):
        if option == "darken":
            self.filter_settings_label.config(text="darken percent:")

            self.filter_settings_entry.pack(side=tk.RIGHT)
            self.filter_settings_label.pack(side=tk.RIGHT)
        if option == "make border":
            self.filter_settings_label.config(text="border width:")

            self.filter_settings_entry.pack(side=tk.RIGHT)
            self.filter_settings_label.pack(side=tk.RIGHT)

    def handle_apply_filter(self):
        option = self.selected_filter.get()
        img_filepath = "cached_images/image_cache.jpg"
        if option == "display":
            image_processing.display((0, self.filepath))

        try:
            img = Image.open(img_filepath)
            self.output_img, img_width, img_height = Application.scale_image(img)
        except:
            self.info_label.config(text="No image Loaded")

        self.out_img_lbl.config(
            image=self.output_img,
            background="light grey",
            text="",
            width=img_width,
            height=img_height,
        )

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
