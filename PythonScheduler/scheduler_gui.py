# from tkinter import *
import os
import tkinter as tk
import subprocess as sub
import sys
# import xlrd
import pandas as pd

global G_out
global inFile
global outFile
PIPE = '|'
try:
    from Tkinter import Canvas
    from Tkconstants import *
except ImportError:
    from tkinter import Canvas
    from tkinter.constants import *

from PIL import Image, ImageDraw, ImageTk

# Python 2/3 compatibility
try:
    basestring
except NameError:
    basestring = str

"""def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]
        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)
    return tuple(int(v, 16) for v in (r, g, b))
"""


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg='blue')

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Welcome to the Schedule Generator!")
        label.pack(side="top", fill="both", expand=True)


def generate():
    # os.system('python3 schedule2.py ClassRoom.xlsx output.csv')
    global G_out
    output = sub.run(['python3', 'schedule2.py', inFile, outFile], check=True, capture_output=True).stdout
    output = str(output)[2:]
    G_out = output.split('\\n')
    # x = sub.check_output(['python3','schedule2.py','ClassRoom.xlsx','output.csv'])
    # sys.stdout = Std_redirector(text)
    # p = sub.Popen('python3 schedule2.py ClassRoom.xlsx output.csv',stdout=sub.PIPE,stderr=sub.PIPE)
    # output, errors = p.communicate()


def view_schedule():
    global G_out
    master = tk.Tk()
    scrollbar = tk.Scrollbar(master)
    scrollbar.pack(side="right", fill=tk.Y, expand=False)
    listbox = tk.Listbox(master, yscrollcommand=scrollbar.set)
    df = pd.read_excel(outFile, sheet_name='Schedule')
    sched_list = df.values.tolist()
    print_out_list = {"Scheduled:": [], "Unscheduled:": []}

    for i in range(len(sched_list)):
        if sched_list[i][len(sched_list[i]) - 1]:
            print_out_list["Scheduled:"].append(sched_list[i][:len(sched_list[i]) - 1])
        else:
            print_out_list["Unscheduled:"].append(sched_list[i][:len(sched_list[i]) - 1])
    for key in print_out_list.keys():
        listbox.insert(tk.END, key)
        for i in range(len(print_out_list[key])):
            listbox.insert(tk.END, str(print_out_list[key][i]))
        # listbox.insert(tk.END, '\n')
    listbox.pack(side="left", fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview_scroll)

    temp = tk.Button(text="test")
    outputfile = open("output.xlsx")

    outputfile.close()
    master.mainloop()


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Show schedule here")
        label.pack(side="top", fill="both", expand=True)


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Show statistics here")
        label.pack(side="top", fill="both", expand=True)


def go(page, inF, outF):
    global inFile
    global outFile
    # do error checking for input and output files here
    inFile = str(inF.get())
    outFile = str(outF.get())
    if "xlsx" in inF.get() and "xlsx" in outF.get():  # Checks whether input and output files are correctly formatted

        root.deiconify()  # Unhides the root window
        page.destroy()  # Removes the toplevel window


def quit_top(top, root):
    top.destroy()  # Removes the toplevel window
    root.destroy()  # Removes the hidden root window
    sys.exit()  # Ends the script


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg='blue')
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Generate Schedule", command=generate)
        b2 = tk.Button(buttonframe, text="View Schedule", command=view_schedule)
        b3 = tk.Button(buttonframe, text="View Statistics", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()


'''class GradientFrame(Canvas):
    def __init__(self, master, from_color, to_color, width=None, height=None, orient=HORIZONTAL, steps=None, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        if steps is None:
            if orient == HORIZONTAL:
                steps = height
            else:
                steps = width
        if isinstance(from_color, basestring):
            from_color = hex2rgb(from_color)

        if isinstance(to_color, basestring):
            to_color = hex2rgb(to_color)
        r,g,b = from_color
        dr = float(to_color[0] - r)/steps
        dg = float(to_color[1] - g)/steps
        db = float(to_color[2] - b)/steps
        if orient == HORIZONTAL:
            if height is None:
                raise ValueError("height can not be None")

            self.configure(height=height)

            if width is not None:
                self.configure(width=width)
            img_height = height
            img_width = self.winfo_screenwidth()
            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)
            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                y0 = int(float(img_height * i)/steps)
                y1 = int(float(img_height * (i+1))/steps)
                draw.rectangle((0, y0, img_width, y1), fill=(int(r),int(g),int(b)))
        else:
            if width is None:
                raise ValueError("width can not be None")
            self.configure(width=width)

            if height is not None:
                self.configure(height=height)
            img_height = self.winfo_screenheight()
            img_width = width

            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)
            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                x0 = int(float(img_width * i)/steps)
                x1 = int(float(img_width * (i+1))/steps)
                draw.rectangle((x0, 0, x1, img_height), fill=(int(r),int(g),int(b)))

        self._gradient_photoimage = ImageTk.PhotoImage(image)
        self.create_image(0, 0, anchor=NW, image=self._gradient_photoimage)
'''
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Main Menu')
    entry = tk.Toplevel(bg='#99badd')
    label1 = tk.Label(entry, text="Input file:", bg='#99badd').pack(side='left')
    inputFile = tk.Entry(entry)
    inputFile.config(highlightthickness=0)
    inputFile.pack(side='left')
    label2 = tk.Label(entry, text="Output file:", bg='#99badd').pack(side='left')
    outputFile = tk.Entry(entry)
    outputFile.config(highlightthickness=0)
    outputFile.pack(side='left')
    button1 = tk.Button(entry, text="Go", command=lambda: go(entry, inputFile, outputFile), bg='black',
                        fg="white")  # keep going button
    button1.config(highlightthickness=0)
    button2 = tk.Button(entry, text="Quit", command=lambda: quit_top(entry, root), bg='black',
                        fg='white')  # quit button
    button2.config(highlightthickness=0)
    # epage = EntryPage(entry)
    button1.pack(side='left')
    button2.pack(side='left')
    root.withdraw()
    # bg_frame = GradientFrame(root, from_color="#000000", to_color="#E74C3C", height=100)

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()