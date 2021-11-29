"""
graphical user interface for the wiefilter
"""

from tkinter import Tk, Listbox, Frame, Button, Label, Y, END
from tkinter import filedialog
from tkinter import ttk

import os

from PIL import ImageTk, Image


class Window(Frame):
    """
    Window holding the application
    """

    def __init__(self, master=None):
        ""
        super().__init__(master)
        self.master = master
        self.pack()

        self.images = []
        self.image_path = {}
        self.image = None
        self.current_index = 0
        #
        self.mk_sections()
        #
        self.mk_btns()
        self.mk_list()

        self.quit_btn = Button(self, text="Quit", command=self.master.destroy)
        self.quit_btn.pack(side="bottom")

    def mk_sections(self):
        ""
        # frameler
        self.btns = Frame(self)
        self.btns.pack(side="bottom", fill="both", expand="yes")
        #
        self.image_list_f = Frame(self)
        self.image_list_f.pack(side="top", fill="both", expand="yes")

        self.image_f = Frame(self.image_list_f)
        self.image_f.pack(side="right", fill="both", expand="yes")

        self.list_f = Frame(self.image_list_f)
        self.list_f.pack(side="left", fill=Y, expand="yes")

    def mk_list(self):
        ""
        self.image_list = Listbox(self.list_f, relief="sunken", selectmode="single")
        self.image_list.pack(side="top", fill=Y, expand="yes")

        self.list_btn = Button(self.list_f, text="Load", command=self.load_images)
        self.list_btn.pack(side="bottom", fill="both", expand="yes")

    def load_images(self):
        ""
        fds = filedialog.askopenfiles(initialdir="./", title="load images")
        self.clear_list()

        #
        for f in fds:
            name = os.path.basename(f.name)
            path = f.name
            self.image_path[name] = path

        self.images = list(self.image_path.values())
        for r in self.image_path.keys():
            self.image_list.insert(END, r)

        self.go_forward()

    def clear_list(self):
        ""
        self.images = []
        self.image_path = {}
        for i in range(self.image_list.size()):
            self.image_list.delete(i)

    def mk_btns(self):
        ""
        self.forward_btn = Button(self.btns, text=">", command=self.go_forward)
        self.forward_btn.pack(side="right")

        self.back_btn = Button(self.btns, text="<", command=self.go_back)
        self.back_btn.pack(side="left")

    def go_forward(self):
        ""
        self.current_index += 1
        self.choose_image()
        self.choose_list()

    def go_back(self):
        ""
        self.current_index -= 1
        self.choose_image()
        self.liste_sec()

    def choose_image(self):
        ""
        if self.current_index >= len(self.images):
            self.current_index = 0
        if self.current_index < 0:
            self.current_index = 0
        img = Image.open(self.images[self.current_index])
        self.image = ImageTk.PhotoImage(img)
        self.clean_image()
        self.panel = Label(self.image_f, image=self.image)
        self.panel.pack(side="top")

    def choose_list(self):
        ""
        self.image_list.activate(self.current_index)

    def clean_image(self):
        ""
        for w in self.image_f.winfo_children():
            w.destroy()


if __name__ == "__main__":
    # main application
    root = Tk()
    app = Window(root)
    app.mainloop()
