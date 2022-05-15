import ctypes
import sys
import time
from tkinter import *
from tkinter.colorchooser import askcolor

from PIL import Image
from tkinter import filedialog, ttk
import os
import shutil
from sign_pdf import sign_file, load, mess
import customtkinter
global img_path


root = customtkinter.CTk()
root.title('VVB.Cloud')
root["bg"] = "#333333"

root.iconbitmap('logo.ico')
root.geometry("700x600+300+150")
root.resizable(width=True, height=True)

lbl1 = Label(root, text="VVB.Cloud", bg="#333333", fg="#007bff", font="none 40 bold")
lbl1.config(anchor=CENTER)
lbl1.place(anchor=CENTER, relx=.5, rely=.2)

message = StringVar()



def open_fn():
    global file_path
    file_path = filedialog.askopenfilename(title="Выберите документ для подписи", filetypes=(
        ("pdf", "*.pdf"), ("pdf", "*.pdf")))
    print(file_path)
    if file_path:
        l1 = customtkinter.CTkLabel(root, text="Путь до файла: " + file_path)
        l1.place(anchor=CENTER, relx=.5, rely=.5)
        l1 = customtkinter.CTkLabel(root, text="ФИО:")
        l1.place(anchor=CENTER, relx=.5, rely=.55)
        message_entry = customtkinter.CTkEntry(textvariable=message)
        message_entry.place(relx=.5, rely=.6, anchor="c")

        btn_img = customtkinter.CTkButton(root, text='Поставить подпись', fg_color="#007bff", command=open_img)
        btn_img.place(anchor=CENTER, relx=.5, rely=.7)
    else:
        pass


def open_img():
    Paint()


def sign_pdf():
    mess(message.get())
    try:
        os.mkdir("./static/")
    except:
        pass
    load()
    sign_file(file_path, "BM", 5, 5, img_path)
    shutil.make_archive('arhive', 'zip', './static/')
    file = os.path.abspath("arhive.zip")
    l1 = customtkinter.CTkLabel(root, text="Путь до архива: " + file)
    file = os.path.abspath("./arhive.zip")
    import subprocess
    subprocess.Popen(f'explorer /select, {file}')
    l1.place(anchor=CENTER, relx=.5, rely=.9)





def sign():
    print("Привет, Tkinter!")

btn = customtkinter.CTkButton(root, text='Выбрать документ', fg_color="#007bff",command=open_fn)
btn.place(anchor=CENTER, relx=.5, rely=.4)

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.iconbitmap('logo.ico')
        self.root.title('VVB.Cloud')

        self.pen_button = Button(self.root, text='Ручка', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.color_button = Button(self.root, text='Цвет', command=self.choose_color)
        self.color_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, text='Ластик', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

        self.c = Canvas(self.root, bg='white', width=300, height=300)
        self.c.grid(row=1, columnspan=5)


        self.eraser_button = Button(self.root, text='Сохранить', command=self.save_img)
        self.eraser_button.grid(row=2, column=2)

        self.setup()
        self.root.mainloop()

    def save_img(self):
        self.c.update()
        from PIL import EpsImagePlugin
        EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs9.56.1\bin\gswin64c'
        self.c.postscript(file="sign.ps", colormode='color')
        img = Image.open("sign.ps")
        try:
            os.mkdir("./static/")
        except:
            pass
        img.save("./static/sign.png", "png")
        global img_path
        img_path = os.path.abspath("./static/sign.png")
        self.root.destroy()
        if message.get():
            btn = customtkinter.CTkButton(root, text='Подписать', fg_color="#007bff", command=sign_pdf)
            btn.place(anchor=CENTER, relx=.5, rely=.8)
        else:
            l1 = customtkinter.CTkButton(root, text='Введите ФИО', fg_color="#FF2400")
            l1.place(anchor=CENTER, relx=.5, rely=.8)


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)



root.mainloop()
