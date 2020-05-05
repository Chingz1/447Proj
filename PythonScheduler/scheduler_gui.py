# from tkinter import *
import os
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
import subprocess as sub
import sys
# import xlrd
import pandas as pd

global G_out
global inFile
global outFile
PIPE = '|'
#colors
GOLD='#ffbf00'
BACKGROUND='#FFF8F4'


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs, bg='blue')

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Welcome to the Schedule Generator!")
        label.pack(side='bottom', anchor=tk.S, fill="both", expand=True)


def on_closing():
    if messagebox.askokcancel("Quit", "Hold up! Closing this window will quit the program. Do you want to quit?"):
        root.destroy()
        sys.exit()


def generate():
    runthis = 'python3 schedule2.py ' + inFile + ' ' + outFile
    os.system(runthis)
    # output= sub.run(['python3','schedule2.py',inFile,outFile], check=True,capture_output=True).stdout

    # x = sub.check_output(['python3','schedule2.py','ClassRoom.xlsx','output.csv'])
    # sys.stdout = Std_redirector(text)
    # p = sub.Popen('python3 schedule2.py ClassRoom.xlsx output.csv',stdout=sub.PIPE,stderr=sub.PIPE)
    # output, errors = p.communicate()


def view_schedule():
    master = tk.Tk()
    scrollbar = tk.Scrollbar(master)
    master.title('View Schedule')
    scrollbar.pack(side="right", fill=tk.Y, expand=False)
    listbox = tk.Listbox(master, yscrollcommand=scrollbar.set,bg=BACKGROUND)
    df = pd.read_excel(outFile, sheet_name='Schedule')
    sched_list = df.values.tolist()
    print_out_list = {"Scheduled:": [], "Unscheduled:": []}

    for i in range(len(sched_list)):
        if sched_list[i][len(sched_list[i]) - 1].lower() == "scheduled":
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
    master.mainloop()



def go(page, inF, outF):
    global inFile
    global outFile
    # do error checking for input and output files here
    inFile = str(inF.get())
    outFile = str(outF.get())
    if ".xlsx" in inF.get() and ".xlsx" in outF.get():  # Checks whether input and output files are correctly formatted
        if os.path.isfile(inFile):
            generate()
            root.deiconify()  # Unhides the root window
            page.destroy()  # Removes the toplevel window
        else:
            messagebox.showerror("File Error", "Input file could not be found.")
    else:
        messagebox.showerror("File Error", "Both the input file and output file need to be xlsx files.")


def quit_top(top, root):
    top.destroy()  # Removes the toplevel window
    root.destroy()  # Removes the hidden root window
    sys.exit()  # Ends the script


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        title_frame = tk.Frame(self)
        container.configure(bg=BACKGROUND)
        title_frame.configure(bg='black')

        label1 = tk.Label(title_frame, text="Welcome to the Scheduler!", font=("Helvetica", 32),fg='white',bg='black')

        b2 = tk.Button(container, text="View Schedule", command=view_schedule, highlightthickness=0,bg=GOLD)
        b3 = tk.Button(container, text="View Statistics", highlightthickness=0,bg=GOLD)  # , command=p3.lift)

        label1.pack(side="top", anchor=tk.N,pady=10)
        b2.pack(side="left", padx=20)
        b3.pack(side="right", padx=20)
        title_frame.pack(side="top",fill='x')
        container.pack(side="bottom", fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title('Main Menu')
    
    entry = tk.Toplevel(bg=BACKGROUND)
    entry.protocol("WM_DELETE_WINDOW", on_closing)
    entry.title('Start Up')
    
    tk.Grid.rowconfigure(entry, 0, weight=1)
    tk.Grid.columnconfigure(entry, 0, weight=1)
    
    #Create & Configure frame 
    frame=tk.Frame(entry,bg=BACKGROUND)
    frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    for row_index in range(6):
        tk.Grid.rowconfigure(frame, row_index, weight=1)
        for col_index in range(5):
            tk.Grid.columnconfigure(frame, col_index, weight=1)
    
    inputFile = ''
    ouputFile = ''
    title_label = tk.Label(frame, text="Welcome to the Scheduler!", font=("Helvetica", 32),fg='white',bg='black')
    title_label.grid(row=0, column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)
    entry.bind('<Return>', lambda e: go(entry, inputFile, outputFile))
    tk.Label(frame, text="Please make sure both the input file and output file are excel workbook files (.xlsx). \n The scheduler is not designed to work with any other files", bg=BACKGROUND).grid(row=5, column=0,columnspan=6, sticky=tk.N+tk.S+tk.E+tk.W)

    tk.Label(frame, text="Input file:", bg=BACKGROUND).grid(row=3, column=0, sticky=tk.N+tk.S,padx=5)
    inputFile = tk.Entry(frame)
    inputFile.config(highlightthickness=0)
    inputFile.grid(row=3, column=1, sticky=tk.E+tk.W)
    tk.Label(frame, text="Output file:", bg=BACKGROUND).grid(row=3, column=2, sticky=tk.N+tk.S,padx=5)
    outputFile = tk.Entry(frame)
    outputFile.config(highlightthickness=0)
    outputFile.grid(row=3, column=3, sticky=tk.E+tk.W)
    
    button1 = tk.Button(frame, text="Generate", command=lambda: go(entry, inputFile, outputFile), bg=GOLD, relief=tk.RAISED)
    button1.config(highlightthickness=0)
    button2 = tk.Button(frame, text="Quit", command=lambda: quit_top(entry, root), bg=GOLD,
                        relief=tk.RAISED)  # quit button
    button2.config(highlightthickness=0)
    button1.grid(row=3, column=4, sticky=tk.E+tk.W,padx = 10,pady=5)
    button2.grid(row=3, column=5, sticky=tk.E+tk.W, padx = 10,pady=5,ipadx=10)
    root.withdraw()
    # bg_frame = GradientFrame(root, from_color="#000000", to_color="#E74C3C", height=100)

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()