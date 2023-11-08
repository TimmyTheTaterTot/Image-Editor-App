import tkinter as tk
import time, image_processing
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


class Application:
    def __init__(self):
        self.init_window()

    def init_window(self):
        # fmt: off
        self.window = tk.Tk()
        self.window.resizable(False, False)

        self.info_frame = tk.Frame(master=self.window, height=20)
        top_spacer_frame = tk.Frame(master=self.window, height=1, background="black")
        self.images_frame = tk.Frame(master=self.window)

        self.in_image_lbl = tk.Label(master=self.images_frame, width=40, height=17, background="grey", text="placeholder") # tk.Label(master=self.images_frame, image=self.input_img)
        middle_spacer_frame = tk.Frame(master=self.images_frame, width=1, background="black")
        self.out_img_lbl = tk.Label(master=self.images_frame, width=40, height=17, background="grey", text="placeholder")
        load_img_button = tk.Button(master=self.info_frame, text="Load New Image", command=self.handle_load_image)
        self.info_label = tk.Label(master=self.info_frame, text='')

        self.info_frame.grid(row=0, sticky="ew")
        top_spacer_frame.grid(row=1, sticky="nsew")
        self.images_frame.grid(row=2, sticky="nsew")

        self.in_image_lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        middle_spacer_frame.grid(row=0, column=1, sticky="ns")
        self.out_img_lbl.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        load_img_button.pack(side=tk.LEFT, padx=4, pady=4)
        self.info_label.pack(side=tk.LEFT, padx=4, pady=4)

        self.window.rowconfigure(2, weight=1, minsize=200)
        self.window.columnconfigure(0, weight=1, minsize=600)
        self.images_frame.rowconfigure([0, 2], weight=2)
        self.images_frame.columnconfigure([0, 2], weight=2)

        self.window.mainloop()
        # fmt: on

    def handle_load_image(self):
        self.open_file()

    def open_file(self):
        # uses the file dialogue to get input for and process an image file
        filepath = askopenfilename(
            filetypes=[
                ("Image Files", "*.png .jpg .jpeg .ico .bmg"),
                ("All Files", "*.*"),
            ]
        )
        if not filepath:
            self.info_label.config(text="Invalid file path. Please try again.")
            return
        try:
            img = Image.open(filepath)
            img_width, img_height = img.size

            scalarx = 500/img_width
            scalary = 400/img_height
            if scalarx > scalary:
                img_width *= scalary
                img_height *= scalary
            else:
                img_width *= scalarx
                img_height *= scalarx

            img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)
            self.input_img = ImageTk.PhotoImage(img, size=(img_width, img_height))
        except:
            self.info_label.config(text="Invalid image type or contents")

        self.in_image_lbl.config(image=self.input_img, background="light grey", text="", width=img_width, height=img_height)


if __name__ == "__main__":
    app = Application()
